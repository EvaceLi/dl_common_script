#coding=utf-8
#主要用于分割ＶＯＣ类型的训练验证集，但是可进行小改动用来分离其他类型的训练集，比如label是json格式，其他数据格式
import  xml.dom.minidom
import os
import random
import shutil
import numpy as np
test_ratio = 0.2
jpg_path = '/Images/'
xml_path = '/Annotations/'
train_xml = '/train/Annotations'
val_xml = '/val/Annotations'
train_jpg = '/train/JPEGImages'
val_jpg = '/val/JPEGImages'
def main():
    files = os.listdir(xml_path)
    if not os.path.exists(train_xml):
        os.makedirs(train_xml)
    if not os.path.exists(val_xml):
        os.makedirs(val_xml)
    if not os.path.exists(train_jpg):
        os.makedirs(train_jpg)
    if not os.path.exists(val_jpg):
        os.makedirs(val_jpg)
    datas = []
    for name in files:

        dom = xml.dom.minidom.parse(os.path.join(xml_path, name))
        root = dom.documentElement
        #bb = root.getElementsByTagName('object')
        bb = root.getElementsByTagName('object/name')
        if len(bb)>0:
            print(bb)
            datas.append(name.split('.')[0])

    np.random.seed(42)
    shuffle_indices = np.random.permutation(len(datas))
    test_set_size = int(len(dataｓ))*test_ratio
    train_index = shuffle_indices[test_set_size:]
    val_index = shuffle_indices[:test_set_size]

    with open('val.txt', 'w') as fd:
        for id in val_index:
            if datas[id] + '.jpg' in os.listdir(jpg_path):
                fd.write(datas[id] + '\n')
                shutil.move(os.path.join(xml_path, datas[id]+'.xml'), val_xml)
                shutil.move(os.path.join(jpg_path, datas[id]+'.jpg'), val_jpg)
            else:
                print(datas[id])
    with open('train.txt', 'w') as fd:
        for id in train_index:
            if datas[id] + '.jpg' in os.listdir(jpg_path):
                fd.write(datas[id] + '\n')
                shutil.move(os.path.join(xml_path, datas[id]+'.xml'), train_xml)
                shutil.move(os.path.join(jpg_path, datas[id]+'.jpg'), train_jpg)
            else:
                print(datas[id])

if __name__ == "__main__":
    main()