from os import getcwd
from sklearn.model_selection import train_test_split
import json
import glob
wd = getcwd()
"labelme标注的json 数据集转为keras 版yolov3的训练集"
classes = ["aircraft","oiltank"]

image_ids = glob.glob(r"LabelmeData/*jpg")
print(image_ids)
train_list_file = open('data/train.txt', 'w')
val_list_file = open('data/val.txt', 'w')
def convert_annotation(image_id, list_file):
    jsonfile=open('%s.json' % (image_id))
    in_file = json.load(jsonfile)

    for i in range(0,len(in_file["shapes"])):
        object=in_file["shapes"][i]
        cls=object["label"]
        points=object["points"]
        xmin=int(points[0][0])
        ymin=int(points[0][1])
        xmax=int(points[1][0])
        ymax=int(points[1][1])
        if cls not in classes:
            print("cls not in classes")
            continue
        cls_id = classes.index(cls)
        b = (xmin, ymin, xmax, ymax)
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
    jsonfile.close()

def ChangeData2TXT(image_List,dataFile):
    for image_id in image_List:
        dataFile.write('%s' % (image_id.split('\\')[-1]))
        convert_annotation(image_id.split('.')[0], dataFile)
        dataFile.write('\n')
    dataFile.close()


trainval_files, test_files = train_test_split(image_ids, test_size=0.2, random_state=55)
ChangeData2TXT(trainval_files,train_list_file)
ChangeData2TXT(test_files,val_list_file)


