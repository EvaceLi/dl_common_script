#将车道线标注数据转换为Tusimple数据集格式
import os
import shutil
import json
import cv2
import numpy as np
org_path = "/6mm/json_0906"
save_img_path = "/6mm/images_0906"
save_json_path = "/6mm/train_0906.json"
space = 5
val = True
color = [(0,0,255),(0,0,180),(0,0,60),(0,255,0),(0,180,0),(0,60,0),(255,0,0),(180,0,0)]
def get_line(x1,x2,y1,y2):
    k = (x2 - x1) / (y2 - y1)
    b = x2-k*y2
    return k,b
def up_list(list):
    for i, elem in enumerate(list[1:]):
        if elem < list[i]:
            return False
        else:
            return True
def main():
    os.makedirs(save_img_path, exist_ok=True)
    result_json = open(save_json_path, "w")
    id = 0
    for name in os.listdir(org_path):
        path = name.strip()
        if path.endswith(".jpg"):
            shutil.copy2(os.path.join(org_path,path),os.path.join(save_img_path,name))
            continue
        org_json = open(os.path.join(org_path,path))
        print("{}|{}".format(len(os.listdir(org_path)),id))
        file = json.load(org_json)
        lane_point_x = []
        lane_point_y = []
        select_point_x = []
        select_point_y = []
        #per line
        # img = cv2.imread(os.path.join(save_img_path, name.replace(".json", ".jpg")))
        for i in range(len(file["objects"])):
            x_list = []
            y_list = []
            lane = file["objects"][i]
            line_point = lane["line"]
            # pre line points
            for points in line_point:
                x_list.append(points[0])
                y_list.append(points[1])

            # for i in range(len(y_list)-2):
            #     # cv2.circle(img,(int(x_list[i]),int(y_list[i])),2,255,2)
            #     cv2.line(img, (int(x_list[i]), int(y_list[i])), (int(x_list[i + 1]), int(y_list[i + 1])), 255, 10)
            # cv2.namedWindow("img",cv2.WINDOW_NORMAL)
            # cv2.imshow("img",img)
            # cv2.waitKey(0)
            assert len(x_list)==len(y_list)
            res_x_list = []
            res_y_list = []
            min_value = min(y_list)
            max_value = max(y_list)
            for h in range(10,1080,2):
                if h>max_value or h<min_value:
                    res_x_list.append(-2)
                    res_y_list.append(h)
                    continue
                is_up = up_list(y_list)
                if is_up:
                    short_line_index = ((np.array(y_list)>h)!=0).argmax(axis=0)
                    k,b = get_line(x_list[short_line_index-1],x_list[short_line_index],y_list[short_line_index-1],y_list[short_line_index])
                else:
                    short_line_index = ((np.array(y_list)<h)!=0).argmax(axis=0)
                    k,b = get_line(x_list[short_line_index],x_list[short_line_index-1],y_list[short_line_index],y_list[short_line_index-1])
                new_x = k*h+b
                res_x_list.append(int(new_x))
                res_y_list.append(h)
            res_x_list.reverse()
            res_y_list.reverse()
            lane_point_y = res_y_list[::int(space/2)]
            lane_point_x.append(res_x_list[::int(space/2)])
        if val:
            img = cv2.imread(os.path.join(save_img_path,name.replace(".json",".jpg")))
            color_index = 0
            for lane in lane_point_x:
                # print(lane)
                # print(lane_point_y)
                for i in range(len(lane)-1):
                    if(lane[i]>0) and (lane[i+1]>0):
                        # cv2.line(img,(int(lane[i]),int(lane_point_y[i])),(int(lane [i+1]),int(lane_point_y[i+1])),255,10)
                        cv2.circle(img,(int(lane[i]),int(lane_point_y[i])),2,color[color_index],2)
                        cv2.putText(img,name.replace(".json",".jpg"),(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
                color_index += 1
            cv2.namedWindow("img",cv2.WINDOW_NORMAL)
            cv2.imshow("img",img)
            cv2.waitKey(0)
        # img_path = os.path.join(save_img_path.split("/")[-2],save_img_path.split("/")[-1])+"/"+name.replace(".json",".jpg")
        img_path = save_img_path.split("/")[-1] + "/" + name.replace(".json",".jpg")
        data = {"lanes":lane_point_x, "h_samples":lane_point_y, "raw_file":img_path}
        json.dump(data,result_json)
        result_json.write("\n")
        id +=1
    result_json.close()

if __name__ == "__main__":
    main()