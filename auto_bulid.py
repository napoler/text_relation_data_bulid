 

from albertk import *
import pymongo
# import warnings
# warnings.filterwarnings("ignore", category = ConvergenceWarning)
import tkitTextClassification as tkitclass
import tqdm
from tkitMarker_bert import Marker
Pred_Marker=Marker(model_path="./model/miaoshu/")
# pmodel,ptokenizer=Pred_Marker.load_model()
Pred_Marker.load_model()






"""
用于构建训练数据
"""
# 确认是否开启bert自动判断
tc_=True

if tc_:
    try:
        tc=tkitclass.TextClassification()
        tc.load("data/text-relation/")
        pass
    except expression as identifier:
        tc_=False
        pass

def add_kg_auto_marked(data):
    """
    添加标记过的数据

    data={
        entity:实体,
        description:描述,
        sentence:句子
    }
    """
    # a=data['sentence'].find(data['description'])
    # print(a)
    # a=data['sentence'].find(data['entity'])
    # print(a)
    tt= tkitText.Text()
    key=tt.md5(str(data))
    # 如果实体和描述都存在则进行保存
    if data['sentence'].find(data['description']) >=0 and data['sentence'].find(data['entity'])>=0:
        try:
            DB.entity_kg_auto_marked.insert_one({"_id":key,"entity":data['entity'],'description':data['description'],'sentence':data['sentence']}) 
            print(data)
            print("添加语料成功！")
        except :
            print("已经存在")
            pass
def set_var(key,value):
    """
    设置简单的参数
    
    """
    try:
        
        DB.var.insert_one({"_id":key,'value':value})
        print("已经更新：",key)
    except:
        DB.var.update({"_id":key},{'$set':{'value':value}})
        print('提交task失败')

def get_var(key):
    """
    获取简单的参数
    
    """
    data= DB.var.find_one({"_id":key})
    if data:
        return data.get('value')
    else:
        set_var(key,0)
        return 0
        pass
def get_all(task,rank=5):
    """
    遍历实体
    遍历task不为
    rank 大于
    """
    # tt= tkitText.Text()
    # data=[]

    for it in DB.entity_kg_rank.find({'rank':{'$gt':rank},'auto_marked_task':{'$ne':task}}):
        # 获取重复合并后的数据
        # 自动更新
        yield it
def set_task(key,task,name='auto_marked_task'):
    """
    更新提交进程
    
    """
    #  db.getCollection('entity_kg_rank1').update({"_id":"萨摩耶##体形：小型犬寿命：14-17岁"},{$set:{"rank":2}})
    try:
        DB.entity_kg_rank.update({"_id":key},{'$set':{name:task}})
        print("已经更新：",key)
    except:
        print('提交task失败')

def set_entity_kg_auto_marked_task(key,task,name='marked'):
    """
    更新提交进程
    
    """
    try:
        DB.entity_kg_auto_marked.update({"_id":key},{'$set':{name:task}})
        print("已经更新：",key)
    except:
        print('提交task失败')


# model,tokenizer=load_albert("model/albert_tiny")
client = pymongo.MongoClient("localhost", 27017)
DB = client.gpt2Write
print(DB.name)
# RDB = client.text_relation
def autorun():
    task=get_var("auto_marked_task")
    for it in get_all(task,rank=5):
        if DB.entity_kg_ner.find_one({"_id":it['entity'],"check":'5252sp'}):
            pass
        else:
            continue
        
        
        kw=it['entity']+it['value']
        for item in search_sent_plus(kw):
                # print(item)
                p=0
                if tc_:
                    try:
                        p=tc.pre(it['entity']+it['value'],item['content'])
                        pass
                    except:
                        pass
                # print(p)
                if p==1:
                # 保存筛选好的数据来作为训练数据
                    marked_data={
                        'entity':it['entity'],
                        'description':it['value'],
                        'sentence':item['content']
                    }
                    # print(marked_data)
                    add_kg_auto_marked(marked_data)


                    #进行启发式预测
                    print("Bert标记的知识：")
                    one=Pred_Marker.pre(it['entity'],item['content'])
                    print(one)
                    for kg in list(set(one)):
                        print(it['entity'],kg)
                        # 保存筛选好的数据来作为训练数据
                        marked_data={
                            'entity':it['entity'],
                            'description':kg,
                            'sentence':item['content']
                        }
                        # print(marked_data)
                        add_kg_auto_marked(marked_data)
        set_task(it['_id'],task)
    set_var("auto_marked_task",task+1)


def find_entity_kg_auto_marked(entity,description):
    """
    获取知识对应的所有标记
    
    """
    for it in DB.entity_kg_auto_marked.find({'entity':entity,"description":description,'marked':{'$ne':1}}):
        yield it
    

def run():
    print("开始手动标记")
    while True:
    # for it in DB.entity_kg_auto_marked.find_one({'marked':{'$ne':1}}):
        #筛选一条
        one=DB.entity_kg_auto_marked.find_one({'marked':{'$ne':1}})
        print("##"*10)
        print('知识：',"\033[31m",one['entity'],"\033[00m",one['description'])
        print('句子：',one['sentence'])
        c = input("输入（1or回车跳过）:")
        # 自动批处理对应的样本
        for it in tqdm.tqdm(find_entity_kg_auto_marked(one['entity'],one['description'])):
            # print(it)
            try:

                if int(c)==1:
                    set_entity_kg_auto_marked_task(it['_id'],1)
                    set_entity_kg_auto_marked_task(it['_id'],1,"grade") #设质量
                else:
                    set_entity_kg_auto_marked_task(it['_id'],1)
                    set_entity_kg_auto_marked_task(it['_id'],0,"grade")#设质量
                    print("跳过!")
            except:
                set_entity_kg_auto_marked_task(it['_id'],1)
                set_entity_kg_auto_marked_task(it['_id'],0,"grade")#设质量
                print("跳过!")

print("1,自动运行筛选")
print("2,手动筛选")
do = input("输入")
do=int(do)
if do==1:
    autorun()
elif do==2:
    
    run()
    pass