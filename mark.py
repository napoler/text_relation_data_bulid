 

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
    for i,one_it in enumerate(DB.entity_kg_rank.aggregate([{ '$sample': { 'size': 50000 }}  ]) ):
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
            c_keyword="\033[91m"+one_it['entity']+"\033[00m"+one_it['value']
            try:
                mark_one(keyword,c_keyword,label_spread)
            except :
                pass
            n=n+1
        
def mark_one(keyword,c_keyword,label_spread):
    tkitFile.File().mkdir("data")
    mjson=tkitFile.Json("data/marked.json")
    # print(text_list)
    c_list=read_labels()
    data=[]
    # klist=run_search_sent(keyword,tokenizer,model,3)
    klist=search_sent_plus(keyword)
    text_list=[]
    for k in klist:
        # text_list=text_list+klist[k]
        myit =k.meta.to_dict()
        # print("it",it)
        # print(k)
        # exit()

        
        highlight=myit['highlight']['content'][0].replace("<em>","\033[32m").replace("</em>","\033[00m")
        text_list.append({"content":k.content,"highlight":highlight})


    # print("text_list",text_list)
    for it in  text_list[:2]:
        print("##"*29)
        pprint.pprint(c_list)
        print("句子A：",c_keyword)
        print("句子B：",it['highlight'])
        # print("句子B：",it['content'])

        new_text_list=[it['content']]

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
                    print("\n\n预测结果:",p,c_list[str(p)])
                    # print("预测结果:",p,c_list[int(p)])
                except:
                    pass
        except:
            pass
        if tc_:
            p=tc.pre(keyword,it['content'])
            print("Bert预测：",p)
        print("Ai推荐（默认）：\033[31m",p,"\033[00m")
        #只判断预测为1数据
        # if p==0:
        #     print("跳过！")
        #     continue

        c = input("\n输入对应标签(新建输入n):")
        # 新建标签操作
        if c=="n":
                n= input("输入新建标签:")
                c_list[len(c_list)]=n
                save_labels(c_list)
                one={"label":len(c_list)-1,'sentence':keyword+" [SEP] "+it['content'],'sentence1':keyword,'sentence2':it['content']}
                print(one)
                mjson.save([one]) 
        else:
            # 保存输入的数据
            try:

                if c_list.get(str(c)):
                    print("输入结果：")
                    one={"label":int(c),'sentence':keyword+" [SEP] "+it['content'],'sentence1':keyword,'sentence2':it['content']}
                    print(one)
                    mjson.save([one])
                elif c_list.get(str(p)):
                    print("采用预测结果：")
                    one={"label":int(p),'sentence':keyword+" [SEP] "+it['content'],'sentence1':keyword,'sentence2':it['content']}
                    print(one)
                    mjson.save([one])
                else:
                    print("跳过保存！")
                    pass
            except:
                pass




# while True:
#     print("###"*20)

run()