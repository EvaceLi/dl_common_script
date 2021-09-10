#mat类型的读取
import scipy.io as scio


datapath = '/home/cidi-gpu/disk/data1/liyi/head_counts_dataset/Beijing-BRT-dataset-master/test/ground_truth/1-20160620091221.mat'

data = scio.loadmat(datapath)
print(data.keys())
print(data['loc'])