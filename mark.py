 

from albertk import *
import pymongo
# import warnings
# warnings.filterwarnings("ignore", category = ConvergenceWarning)
import tkitTextClassification as tkitclass

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



model,tokenizer=load_albert("model/albert_tiny")
client = pymongo.MongoClient("localhost", 27017)
DB = client.gpt2Write
print(DB.name)
RDB = client.text_relation
def run():
    
    AutoTNum=input("每标记多少次训练一次（默认50）：")
    if AutoTNum:
        pass
    else:
        AutoTNum=50
        pass
    tt=tkitText.Text()
    text_list=[]
    n=0
    for i,one_it in enumerate(DB.entity_kg_rank.aggregate([{ '$sample': { 'size': 10000 }}  ]) ):
        # print(one_it)
        if one_it['rank']>3:
            
            try:
                mjson=tkitFile.Json("data/marked.json")
                c_list=read_labels()
                marked_text,marked_label=bulid_t_data(mjson)
            except:
                pass

            try:
                new_text_list=[]
                print("AutoTNum:",AutoTNum)
                if n%int(AutoTNum)==0:
                    print("#####进行自动训练######")
                    label_spread=auto_train_model(new_text_list,marked_text,marked_label,tokenizer,model,n_neighbors=len(c_list))
                pass
            except:
                pass
            keyword=one_it['entity']+" "+one_it['value']
            try:
                mark_one(keyword,label_spread)
            except :
                pass
            n=n+1
        
def mark_one(keyword,label_spread):
    tkitFile.File().mkdir("data")
    mjson=tkitFile.Json("data/marked.json")
    # print(text_list)
    c_list=read_labels()
    data=[]
    klist=run_search_sent(keyword,tokenizer,model,3)
    text_list=[]
    for k in klist.keys():
        text_list=text_list+klist[k]



    for it in  text_list[:2]:
        print("##"*29)
        pprint.pprint(c_list)
        print("句子A：",keyword)
        print("句子B：",it)

        new_text_list=[it]

        # print(new_text_list,marked_text,marked_label)
        # exit()

        try:
            # pre=auto_train(new_text_list,marked_text,marked_label,tokenizer,model,n_neighbors=len(c_list))

            pre=auto_predict(new_text_list,label_spread,tokenizer,model)

            # print("预测：",pre)
            for i,p in enumerate( pre):
                # print(type(p))
                # print("句子：",new_text_list[i])
                
                try:
                    print("\n\n预测结果（默认）:",p,c_list[str(p)])
                    # print("预测结果:",p,c_list[int(p)])
                except:
                    pass
        except:
            pass
        if tc_:
            print("Bert预测：",tc.pre(keyword,it))
        c = input("输入对应标签(新建输入n):")
        if c=="n":
                n= input("输入新建标签:")
                c_list[len(c_list)]=n
                save_labels(c_list)
                one={"label":len(c_list)-1,'sentence':keyword+" [SEP] "+it,'sentence1':keyword,'sentence2':it}
                print(one)
                mjson.save([one]) 
        else:
            try:

                if c_list.get(str(c)):
                    one={"label":int(c),'sentence':keyword+" [SEP] "+it,'sentence1':keyword,'sentence2':it}
                    print(one)
                    mjson.save([one])

            except:
                pass




# while True:
#     print("###"*20)

run()