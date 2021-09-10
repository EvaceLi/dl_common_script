# coding=utf-8
import xml.etree.ElementTree as ET
import os
import json
#ｘｍｌ转ｊson文件

voc_clses = ['head',]


categories = []
for iind, cat in enumerate(voc_clses):
    cate = {}
    cate['supercategory'] = cat
    cate['name'] = cat
    cate['id'] = iind+1
    categories.append(cate)

def getimages(xmlname, id):
    sig_xml_box = []
    tree = ET.parse(xmlname)
    root = tree.getroot()
    images = {}
    for i in root:  # 遍历一级节点
        if i.tag == 'filename':
            file_name = i.text  # 0001.jpg
            # print('image name: ', file_name)
            # images['file_name'] = file_name
            images['file_name'] = xmlname.split("/")[-1].replace('.xml',".jpg")
        if i.tag == 'size':
            for j in i:
                if j.tag == 'width':
                    width = j.text
                    images['width'] = int(width)
                if j.tag == 'height':
                    height = j.text
                    images['height'] = int(height)
        if i.tag == 'object':
            for j in i:
                if j.tag == 'name':
                    cls_name = j.text
                cat_id = voc_clses.index(cls_name)+1
                #cat_id = voc_clses.index(cls_name)
                if j.tag == 'bndbox':
                    bbox = []
                    xmin = 0
                    ymin = 0
                    xmax = 0
                    ymax = 0
                    for r in j:
                        if r.tag == 'xmin':
                            xmin = eval(r.text)
                        if r.tag == 'ymin':
                            ymin = eval(r.text)
                        if r.tag == 'xmax':
                            xmax = eval(r.text)
                        if r.tag == 'ymax':
                            ymax = eval(r.text)
                    # print(xmlname)
                    if(xmax<=xmin or ymax<=ymin):
                        print('xmax<=xmin or ymax<=yminn'+xmlname)
                        continue
                    if((xmax - xmin)<=5 or (ymax - ymin)<=5):
                        print('w and h <5'+xmlname)
                        continue
                    assert(xmax >=0)
                    assert(ymax >=0)
                    assert(xmin>=0)
                    assert(ymin>=0)
                    ratios = (xmax-xmin)/(ymax-ymin)
                    # if (ratios>3 or ratios<0.333):
                    #     print('ratios'+xmlname)
                    #     continue
                    if(ratios>3 and (abs(xmin-0)<5 or abs(960-xmax)<5 or abs(ymin-0)<5 or abs(720-ymax)<5 )):
                        print('ratios'+xmlname)
                        continue
                    if(ratios<0.333 and (abs(xmin-0)<5 or abs(960-xmax)<5 or abs(ymin-0)<5 or abs(720-ymax)<5 )):
                        print('ratios'+xmlname)
                        continue
                    bbox.append(xmin)
                    bbox.append(ymin)
                    bbox.append(xmax - xmin)
                    bbox.append(ymax - ymin)
                    bbox.append(id)   # 保存当前box对应的image_id
                    bbox.append(cat_id)
                    # anno area
                    bbox.append((xmax - xmin) * (ymax - ymin) - 5.0)   # bbox的ares
                    # coco中的ares数值是 < w*h 的, 因为它其实是按segmentation的面积算的,所以我-5.0一下...
                    sig_xml_box.append(bbox)
                    # print('bbox', xmin, ymin, xmax - xmin, ymax - ymin, 'id', id, 'cls_id', cat_id)
    images['id'] = id
    # print ('sig_img_box', sig_xml_box)
    return images, sig_xml_box



def txt2list(txtfile):
    f = open(txtfile)
    l = []
    for line in f:
        l.append(line[:-1])
    return l


# voc2007xmls = 'anns'
voc2007xmls = '/home/cidi-gpu/disk/data1/datasets/headCount/HeadData/VOC/VOC2012_head/Annotations'
# test_txt = 'voc2007/test.txt'
test_txt = '/home/cidi-gpu/disk/data1/datasets/headCount/HeadData/VOC/VOC2012_head/ImageSets/Main/test.txt'
xml_names = txt2list(test_txt)
xmls = []
bboxes = []
ann_js = {}
for ind, xml_name in enumerate(xml_names):
    # print(xml_name)
    xmls.append(os.path.join(voc2007xmls, xml_name + '.xml'))
json_name = '/home/cidi-gpu/disk/data1/datasets/headCount/HeadData/COCO/COCO_head/annotations/instances_val2017.json'
images = []
for i_index, xml_file in enumerate(xmls):
    image, sig_xml_bbox = getimages(xml_file, i_index)
    images.append(image)
    bboxes.extend(sig_xml_bbox)
ann_js['images'] = images
ann_js['categories'] = categories
annotations = []
for box_ind, box in enumerate(bboxes):
    anno = {}
    anno['image_id'] =  box[-3]
    anno['category_id'] = box[-2]
    anno['bbox'] = box[:-3]
    anno['id'] = box_ind
    anno['area'] = box[-1]
    anno['iscrowd'] = 0
    annotations.append(anno)
ann_js['annotations'] = annotations
json.dump(ann_js, open(json_name, 'w'), indent=4)  # indent=4 更加美观显示
