
#从视频取图像
import time
import cv2
import scipy.misc as scm
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
video_path = "/home/cidi-gpu/disk/data1/liyi/test_cammer"
save_path = '/home/cidi-gpu/disk/data1/liyi/test_cammer_img'
def main():
    os.makedirs(save_path,exist_ok=True)
    for video_name in os.listdir(video_path):
        video_file = os.path.join(video_path, video_name)
        result_path = os.path.join(save_path, video_name.split('.')[0])
        os.makedirs(result_path, exist_ok=True)

        video_capture = cv2.VideoCapture(video_file)
        count = 0
        # print(count)
        frame = 0
        while True:
            ret, img_org = video_capture.read()
            if frame%1==0:
                print(frame)

                if ret != True:
                    break
                cv2.imwrite(result_path + "/" + str(frame) + '.jpg', img_org)
                frame = frame + 1

if __name__ == "__main__":
    main()