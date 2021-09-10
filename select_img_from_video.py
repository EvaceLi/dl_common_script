#从视频中获取图像。进行了一些筛选。
import os
import cv2

# video_base_path = "/home/cidi-gpu/disk/data1/datasets/701/record/full/backdoor"
video_path = "/home/cidi-gpu/disk/data1/datasets/headCount/mcamera_6/bus_data/315/41110/record/full/315_41110_0617_0619_video.txt"
difficult_path = '/home/cidi-gpu/disk/data1/liyi/diffcult_sample_data/315_41110_0620/315_41110_0620_diffcult.txt'
save_img_path = "/home/cidi-gpu/disk/data1/liyi/diffcult_sample_data/315_41110_0620/315_41110_0620_seletct_img"
bus_name = "41110"
os.makedirs(save_img_path, exist_ok=True)
difficult_list = open(difficult_path, 'r').readlines()
video_path_list = open(video_path, 'r').readlines()
video_list = []
all_video_name = [line.strip().split("/")[-1] for line in video_path_list]
for line in difficult_list:
    video_name = line.split(" ")[0]
    video_list.append(video_name)
    # frame_id = line.split(" ")[-1].strip()
video_name = list(set(video_list))

for name in video_name:
    # video_path = os.path.join(video_base_path, name.replace('.txt','.avi'))
    video_id = name.replace('.txt','.avi')
    print(video_id)
    video_path = video_path_list[all_video_name.index(video_id)].strip()
    print(video_path)
    frame_list = []
    for line in difficult_list:
        if line.split(" ")[0] == name:
            frame_list.append(line.split(" ")[-1].strip())
    frame_list = list(map(int, frame_list))
    video_capture = cv2.VideoCapture(video_path)
    id = 0
    while True:
        ret, img = video_capture.read()
        if ret!=True:
            break
        if id in frame_list:
            img_name = name.split(".txt")[0].replace(".", "_") +'_'+bus_name+'_'+ '%06d' % (id) + '.jpg'

            cv2.imwrite(os.path.join(save_img_path, img_name), img)
        id += 1
        print(id)

