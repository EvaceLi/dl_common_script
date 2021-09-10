
#csv转为txt
import pandas as pd

csv_path = '/segmentation.csv'
data = pd.read_csv(csv_path)
with open('/segmentation.txt', 'a+') as f:
    for line in data.values:
        f.write((str(line[0])+' '+str(line[1])+' '+
                 str(line[2])+' '+str(line[3])+'\n'))
        # f.write((str(line[0])+' '+str(line[1])+'\n'))
