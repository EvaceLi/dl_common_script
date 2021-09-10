# -*- coding:utf-8 -*-
#生成xml文件
import xml.dom.minidom

class generateXml:
    def __init__(self, label_info, dets_final, im_name, size,xmlname):
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
        nodewidth.appendChild(doc.createTextNode(str(size[1])))
        nodeheight = doc.createElement('height')
        nodeheight.appendChild(doc.createTextNode(str(size[0])))
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
        for i in xrange(len(box)):
            nodeobject = doc.createElement('object')
            nodename = doc.createElement('name')
            nodename.appendChild(doc.createTextNode(label[i]))
            nodepose = doc.createElement('pose')
            nodepose.appendChild(doc.createTextNode('Unspecified'))
            nodetruncated = doc.createElement('truncated')
            nodetruncated.appendChild(doc.createTextNode('0'))
            nodedifficult = doc.createElement('difficult')
            nodedifficult.appendChild(doc.createTextNode('0'))
            nodebndbox = doc.createElement('bndbox')

            nodexmin = doc.createElement('xmin')
            nodexmin.appendChild(doc.createTextNode(str(int(float(box[i][0])))))
            nodeymin = doc.createElement('ymin')
            nodeymin.appendChild(doc.createTextNode(str(int(float(box[i][1])))))
            nodexmax = doc.createElement('xmax')
            nodexmax.appendChild(doc.createTextNode(str(int(float(box[i][2])))))
            nodeymax = doc.createElement('ymax')
            nodeymax.appendChild(doc.createTextNode(str(int(float(box[i][3])))))
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
