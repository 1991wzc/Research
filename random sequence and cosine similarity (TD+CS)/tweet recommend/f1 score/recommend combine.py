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


def recommend(userID,top,r):
    print 'Recommend tweets of top 5 topics for each user.'
    path = os.getcwd()
    #path=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))      
    f_theta_en=open('theta_en_'+str(userID)+'.txt')
    lines=f_theta_en.readlines()
    theta_user = {}

    topic=0
    for line in lines:
        prob=string.atof(line)
        theta_user[topic]=prob
        topic+=1

    ordered = sorted(theta_user.iteritems(), key=lambda d: d[1], reverse=True)

    #recommend tweets
    f_topic_ja=open('tweet_topic_ja.txt')
    topic_ja=f_topic_ja.readlines()    

    right=0
    wrong=0
    count=0
    for i in ordered:   
        topic=i[0]
        print 'Topic %d'%topic
        numberlist=list()
        for tweetnm in xrange(len(topic_ja)):
            if int(topic_ja[tweetnm])==topic:
                numberlist.append(tweetnm)
        right,wrong=calculate_score(numberlist,theta_user,top,r,topic,right,wrong)
        # print right
        # print wrong
        count+=1

        if count==5:
            break

    precision=right/(right+wrong)
    recall=right/5000
    f1=(2*precision*recall)/(precision+recall)

    print 'Right: %d'%right
    print 'Wrong: %d'%wrong
    print 'Right+Wrong: %d'%(right+wrong)
    print 'Precision: %s'%str(precision)
    print 'Recall: %s'%str(recall)
    print 'F1 Score: %s'%str(f1)

def calculate_score(numberlist,theta_user,top,r,topic,right,wrong):
    print 'Calculating score.'
    # path = os.path.abspath(
    #   os.path.join(os.path.dirname("__file__"), os.path.pardir))
    path = os.getcwd()
    #pattern = re.compile(r'http://\S*')

    f_theta_candicates = open('theta_ja.txt')
    theta_candicates = f_theta_candicates.readlines()

    cosine = dict()
    score=dict()

    f_tweets_weight=open('tweet_weight_ja.txt','r')
    tweets_weight=dict()

    lineno=0
    for line in f_tweets_weight.xreadlines():
        tweets_weight[lineno]=string.atof(line)
        lineno+=1

    count=0
    for number in numberlist:
        theta_tweet = []
        theta_tweet = theta_candicates[number].split()
        for i in range(len(theta_tweet)):
            theta_tweet[i] = string.atof(theta_tweet[i])

        cosine[number] = cosine_similarity(theta_user, theta_tweet)

        score[number]=r*cosine[number]+(1-r)*tweets_weight[number]
        count+=1
        if count%2000==0:
            print '%d calculated.'%count

    score = sorted(score.iteritems(), key=lambda d: d[1], reverse=True)

    print 'Writing recommendation into file.'    
    db = MySQLdb.connect("localhost", "root", "0000", "mydb")

    # 仍然是，第一步要获取连接的cursor对象，用于执行查询
    cur = db.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    # 类似于其他语言的query函数，execute是python中的执行查询函数

    count=0
    for i in score:
        dbid = i[0] + 1
        sql="SELECT * FROM ja_f1 where id=%d;"% dbid
        cur.execute(sql) 
        rows = cur.fetchall()
        if rows[0][2] ==1:
            right+=1
        elif rows[0][2] ==0:
            wrong+=1
        count+=1

        if count>(top/5):
            break

    db.close()

    return (right,wrong)

def cosine_similarity(v1, v2):
    "compute cosine similarity of v1 to v2: (v1 dot v1)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]
        y = v2[i]
        sumxx += x * x
        sumyy += y * y
        sumxy += x * y
    return sumxy / math.sqrt(sumxx * sumyy)

if __name__ == "__main__":
    #calculate_weight('ja', 300)
    recommend(2,1000,0.000005)