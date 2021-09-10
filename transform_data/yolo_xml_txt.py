#将xml数据，转换为yolo的数据格式
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import cv2

sets = [('vehicle')]
classes = ["vehicle"]

path = '/val/'


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id):
    if(os.path.exists(path+'Annotations/%s.xml' %(image_id))):
        print(path+'Annotations/%s.xml' %(image_id))
        in_file = open(path+'Annotations/%s.xml' %(image_id))
        out_file = open(path+'labels/%s.txt' %(image_id), 'w')
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        # h,w,_ = cv2.imread(path+'JPEGImages/'+image_id+'.jpg').shape
        w1 = int(size.find('width').text)
        h1 = int(size.find('height').text)

        for obj in root.iter('object'):
            # difficult = obj.find('difficult').text
            cls = obj.find('name').text
            print(cls)
            if cls not in classes:  # or int(difficult)==1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            # b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
            #      float(xmlbox.find('ymax').text))
            # bb = convert((w, h), b)
            bb = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text),
                int(xmlbox.find('ymax').text))

            out_file.write(cls + " " + " ".join([str(a) for a in bb]) + '\n')
        out_file.close()
    else:
        out_file = open(path+'labels/%s.txt' %(image_id), 'w')
        out_file.close()


wd = getcwd()
for image_set in sets:
    if not os.path.exists(path+'labels/'):
        os.makedirs(path+'labels/')
    image_ids = open(path+'val.txt').readlines()
    for image_id in image_ids:
        # list_file.write(path+'JPEGImages/%s.jpg\n' % (image_id))
        # print(image_id)
        image_id = image_id.replace('\n','')
        convert_annotation(image_id)
