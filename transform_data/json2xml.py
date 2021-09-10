#json转xml文件
import json
import os
from collections import defaultdict, OrderedDict
import xml.etree.ElementTree as ET
from xml.dom.minidom import Document

labelpath = 'save.txt'
savepath = 'save_xml/'
basePath = 'select2/'
filefinames = open(labelpath,'r').readlines()
filefinames = [file.replace('\n','') for file in filefinames]

# classType = ['vehicle']
classType = ['traffic_cones','vehicle']

def convert_xml(lables,bboxs,name, Child_folderName):
    doc = Document()
    # boot
    root = doc.createElement('annotation')
    doc.appendChild(root)

    nodeName = doc.createElement('filename')
    root.appendChild(nodeName)
    nodeName.appendChild(doc.createTextNode(name + ".jpg"))

    nodeFlder = doc.createElement('folder')
    root.appendChild(nodeFlder)
    nodeFlder.appendChild(doc.createTextNode("cidi_data"))
    hig, wid, dep = [1020,1920,3]
    for l, label in enumerate(lables):
        nodeObject = doc.createElement('object')
        root.appendChild(nodeObject)
        Name = doc.createElement('name')
        nodeObject.appendChild(Name)
        Name.appendChild(doc.createTextNode(label))
        # Name.appendChild(doc.createTextNode("up_person"))
        Bndbox = doc.createElement('bndbox')
        nodeObject.appendChild(Bndbox)

        Xmax = doc.createElement('xmin')
        Bndbox.appendChild(Xmax)
        line = bboxs[l]
        x1 = line[0]
        y1 = line[1]
        x2 = line[0]+line[2]
        y2 = line[1]+line[3]

        Xmax.appendChild(doc.createTextNode(str(int(x1))))
        Xmin = doc.createElement('ymin')
        Xmin.appendChild(doc.createTextNode(str(int(y1))))
        Bndbox.appendChild(Xmin)
        Ymax = doc.createElement('xmax')
        Ymax.appendChild(doc.createTextNode(str(int(x2))))
        Bndbox.appendChild(Ymax)
        Ymin = doc.createElement('ymax')
        Ymin.appendChild(doc.createTextNode(str(int(y2))))
        Bndbox.appendChild(Ymin)

        Difficult = doc.createElement('difficult')
        Difficult.appendChild(doc.createTextNode("0"))
        nodeObject.appendChild(Difficult)

    nodeSize = doc.createElement('size')
    root.appendChild(nodeSize)
    Depth = doc.createElement('depth')
    nodeSize.appendChild(Depth)
    Depth.appendChild(doc.createTextNode(str(int(dep))))
    Height = doc.createElement('height')
    nodeSize.appendChild(Height)
    Height.appendChild(doc.createTextNode(str(int(hig))))
    Width = doc.createElement('width')
    nodeSize.appendChild(Width)
    Width.appendChild(doc.createTextNode(str(int(wid))))

    nodeSource = doc.createElement('source')
    Annotation = doc.createElement('annotation')
    nodeSource.appendChild(Annotation)
    Database = doc.createElement('database')
    nodeSource.appendChild(Database)
    Database.appendChild(doc.createTextNode("CIDI"))

    Image = doc.createElement('image')
    nodeSource.appendChild(Image)
    Image.appendChild(doc.createTextNode("flickr"))
    # f.close()
    fp = open(basePath+savepath + Child_folderName + '/' + name+ ".xml", 'w')
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
    fp.close()

cout = 0
for path in filefinames:
    fp = open(os.path.join(basePath,path))
    Child_folderName = path.split('/')[2]
    if not os.path.exists(os.path.join(basePath , savepath + Child_folderName)):
        os.makedirs(os.path.join(basePath , savepath + Child_folderName))
    print(os.path.join(basePath,path))
    file = json.load(fp)
    objects = file['objects']
    labels = []
    bboxs = []
    for i, obj in enumerate(objects):
        if(obj['label'] not in classType):
            continue
        labels.append(obj['label'])
        bboxs.append(obj['bbox'])
        cout += 1
        print(cout)
    convert_xml(labels,bboxs,path.split('/')[-1].split('.')[0], Child_folderName)



        







