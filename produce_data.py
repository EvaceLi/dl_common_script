#生成yml数据，将模型的输入与输出写入yml，用于进行部署的时候验证TensorRT结果是否对。
#前面的代码
from util.utils import *
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import torch
import time
from util.prune_utils import *
import argparse
from util.parse_config import *
# from utils_junjie import tools, timer
from utils_junjie.utils import *
from utils_junjie.visualization import *
from utils_junjie.get_module_list import *
from PIL import Image
import cv2
from collections import OrderedDict

parser = argparse.ArgumentParser(description="demo for rotated image detection")
parser.add_argument('--model_name', type=str, default='rapid',
                    help='the name of model')
parser.add_argument('--model_def', type=str, default='cfg/prune_0.9_prune_rotate_detection_darknet53_256.cfg')
parser.add_argument('--model', type=str, default='weights/rapid_pL1_dark53_Jan05-15_0.9_1_339000.pth',
                    help='model path')
parser.add_argument('--img_path', type=str, default='test/43264/JPEGImages',
                    help='image path')
parser.add_argument('--input_size', type=int, default=(256, 512))
parser.add_argument('--conf_thres', type=float, default=0.5)
parser.add_argument('--visualize', type=bool, default=True)
parser.add_argument('--preprocess_type', type=str, default='cv2', choices=['cv2', 'torch'],
                        help='image preprocess type')
args = parser.parse_args()

module_defs = parse_model_config(args.model_def)
# module_defs.pop(0)
model = RotateDetectNet(module_defs)
pretrained_dict = torch.load(args.model)
model.load_state_dict(pretrained_dict['model'])
for parameter in model.parameters():
    parameter.requires_grad = False
model.eval()
fs = cv2.FileStorage("/data/TrtInfer/samples/testcases0.ymal",cv2.FileStorage_WRITE)
fs.write("testcase_num",5)
for number in range(5):
    # input = torch.randn(2,3,256,512)
    input_shape = (args.input_size[0], args.input_size[1],3)
    input = torch.randn(4, *input_shape)
    output = model(input)
    fs.write("testcase_input"+str(number),input.cpu().numpy())
    for i in range(len(output)):
        fs.write("testcase_output"+str(number)+"_"+str(i),output[i].detach().numpy())