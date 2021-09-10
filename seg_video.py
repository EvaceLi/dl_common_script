#该脚本用来分割不同区域的视频，分割后形成两个视频。
# 主要用途：有的时候由于远程传输数据需要压缩数据，所以是各个摄像头拼在一起的数据，故而需要分割
import cv2
import os
video_path = "/data/CIDI-data/xiangtan/43312_xt.txt"
# path = "/home/liyi/Pictures/Screenshot from 20201120122333190.pano.avi.png"
save_basepath = "/data/CIDI-data/xiangtan/43312_xt_split/"
def main():
    os.makedirs(save_basepath, exist_ok=True)
    size = (1280,720)
    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
    # fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    files = open(video_path)
    lines = files.readlines()
    img_id = 0
    for i,video_file in enumerate(lines[:]):
        video_capture = cv2.VideoCapture(video_file.strip())
        fps = video_capture.get(cv2.CAP_PROP_FPS)

        video_name1 = video_file.split("/")[-1].replace("passenger", "frontdoor").strip()
        video_name3 = video_file.split("/")[-1].replace("passenger", "backdoor").strip()
        save_path1 = save_basepath + "/" + video_name1
        save_path3 = save_basepath + "/" + video_name3
        video1 = cv2.VideoWriter(save_path1,fourcc,fps,size)
        video3 = cv2.VideoWriter(save_path3, fourcc, fps, size)
        i = 0
        while True:
            ret, img_org = video_capture.read()

            if ret != True:
                break
            # img0 = img_org[0:360, 0:640]  # 裁剪坐标为[y0:y1, x0:x1]
            img1 = img_org[0:360, 640:]  # 裁剪坐标为[y0:y1, x0:x1]
            # img2 = img_org[360:, 0:640]  # 裁剪坐标为[y0:y1, x0:x1]
            img3 = img_org[360:, 640:]  # 裁剪坐标为[y0:y1, x0:x1]
            front_img = cv2.resize(img1, (1280, 720))
            back_img = cv2.resize(img3, (1280, 720))
            video1.write(front_img)
            video3.write(back_img)

        img_id += 1
        print(img_id)
if __name__ == "__main__":
    main()
