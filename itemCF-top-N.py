import pandas as pd
import numpy as np
import random
from math import *

movies_path = r'F:\datasets\ml-latest-small\movies.csv'
ratings_path = r'F:\datasets\ml-latest-small\ratings.csv'
data_path = r'F:\datasets\ml-latest-small\itemCF_data.csv'

#load data
movies_csv = pd.read_csv(movies_path,sep=',')
ratings_csv = pd.read_csv(ratings_path,sep=',')
#connect by movieId
cdata = pd.merge(movies_csv,ratings_csv, on='movieId')
#写入CSV保存
cdata[['userId','rating','movieId','title','genres']].sort_values('userId').to_csv(data_path,header=False)

file = open(data_path,'r',encoding='utf-8')
data = {}##存放每个电影被评论的用户和评分
for line in file.readlines():
    line = line.strip().split(',')
    # 如果字典中没有某部电影，则使用电影ID来创建这部电影
    if not line[3] in data.keys():
        data[line[3]] = {line[1]:line[2]}
    # 否则直接添加以该电影ID为key字典中
    else:
        data[line[3]][line[1]] = line[2]

def Euclidean(item1, item2):
    #取出两部电影被评论过的用户和评分
    item1_data = data[item1]
    item2_data = data[item2]
    dist = 0
    #找到两部电影都被评论过的用户，计算欧氏距离
    for key in item1_data.keys():
        if key in item2_data.keys():
            #distance越大表示两者越相似
            dist = dist + pow(float(item1_data[key]) - float(item2_data[key]), 2)

    return 1 / (1 + sqrt(dist))

#计算某部电影和其他电影的相似度
def top10_similar(item1):
    res = []
    for itemid in data.keys():
        if not item1 == itemid:
            similar = Euclidean(item1,itemid)
            res.append((itemid,similar))

    res.sort(key=lambda val: val[1], reverse = True)
    return res[:10]

def recommend(i):
    #相似度最高的电影
    top_sim_item = top10_similar(i)[0][0]
    # 相似度最高的电影的观影记录
    items = data[top_sim_item]
    #print(items)
    recommendation = []
    #筛选出该电影未观看的用户并添加到列表中
    for item in items.keys():
        if item not in data[i].keys():
            recommendation.append((item,items[item]))
    # 按照评分排序
    recommendation.sort(key=lambda val:val[1],reverse=True)
    # 返回评分最高的10部电影
    return recommendation[:10]


Recommendations = recommend('13')
for each in Recommendations:
    print(each)