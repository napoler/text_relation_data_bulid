---
layout: default
---

<!-- 
[Link to another page](./another-page.html). -->



# 关于text_relation_data_bulid
MRPC格式数据标记助手
MRPC(Microsoft Research Paraphrase Corpus)，由微软发布，判断两个给定句子，是否具有相同的语义，属于句子对的文本二分类任务。
https://www.microsoft.com/en-us/download/details.aspx?id=52398

![效果](https://raw.githubusercontent.com/napoler/text_relation_data_bulid/master/assets/_2020-06-15_19-10-53.png "效果")

## 运行

进行标注

```
$ python mark.py
```
data转化为MRPC格式
输出目录为data下
```
$ python data2MRPC.py
```




数据句子索引使用了elasticsearch

index_sent.py中有索引demo



## 数据
个人用小部分数据开源
https://www.kaggle.com/terrychanorg/text-relation-data-2mrpc/

## Bert模型
数据标记不是很大，自己可以训练后使用
https://www.kaggle.com/terrychanorg/transformerstextrelationmodel

训练过程

https://www.kaggle.com/terrychanorg/transformers-text-relation/

## 联系我

如果您有任何意见都可以随时联系我

Github上留言：


邮箱：
napoler2008{@}gmail.com

