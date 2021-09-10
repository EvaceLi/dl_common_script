# dl_common_script

深度学习常用的脚本，比如公共数据集（Tusimple,VOC等）的转换，读取视频，分离训练验证集等。
计算机视觉领域搬砖人员一些常用的python工具，持续更新............
主要文件说明：
split_train_val.py：#主要用于分割ＶＯＣ类型的训练验证集，但是可进行小改动用来分离其他类型的训练集，比如label是json格式，其他数据格式
seg_video.py：#该脚本用来分割不同区域的视频，分割后形成两个视频。主要用途：有的时候由于远程传输数据需要压缩数据，所以是各个摄像头拼在一起的数据，故而需要分割
check_file_same.py：#对比两个文件夹中，找出不同名字的图片。输出在out文件夹中。主要用法：标注公司返回来的数据，可能一个图片标注多个xml文件，导致根据ｘｍｌ索引图片名字，训练就会出错，
所以在训练之前就找到这些图片
crop_img.py：裁剪图像
merge_img.py：将图像拼接起来，可视化
modify_xml.py：修改xml文件
produce_data.py：生成yml数据，将模型的输入与输出写入yml，用于进行部署的时候验证TensorRT结果是否对。
read_video.py：从视频取图像
select_difficult_sample.py：#找难样本。比如用一个小网络yolov3裁剪网络生成的结果（txt），大网络yolov4生成的结果作为ＧＴ，
找出那些YOlov4检测出来了，yolov3出错的图片，称之为难样本，用于训练提高效果；
select_img_from_video.py：从视频中获取图像。进行了一些筛选。
transform_data/yolo2voc.py:将yolo（txt）规定的数据格式转换为ＶＯＣ数据格式
transform_data/xml2json.py:ｘｍｌ转ｊson文件
transform_data/json2xml.py:json转xml文件
transform_data/generate_simple.py:将车道线标注数据转换为Tusimple数据集格式
transform_data/yolo2voc.py:将yolo（txt）规定的数据格式转换为ＶＯＣ数据格式
transform_data/yolo_xml_txt.py:将xml数据，转换为yolo的数据格式
/transform_data/csv2txt.py:csv转为txt
