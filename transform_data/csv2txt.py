
#csv转为txt
import pandas as pd

csv_path = '/data/openImg-data-statistics/segmentation/validation-annotations-object-segmentation.csv'
data = pd.read_csv(csv_path)
with open('/data/openImg-data-statistics/segmentation/validation-annotations-object-segmentation.txt', 'a+') as f:
    for line in data.values:
        f.write((str(line[0])+' '+str(line[1])+' '+
                 str(line[2])+' '+str(line[3])+'\n'))
        # f.write((str(line[0])+' '+str(line[1])+'\n'))
