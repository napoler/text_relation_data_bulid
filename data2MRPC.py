# from tkitText import *
import  hashlib
import csv
import tkitFile
"""
保存数据MRPC格式

"""

def md5(string):
    # 对要加密的字符串进行指定编码
    string = string.encode(encoding ='UTF-8')
    # md5加密
    # print(hashlib.md5(string))
    # 将md5 加密结果转字符串显示
    string = hashlib.md5(string).hexdigest()
    # print(string)
    return string
def w2tsv(data,name):
    with open(name, 'wt') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        # Quality	#1 ID	#2 ID	#1 String	#2 String
        tsv_writer.writerow(['Quality', '#1 ID','#2 ID','#1 String','#2 String'])
        for it in data:
            tsv_writer.writerow(it)
        # tsv_writer.writerow(['Shelah', 'Math'])
        # tsv_writer.writerow(['Aumann', 'Economic Sciences'])
        
# file_list=["test.txt","dev.txt","train.txt"]
mjson=tkitFile.Json("data/marked.json")
# for file_neme in mjson.auto_load():

data=mjson.load()
# with open(file_neme, "r") as f:
data=[]
for it in  mjson.auto_load():
    one=[it['label'],md5(it['sentence1']),md5(it['sentence2']),it['sentence1'],it['sentence2']]
    data.append(one)

# 这里保存数据MRPC格式
c=int(len(data)*0.1)
d=int(len(data)*0.2)
w2tsv(data[0:c],"data/test.tsv")
w2tsv(data[c:d],"data/dev.tsv")
w2tsv(data[d:len(data)],"data/train.tsv")
        


