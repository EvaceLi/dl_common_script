#找难样本。比如用一个小网络yolov3裁剪网络生成的结果（txt），大网络yolov4生成的结果作为ＧＴ，
# 找出那些YOlov4检测出来了，yolov3出错的图片，称之为难样本，用于训练提高效果；
import os
import numpy as np

yolov3_base = "/home/cidi-gpu/disk/data1/liyi/diffcult_sample_data/315_41110_0620/v3/"
yolov4_base = '/home/cidi-gpu/disk/data1/liyi/diffcult_sample_data/315_41110_0620/v4/'
save_path = "/home/cidi-gpu/disk/data1/liyi/diffcult_sample_data/315_41110_0620_diffcult.txt"
def xyxy2xywh(x):
    y = np.array(x)
    y[:, 0] = x[:, 0]
    y[:, 1] = x[:, 1]
    y[:, 2] = x[:, 2] - x[:, 0]
    y[:, 3] = x[:, 3] - x[:, 1]
    return y


def compute_iou(bbox, candidates):
    """Computer intersection over union.

    Parameters
    ----------
    bbox : ndarray
        A bounding line in format `(top left x, top left y, width, height)`.
    candidates : ndarray
        A matrix of candidate bounding boxes (one per row) in the same format
        as `bbox`.

    """
    bbox_tl, bbox_br = bbox[:2], bbox[:2] + bbox[2:]
    candidates_tl = candidates[:, :2]
    candidates_br = candidates[:, :2] + candidates[:, 2:]

    tl = np.c_[np.maximum(bbox_tl[0], candidates_tl[:, 0])[:, np.newaxis],
               np.maximum(bbox_tl[1], candidates_tl[:, 1])[:, np.newaxis]]
    br = np.c_[np.minimum(bbox_br[0], candidates_br[:, 0])[:, np.newaxis],
               np.minimum(bbox_br[1], candidates_br[:, 1])[:, np.newaxis]]
    wh = np.maximum(0., br - tl)

    area_intersection = wh.prod(axis=1)
    area_bbox = bbox[2:].prod()
    area_candidates = candidates[:, 2:].prod(axis=1)
    # print(area_intersection)
    return area_intersection / (area_bbox + area_candidates - area_intersection)
def main():
    for video_name in os.listdir(yolov3_base):
        yolov4_path = yolov4_base+video_name
        yolov3_path = yolov3_base+video_name
    # video_name = yolov4_path.split("/")[-1].replace('.txt', '.avi')

        yolov3_file = open(yolov3_path, 'r')
        yolov4_file = open(yolov4_path, 'r')
        yolov3_list = yolov3_file.readlines()
        yolov4_list = yolov4_file.readlines()
        boxlist_v3 = []
        boxlist_v4 = []
        img_name_all_v3 = []
        img_name_all_v4 = []
        img_name_all_v3 = [line.strip().split(" ")[0] for line in yolov3_list]
        img_name_all_v4 = [line.strip().split(" ")[0] for line in yolov4_list]
        print(video_name)
        for line in yolov4_list:
            line = line.strip().split(" ")
            if len(line) > 1:
                # boxlist_v4.append([line[0], line[1], line[2], line[3], line[4], line[5]])
                ratios = (float(line[5])-float(line[3])) / (float(line[4])-float(line[2]))
                print(ratios)
                if ratios<2 and ratios>0.5:
                    boxlist_v4.append([line[0], line[1], line[2], line[3], line[4], line[5]])
                else:
                    # print(line)
                    # print(img_name_all_v4.count(line[0]))
                    if img_name_all_v4.count(line[0])==1:
                        # print('wwww')
                        boxlist_v4.append([line[0], 0, 0, 0, 0, 0])
                    else:
                        img_name_all_v4.remove(line[0])
            else:
                boxlist_v4.append([line[0], 0, 0, 0, 0, 0])

        for line in yolov3_list:
            line = line.strip().split(" ")
            if len(line) > 1:
                # boxlist_v3.append([line[0], line[1], line[2], line[3], line[4], line[5]])
                # if(video_name =='20200603133148961.backdoor.txt' and line[0]=='200'):
                #     print('rrr')
                ratios = (float(line[5])-float(line[3])) / (float(line[4])-float(line[2]))
                if ratios<2 and ratios>0.5:
                    boxlist_v3.append([line[0], line[1], line[2], line[3], line[4], line[5]])
                else:
                    if img_name_all_v3.count(line[0])==1:
                        boxlist_v3.append([line[0], 0, 0, 0, 0, 0])
                    else:
                        img_name_all_v3.remove(line[0])
            else:
                boxlist_v3.append([line[0], 0, 0, 0, 0, 0])
        box_np_v3 = np.array(boxlist_v3)
        box_np_v4 = np.array(boxlist_v4)

        img_name_list = []
        for line in box_np_v4:
            img_name_list.append(line[0])
        img_name = list(set(img_name_list))
        # print(img_name)
        for name in img_name:
            # print(video_name)
            # print(name)
            box4_ = box_np_v4[np.where(box_np_v4[:, 0] == name)]
            box4 = box4_[:, 2:].astype(float)

            box3_ = box_np_v3[np.where(box_np_v3[:, 0] == name)]
            # print(box_np_v3)
            box3 = box3_[:, 2:].astype(float)
            box3_numb = 0
            box4_numb = 0
            if box3.min() == 0:
                box3_numb = len(box3) - 1
            else:
                box3_numb = len(box3)
            if box4.min() == 0:
                box4_numb = len(box4) - 1
            else:
                box4_numb = len(box4)
            if box3_numb != box4_numb:
                # print(name + "number" + "\n")
                fp = open(save_path, "a+")
                fp.write(video_name + " " + name + '\n')
                continue
            if box4_numb == 0 and box3_numb == 0:
                continue
            box3 = xyxy2xywh(box3)
            box4 = xyxy2xywh(box4)
            for box in box3:
                iou = compute_iou(box, box4)
                if iou.max() > 0.3:
                    # print(str(iou) + "\n")
                    # print(name)
                    box4 = np.delete(box4, (np.argmax(iou)), axis=0)
                else:
                    # print(name)
                    # print(str(iou) + 'iou太小' + "\n")
                    fp = open(save_path, "a+")
                    fp.write(video_name + " " + name + '\n')
                    break

if __name__ =="__main__":
    main()
