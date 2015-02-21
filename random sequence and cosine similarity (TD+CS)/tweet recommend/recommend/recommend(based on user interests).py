#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import sys
import string
import math
import os

def recommend(usersum):
    path = os.getcwd()
    #path=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    for ID in range(usersum):        
        f_topic_prob=open(path+'\\recommend\\user\\topic probability\\topic_prob_en_'+str(ID)+'.txt','r')

        lines=f_topic_prob_en.readlines()

        probability = {}

        for line in lines:
            topic=int((line.split())[0])
            prob=string.atof((line.split())[1])
            probability[topic]=prob

        probability = sorted(probability.iteritems(), key=lambda d: d[1], reverse=False)

        #recommend tweets
        f_tweet_ja=open(path+'\\tweets\\ja_pub_tweets.txt','r')

        f_related_ja=open(path+'\\recommended tweets\\based on user interests\\related_ja_tweets_'+str(ID)+'.txt','w')
        f_related_ja.write('')
        f_related_ja=open(path+'\\recommended tweets\\based on user interests\\related_ja_tweets_'+str(ID)+'.txt','a')

        f_topic_ja=open(path+'\\recommend\\tweet_topic_ja.txt','r')
        
        tweet_ja=f_tweet_ja.readlines()

        topic_ja=f_topic_ja.readlines()


        for rank in range(10):
            topic=str(probability[rank][0])
            #print 'Topic '+topic
            f_recommend.write('Topic '+topic+':\n')
            for tweetnm in xrange(len(topic_en)):
                if int(topic_en[tweetnm])==int(topic):
                    f_recommend.write(tweet_en[tweetnm])
            f_recommend.write('\n')

            f_related_ja.write('Topic '+topic+':\n')
            for tweetnm in xrange(len(topic_ja)):
                if int(topic_ja[tweetnm])==int(topic):
                    f_related_ja.write(tweet_ja[tweetnm])
            f_related_ja.write('\n')

recommend(100)