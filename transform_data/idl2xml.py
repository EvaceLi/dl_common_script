#idl文件转xml
import os

# -*- coding:utf-8 -*-
import xml.dom.minidom

class generateXml:
    def __init__(self, label_info, dets_final, im_name, size, xmlname):
        self.label_info = label_info
        self.dets_final = dets_final
        self.im_name = im_name
        self.size = size
        self.xmlname = xmlname

    def generate(self):
        label = self.label_info
        box = self.dets_final
        name = self.im_name
        size = self.size
        doc = xml.dom.minidom.Document()
        root = doc.createElement('annotation')
        doc.appendChild(root)

        nodefolder = doc.createElement('folder')
        nodefolder.appendChild(doc.createTextNode('test-file'))

        nodefilename = doc.createElement('filename')
        nodefilename.appendChild(doc.createTextNode(name.split('.')[0]))

        nodepath = doc.createElement('path')
        nodepath.appendChild(doc.createTextNode('/home/qi/Desktop/'))

        nodesource = doc.createElement('source')
        nodedatabase = doc.createElement('database')
        nodedatabase.appendChild(doc.createTextNode('Unknow'))
        nodesource.appendChild(nodedatabase)


        nodesize = doc.createElement('size')
        nodewidth = doc.createElement('width')
        nodewidth.appendChild(doc.createTextNode(str(size[0])))
        nodeheight = doc.createElement('height')
        nodeheight.appendChild(doc.createTextNode(str(size[1])))
        nodedepth = doc.createElement('depth')
        nodedepth.appendChild(doc.createTextNode(str(size[2])))
        nodesize.appendChild(nodewidth)
        nodesize.appendChild(nodeheight)
        nodesize.appendChild(nodedepth)

        nodesegmented = doc.createElement('segmented')
        nodesegmented.appendChild(doc.createTextNode('0'))
        root.appendChild(nodefolder)
        root.appendChild(nodefilename)
        root.appendChild(nodepath)
        root.appendChild(nodesource)
        root.appendChild(nodesize)
        root.appendChild(nodesegmented)

        # cls = 'police'
        for i in range(len(box)):
            gt = box[i].split(' ')[1:]
            if len(gt)>0:
                nodeobject = doc.createElement('object')
                nodename = doc.createElement('name')
                nodename.appendChild(doc.createTextNode(label))
                nodepose = doc.createElement('pose')
                nodepose.appendChild(doc.createTextNode('Unspecified'))
                nodetruncated = doc.createElement('truncated')
                nodetruncated.appendChild(doc.createTextNode('0'))
                nodedifficult = doc.createElement('difficult')
                nodedifficult.appendChild(doc.createTextNode('0'))
                nodebndbox = doc.createElement('bndbox')

                nodexmin = doc.createElement('xmin')
                nodexmin.appendChild(doc.createTextNode(str(int(float(gt[0])))))
                nodeymin = doc.createElement('ymin')
                nodeymin.appendChild(doc.createTextNode(str(int(float(gt[1])))))
                nodexmax = doc.createElement('xmax')
                nodexmax.appendChild(doc.createTextNode(str(int(float(gt[2])))))
                nodeymax = doc.createElement('ymax')
                nodeymax.appendChild(doc.createTextNode(str(int(float(gt[3])))))
                nodebndbox.appendChild(nodexmin)
                nodebndbox.appendChild(nodeymin)
                nodebndbox.appendChild(nodexmax)
                nodebndbox.appendChild(nodeymax)

                nodeobject.appendChild(nodename)
                nodeobject.appendChild(nodepose)
                nodeobject.appendChild(nodetruncated)
                nodeobject.appendChild(nodedifficult)
                nodeobject.appendChild(nodebndbox)


                root.appendChild(nodeobject)


        fp = open(self.xmlname +'/'+ name.split('.')[0] + '.xml', 'w')
        doc.writexml(fp, addindent='\t', newl='\n', encoding="utf-8")
        fp.close()

idl_file_dir = "/home/cidi-gpu/disk/data1/liyi/head_counts_dataset/brainwash/brainwash_train.idl"
xml_files_dir = "train_xml_files"

if not os.path.exists(xml_files_dir):
    os.mkdir(xml_files_dir)
f1 = open(idl_file_dir, 'r+')
lines = f1.readlines()
print(len(lines))
for i in range(len(lines)):
    line = lines[i]
    line = line.replace(":", ";")
    # print(line)
    img_dir = line.split(";")[0]
    # print(img_dir)
    img_boxs = line.split(";")[1]
    img_dir = img_dir.replace('"', "")
    img_dir1 = img_dir.replace('/', '_')
    # print(img_dir)
    img_name = img_dir.split("/")[1]
    txt_name = img_name.split(".")[0]
    img_extension = img_name.split(".")[1]
    # print(txt_name)
    # print(img_extension)
    img_boxs = img_boxs.replace(",", "")
    # print(img_boxs)
    img_boxs = img_boxs.replace("(", "")
    img_boxs = img_boxs.split(")")
    label_info = 'head'
    size = list(map(int, txt_name.split('_')[1].split('x') + ['3']))
    out = generateXml(label_info, img_boxs, img_dir1, size, xml_files_dir)
    out.generate()

