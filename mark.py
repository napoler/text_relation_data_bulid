 

from albertk import *
import pymongo

model,tokenizer=load_albert("model/albert_tiny")
client = pymongo.MongoClient("localhost", 27017)
DB = client.gpt2Write
print(DB.name)
RDB = client.text_relation
def run():

    tt=tkitText.Text()
    text_list=[]

    # text=''
    # keyword = input("输入关键词:")
    # for it in search_sent(kw):

    #     # text=text+"。"+it.content
    #     if len(it.content)>5:
    #         text_list.append(it.content)

    # for it in search_content(kw):
        # text=text+it.title+"。"+it.content
    # text_list=text_list+tt.sentence_segmentation_v1(text)

    # for one_it in DB.entity_kg_rank.find({}):
    for one_it in DB.entity_kg_rank.aggregate([{ '$sample': { 'size': 1000 }}  ])  :
        # print(one_it)
        keyword=one_it['entity']+" "+one_it['value']
        try:
            mark_one(keyword)
        except :
            pass
        
def mark_one(keyword):
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
            marked_text,marked_label=bulid_t_data(mjson)
        except:
            pass
        # print("cd",len(c_list))
        # print(marked_label[:2])
        # print(marked_text[-2:])
        # print(len(marked_text),len(marked_label))
        # pre=auto_train(new_text_list,marked_text,marked_label,n_neighbors=len(c_list))
        try:


            pre=auto_train(new_text_list,marked_text,marked_label,tokenizer,model,n_neighbors=len(c_list))

            # print("预测：",pre)
            for i,p in enumerate( pre):
                # print(type(p))
                # print("句子：",new_text_list[i])
                
                try:
                    print("预测结果:",p,c_list[str(p)])
                    # print("预测结果:",p,c_list[int(p)])
                except:
                    pass
        except:
            pass
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