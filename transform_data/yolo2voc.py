#将yolo（txt）规定的数据格式转换为ＶＯＣ数据格式
import os
import shutil
import cv2

yolo_txt_path = "960_yolo/val.txt'
VOC_base_path = '/VOC/VOC2012_head'
img_save_path = VOC_base_path+'/JPEGImages'
xml_save_path = VOC_base_path+'/Annotations'
txt_save_path = VOC_base_path+'/labels'
image_sets = VOC_base_path +"/ImageSets/Main"
def main():
    os.makedirs(img_save_path, exist_ok=True)
    os.makedirs(xml_save_path, exist_ok=True)
    os.makedirs(image_sets, exist_ok=True)
    os.makedirs(txt_save_path, exist_ok=True)
    yolo_txt_file = open(yolo_txt_path, 'r')
    file = yolo_txt_file.readlines()
    all_number = len(file)
    i = 0
    fd = open(image_sets+'/test.txt', 'w+')
    yolofd = open(image_sets+'/test_yolov4.txt', 'w+')
    exist_number= 0
    for img_lines in file:
        print('INFO:'+str(i)+'/'+str(all_number))
        img_line = img_lines.strip()
        
        xml_line = img_line.replace('.jpg','.xml').replace('JPGE','labels').replace('validation', 'validation_xml')
        txt_line = img_line.replace('.jpg','.txt').replace('JPGE','labels')
        img_name = img_line.split("/")[-1]

        if os.path.exists(os.path.join(img_save_path, img_name)):
            exist_number = exist_number+1
            print(img_name)
            i+=1
            continue

        shutil.copy(img_line, os.path.join(img_save_path, img_name))
        if os.path.exists(xml_line):
            shutil.copy(xml_line, os.path.join(xml_save_path, img_name.replace('.jpg', '.xml')))
        if os.path.exists(txt_line):
            shutil.copy(txt_line, os.path.join(txt_save_path, img_name.replace('.jpg', '.txt')))
        img_id = img_name.strip('.jpg')
        fd.write(img_id+'\n')
        yolofd.write(os.path.join(img_save_path, img_name)+'\n')
        i+=1
    print(exist_number)
if __name__ == "__main__":
    main()

