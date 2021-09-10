#对比两个文件夹中，找出不同名字的图片。输出在out文件夹中
# 主要用法：标注公司返回来的数据，可能一个图片标注多个xml文件，导致根据ｘｍｌ索引图片名字，训练就会出错，所以在训练之前就找到这些图片
import os
import shutil
path1 = './img_path1'
path2 = './img_path2'
out = './out'
def main():
    os.makedirs(out, exist_ok=True)
    files1_original = [names.split('.jpg')[0] for names in os.listdir(path1)]
    files2_original = [names.split('.jpg')[0] for names in os.listdir(path2)]

    out1 = []
    out2 = []
    for names1 in files1_original:
        if names1 not in files2_original:
            out1.append(names1)
            with open(os.path.join(out, 'out.txt'), 'a') as fd:
                fd.write(names1 + '\n')

    for names2 in files2_original:
        if names2 not in files1_original:
            out2.append(names2)
            with open(os.path.join(out, 'out.txt'), 'a') as fd:
                fd.write(names2 + '\n')
    for i in out1:
        shutil.move(os.path.join(path1, i+'.jpg'), out)
    for i in out2:
        shutil.move(os.path.join(path2, i+'.jpg'), out)

if __name__=="__main__":
    main()