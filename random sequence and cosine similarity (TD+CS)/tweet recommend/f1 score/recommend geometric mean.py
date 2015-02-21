#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import sys
import string
import math
import os
import MySQLdb
import re

def calculate_weight(lan,K):
    #path = os.getcwd()
    path=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))

    f_top_words=open('model_'+lan+'-final.twordsnoProb')
    lines=f_top_words.readlines()
    
    word_weight=[0]*K
    for k in range(K):
        word_weight[k]=dict()
        words=lines[k].split()
        for word in words:
            word_weight[k][word]=1/(words.index(word)+1)
    f_top_words.close()

    f_tweets_topic=open('tweet_topic_'+lan+'.txt')
    f_tweets=open(lan+'_tweet_final.txt')
    tweets=f_tweets.readlines()
    f_tweets_weight=open('tweet_weight_'+lan+'.txt','wb')

    lineNo=-1
    tweets_weight=[0]*len(tweets)
    for topic in f_tweets_topic.xreadlines():
        lineNo+=1
        words=tweets[lineNo].split()
        geometricMean=1
        for word in words:
            #exponent+=1
            if word in word_weight[int(topic)]:
                geometricMean*=word_weight[int(topic)][word]
            elif word not in word_weight[int(topic)]:
                geometricMean*=math.pow(1/1000,2)
        if len(words)!=0:
            geometricMean=math.pow(geometricMean, 1/len(words))
            tweets_weight[lineNo]=geometricMean
        elif len(words)==0:
            tweets_weight[lineNo]=math.pow(1/1000,2)

        f_tweets_weight.write(str(tweets_weight[lineNo])+'\n')
            
        if lineNo%50000==0:
            print '%s tweets\' weights calculated.'%str(lineNo)    

    f_tweets.close()
    f_tweets_weight.close()
    f_tweets_topic.close()

    #return tweets_weight

def recommend_user(userID,lan,K,top):
    #path = os.getcwd()
    path=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    f_tweets_weight=open('tweet_weight_'+lan+'.txt','r')
    tweets_weight=list()

    for line in f_tweets_weight.xreadlines():
        tweets_weight.append(string.atof(line))
      
    f_topic_prob_en=open('topic_prob_en_'+str(userID)+'.txt')
    lines=f_topic_prob_en.readlines()
    probability = {}

    for line in lines:
        topic=int((line.split())[0])
        if topic!=-1:
            prob=string.atof((line.split())[1])
            probability[topic]=prob

    probability = sorted(probability.iteritems(), key=lambda d: d[1], reverse=True)

    f_topic_ja=open(path+'\\recommend\\tweet_topic_ja.txt','r')
    topic_ja=f_topic_ja.readlines()

    idlist=list()

    for rank in range(5):
        
        print 'Rank %s.'%str(rank+1)
        topic=str(probability[rank][0])

        recommend_tweets=dict()

        for tweetnm in xrange(len(topic_ja)):
            if int(topic_ja[tweetnm])==int(topic):
                recommend_tweets[tweetnm]=tweets_weight[tweetnm]

        recommend_tweets = sorted(recommend_tweets.iteritems(), key=lambda d: d[1], reverse=True)

        count=0
        for i in recommend_tweets:
            idlist.append(i[0])
            count+=1

    db = MySQLdb.connect("localhost", "root", "0000", "mydb")

    # 仍然是，第一步要获取连接的cursor对象，用于执行查询
    cur = db.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    # 类似于其他语言的query函数，execute是python中的执行查询函数

    right=0
    wrong=0

    for i in idlist:
        dbid = i + 1
        sql="SELECT * FROM ja_f1 where id=%d;"% dbid
        cur.execute(sql) 
        rows = cur.fetchall()
        if rows[0][2] ==1:
            right+=1
        elif rows[0][2] ==0:
            wrong+=1

        if right+wrong == top:
            break

    precision=right/(right+wrong)
    recall=right/5000
    f1=(2*precision*recall)/(precision+recall)
    print 'Right: %d'%right
    print 'Wrong: %d'%wrong
    print 'Precision: %s'%str(precision)
    print 'Recall: %s'%str(recall)
    print 'F1 Score: %s'%str(f1)

    db.close()

#calculate_weight('ja', 100)
recommend_user(2,'ja',100,200)