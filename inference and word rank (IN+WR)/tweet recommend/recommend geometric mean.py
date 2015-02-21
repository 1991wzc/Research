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
    path = os.getcwd()
    #path=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))

    f_top_words=open(path+'\\topic assign\\model_'+lan+'-final.twordsnoProb')
    lines=f_top_words.readlines()
    
    word_weight=[0]*K
    for k in range(K):
        word_weight[k]=dict()
        words=lines[k].split()
        for word in words:
            word_weight[k][word]=1/(words.index(word)+1)
    f_top_words.close()

    f_tweets_topic=open(path+'\\recommend\\tweet_topic_'+lan+'.txt')
    f_tweets=open(path+'\\tweets\\'+lan+'_tweet_final.txt')
    tweets=f_tweets.readlines()
    f_tweets_weight=open(path+'\\recommend\\tweet_weight_'+lan+'.txt','wb')

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

def recommend_user(usersum,lan,K,top):
    path = os.getcwd()
    #path=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    f_tweets_weight=open(path+'\\recommend\\tweet_weight_'+lan+'.txt','r')
    tweets_weight=list()

    pattern = re.compile(r'http://\S*')

    for line in f_tweets_weight.xreadlines():
        tweets_weight.append(string.atof(line))
    for i in range(usersum):
        ID=i+1
        print 'user '+str(ID)        
        f_topic_prob_en=open(path+'\\recommend\\user\\topic probability\\topic_prob_en_'+str(ID)+'.txt','r')
        lines=f_topic_prob_en.readlines()
        probability = {}

        for line in lines:
            topic=int((line.split())[0])
            if topic!=-1:
                prob=string.atof((line.split())[1])
                probability[topic]=prob

        probability = sorted(probability.iteritems(), key=lambda d: d[1], reverse=True)

        #recommend tweets
        #f_tweet_ja=open(path+'\\tweets\\tweets_ja_ac.txt','r')
        f_related_ja=open(path+'\\recommended tweets\\based on geometric mean\\related_ja_tweets_'+str(ID)+'.txt','wb')
        f_topic_ja=open(path+'\\recommend\\tweet_topic_ja.txt','r')

        #tweet_ja=f_tweet_ja.readlines()
        topic_ja=f_topic_ja.readlines()

        #tweets_weight=calculate_weight(lan, K)

        db = MySQLdb.connect("localhost", "root", "0000", "mydb")

        # 仍然是，第一步要获取连接的cursor对象，用于执行查询
        cur = db.cursor()
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        # 类似于其他语言的query函数，execute是python中的执行查询函数

        for rank in range(5):
            
            print 'Rank %s.'%str(rank+1)
            topic=str(probability[rank][0])

            f_related_ja.write('Topic '+topic+':\n')
            recommend_tweets=dict()

            for tweetnm in xrange(len(topic_ja)):
                if int(topic_ja[tweetnm])==int(topic):

                    dbid=tweetnm+1
                    sql="SELECT * FROM ja_ac where id=%d;"%dbid
                    #print sql
                    cur.execute(sql)
                    rows = cur.fetchall()

                    recommend_tweets[rows[0][1]]=tweets_weight[tweetnm]

            recommend_tweets = sorted(recommend_tweets.iteritems(), key=lambda d: d[1], reverse=True)
            count=0
            exist=list()
            for i in recommend_tweets:
                match = pattern.search(str(i[0]))
                if match and i[1] not in exist:
                    f_related_ja.write('Weight:'+str(i[1])+' '+str(i[0])+'\n')
                    exist.append(i[1])
                    count+=1
                    if count==top:
                        break
            f_related_ja.write('\n')


        f_related_ja.close()

#calculate_weight('ja', 100)
recommend_user(5,'ja',100,1000)