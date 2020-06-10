import pandas as pd
import numpy as np
import random
from math import *


movies_path = r'F:\datasets\ml-latest-small\movies.csv'
ratings_path = r'F:\datasets\ml-latest-small\ratings.csv'
data_path = r'F:\datasets\ml-latest-small\userCF_data.csv'

#将用户行为数据集按照均匀分布随机分成M份
def SplitData(data,M,k,seed):
    test = {}
    train = {}
    random.seed(seed)
    # each 用户id
    #data[each] 对应电影名称和评分
    for each in data.keys():
        if random.randint(0,M) == k:
            test[each] = data[each]
        else:
            train[each] = data[each]
            pass
    return train, test

#load data
movies_csv = pd.read_csv(movies_path,sep=',')
ratings_csv = pd.read_csv(ratings_path,sep=',')
#connect by movieId
cdata = pd.merge(movies_csv,ratings_csv, on='movieId')
#写入CSV保存
cdata[['userId','rating','movieId','title','genres']].sort_values('userId').to_csv(data_path,header=False)


file = open(data_path,'r',encoding='utf-8')
data = {}##存放每位用户评论的电影和评分
for line in file.readlines():
    line = line.strip().split(',')
    # 如果字典中没有某位用户，则使用用户ID来创建这位用户
    if not line[1] in data.keys():
        data[line[1]] = {line[3]:line[2]}
    # 否则直接添加以该用户ID为key字典中
    else:
        data[line[1]][line[3]] = line[2]

#print(data)
#将data进行分解成测试集和训练集
train_data, test_data = SplitData(data,10,1,1)

def Euclidean(user1, user2):
    #取出两个用户评论过的电影和评分
    user1_data = data[user1]
    user2_data = data[user2]
    dist = 0
    #找到两个用户都评论过的电影，计算欧氏距离
    for key in user1_data.keys():
        if key in user2_data.keys():
            #distance越大表示两者越相似
            dist = dist + pow(float(user1_data[key]) - float(user2_data[key]), 2)

    return 1 / (1 + sqrt(dist))

def Pearson_similarity(user1, user2):
    user1_data = data[user1]
    user2_data = data[user2]
    dist = 0
    common = {}
    #找到两个用户都评论过的电影，计算皮尔逊相关系数
    for key in user1_data.keys():
        if key in user2_data.keys():
            common[key] = 1

    if len(common) == 0:
        return 0

    n = len(common)
    #计算评分和
    sum1 = sum([float(user1_data[movie]) for movie in common])
    sum2 = sum([float(user2_data[movie]) for movie in common])

    #计算评分和
    sum1Sq = sum([pow(float(user1_data[movie]), 2) for movie in common])
    sum2Sq = sum([pow(float(user2_data[movie]), 2) for movie in common])

    #计算乘积和
    PSum = sum([float(user1_data[it]) * float(user2_data[it]) for it in common])

    P = ((n * PSum) - (sum1 * sum2)) / (sqrt((n * sum1Sq) - pow(sum1,2)) * sqrt((n * sum2Sq) - pow(sum2,2)))

    return P

#计算某个用户和其他用户的相似度
def top10_similar(user1):
    res = []
    for userid in train_data.keys():
        if not user1 == userid:
            similar = Euclidean(user1,userid)
            #similar = Pearson_similarity(user1,userid)
            res.append((userid,similar))

    res.sort(key=lambda val: val[1], reverse = True)
    return res[:10]

def recommend(user):
    #相似度最高的用户
    top_sim_user = top10_similar(user)[0][0]
    # 相似度最高的用户的观影记录
    items = train_data[top_sim_user]
    recommendation = []
    #筛选出该用户未观看的电影并添加到列表中
    for item in items.keys():
        if item not in train_data[user].keys():
            recommendation.append((item,items[item]))
    # 按照评分排序
    recommendation.sort(key=lambda val:val[1],reverse=True)
    # 返回评分最高的10部电影
    return recommendation

Recommendations = recommend('6')
#看推荐效果
for each in Recommendations:
    print(each)
