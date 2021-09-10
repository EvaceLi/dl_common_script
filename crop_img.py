#裁剪图像
import os
import cv2

path='20210208_data/frontdoor/'
savepath='20210208_data/frontdoor_crop/'
os.makedirs(savepath,exist_ok=True)
files = os.listdir(path)

for file in files:
    print(file)
    img = cv2.imread(path+file)
    #img = img[:,120:840,:]
    img = img[:,160:1120,:]
    cv2.imwrite(savepath+file,img)
