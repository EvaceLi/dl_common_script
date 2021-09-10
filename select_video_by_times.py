#通过视频名字来找到具体时间段的视频
import argparse,os
from tqdm import tqdm
import random

def getallfile(path, allfile):
    allfilelist=os.listdir(path)
    for file in allfilelist:
        filepath=os.path.join(path,file)
        if os.path.isdir(filepath):
            getallfile(filepath, allfile)
        allfile.append(filepath)
    return allfile

def parse_day_and_night(index, file, day_index, night_index, day_start, day_end):
    name = os.path.basename(file)
    time = int(name[8:12])
    if time >= day_start and time <= day_end:
        day_index.append(index)
    else:
        night_index.append(index)

def filter(args):
    origin_files = []
    getallfile(args.video_dir, origin_files)
    pass_files = [l.rstrip("\n") for l in open(args.pass_path)]
    pass_files = set(pass_files)
    files = [f for f in origin_files if f not in pass_files]

    day_start = int(args.day_time[0:4])
    day_end = int(args.day_time[5:9])

    day_index,night_index = [],[]
    day_files,night_files = [],[]
    print('INFO: parse files on {}'.format(args.video_dir))
    for i, file in tqdm(enumerate(files)):
        parse_day_and_night(i, file, day_index, night_index, day_start, day_end)
    if len(day_index) > args.day_num:
        day_index = set(random.sample(day_index, args.day_num))
    for i, f in enumerate(files):
        if i in day_index:
            day_files.append(f)
    
    if len(night_index) > args.night_num:
        night_index = set(random.sample(night_index, args.night_num))
    for i, f in enumerate(files):
        if i in night_index:
            night_files.append(f)

    print('INFO: day num:{},night num:{}'.format(len(day_files), len(night_files)))

    print('INFO: write filelists')
    with open(args.save_path, 'w') as f:
        for file in day_files:
            f.write('{}\n'.format(file))
        for file in night_files:
            f.write('{}\n'.format(file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_dir', default='/41306_cs', type=str, help='video dir')
    parser.add_argument('--day_num', default=130, type=int, help='day num')
    parser.add_argument('--night_num', default=0, type=int, help='day num')
    parser.add_argument('--day_time', default='0600-1900', type=str, help='day_time')
    parser.add_argument('--pass_path', default='41306_cs_select.txt', type=str, help='pass filelists txt path')
    parser.add_argument('--save_path', default='41306_cs_select1.txt', type=str, help='save filelists txt path')
    args = parser.parse_args()
    
    filter(args)
    
