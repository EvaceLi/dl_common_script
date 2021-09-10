#将图像拼接起来，可视化
import cv2
import numpy as np
import os

path1 = '/test_origion_result/'
path2 = 'test_resize_result/'
save_path = '/compare_resize/'
def main():
    os.makedirs(save_path, exist_ok=True)
    # out_compare = np.hstack((images[0], images[1]))
    number = 0
    for name in os.listdir(path1):
        img2_path = path2+name
        img1_path = path1+name
        img2 = cv2.imread(img2_path, 1)
        img1 = cv2.imread(img1_path, 1)
        # out_compare = np.hstack((img1, img2))
        out_compare = np.concatenate([img1, img2], 1)
        save_img_path = save_path+name
        # cv2.imshow(out_compare)
        # cv2.namedWindow('result', 0)
        # cv2.resizeWindow('result', 1280, 720)
        # cv2.imshow('result', out_compare)
        cv2.imwrite(save_img_path, out_compare)
        number = number + 1
        print(number)
        # cv2.waitKey(0)
if __name__ == "__main__":
    main()