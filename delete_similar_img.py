import os
import cv2
from queue import Queue
import shutil
import numpy as np
import random

path="empty_img/"
savepath="empty_selected/"
os.makedirs(savepath, exist_ok=True)
files = open("empty.txt","r").readlines()

# rmfiles=[]
# for i, file in enumerate(files):
#     f = file.replace('\n','')
#     if((f in rmfiles) or (i>=files.__len__()-1)):
#         continue
#     rmfile=[]
#     img = cv2.imread(f)
#     imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#     rmfiles.append(f)
#     rmfile.append(f)
#     for j, f2 in enumerate(files[i+1:]):
#             f2 = f2.replace('\n','')
#             img2 = cv2.imread(f2)
#             imgGray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
#             dist = abs(imgGray-imgGray2).mean()
#             print(dist)
#             if(dist>80):
#                 a = random.randint(0, rmfile.__len__()-1)
#                 # a = np.random.randint(0, rmfile.__len__(),1)[0]
#                 # print("fdsafasfasfd------------:   "+str(a))
#                 # shutil.copy(rmfile[a],savepath+rmfile[a].split('/')[-1])
#                 # cv2.imwrite(savepath+f,img)
#                 break
#             else:
#                 rmfiles.append(f2)
#                 rmfile.append(f2)

#                 cv2.namedWindow("image1",cv2.WINDOW_NORMAL)
#                 cv2.namedWindow("image2",cv2.WINDOW_NORMAL)
#                 cv2.imshow("image1",img)
#                 cv2.imshow("image2",img2)
#                 cv2.waitKey()



def create_rgb_hist(image):
    h, w, c = image.shape
    # 创建一个（16*16*16,1）的初始矩阵，作为直方图矩阵 
    # 16*16*16的意思为三通道每通道有16个bins
    rgbhist = np.zeros([32 * 32 * 32, 1], np.float32)
    bsize = 256 / 32
    for row in range(h):
        for col in range(w):
            b = image[row, col, 0]
            g = image[row, col, 1]
            r = image[row, col, 2]
            # 人为构建直方图矩阵的索引，该索引是通过每一个像素点的三通道值进行构建
            index = int(b / bsize) * 16 * 16 + int(g / bsize) * 16 + int(r / bsize)
           	# 该处形成的矩阵即为直方图矩阵
            rgbhist[int(index), 0] += 1
    # plt.ylim([0, 10000])
    # plt.grid(color='r', linestyle='--', linewidth=0.5, alpha=0.3)
    return rgbhist

rmfiles=[]
for i, file in enumerate(files):
    f = file.replace('\n','')
    if((f in rmfiles) or (i>=files.__len__()-1)):
        continue
    rmfile=[]
    img = cv2.imread(f)
    # hist1 = create_rgb_hist(img)
    histGrayImage = cv2.calcHist([img], [1], None, [256], [0, 256])
    cv2.normalize(histGrayImage, histGrayImage,0,255*0.9,cv2.NORM_MINMAX)
    rmfiles.append(f)
    rmfile.append(f)
    for j, f2 in enumerate(files[i+1:]):
            f2 = f2.replace('\n','')
            img2 = cv2.imread(f2)
            # hist2 = create_rgb_hist(img2)
            histGrayImage2 = cv2.calcHist([img2], [1], None, [256], [0, 256])
            cv2.normalize(histGrayImage2, histGrayImage2,0,255*0.9,cv2.NORM_MINMAX)

            dist = cv2.compareHist(histGrayImage, histGrayImage2, cv2.HISTCMP_CORREL)
            # dist = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)


            print(dist)
            if(dist<0.93):
                a = random.randint(0, rmfile.__len__()-1)
                # a = np.random.randint(0, rmfile.__len__(),1)[0]
                # print("fdsafasfasfd------------:   "+str(a))
                shutil.copy(rmfile[a],savepath+rmfile[a].split('/')[-1])
                # cv2.imwrite(savepath+f,img)
                break
            else:
                rmfiles.append(f2)
                rmfile.append(f2)

                # cv2.namedWindow("image1",cv2.WINDOW_NORMAL)
                # cv2.namedWindow("image2",cv2.WINDOW_NORMAL)
                # cv2.imshow("image1",img)
                # cv2.imshow("image2",img2)
                # cv2.waitKey()
