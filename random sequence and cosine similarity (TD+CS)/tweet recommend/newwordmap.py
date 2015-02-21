#!/usr/bin/python
# -*- coding: utf-8 -*-

# tf 换成词的总频率
# idf

from __future__ import division
import sys
import string
import math
import os


class wordMap:
    # dictionary
    dic_wordTonum = {}
    #dic_numToword = {}

    # tweets document length
    M = 0

    # documents
    document = []

    # topic of words
    word_topic = []

    # topic of tweets
    tweet_topic = []

    # topic count
    topic_count = {}

    nd = []
    ndsum = []
    theta = []

    # phi
    phi = []

    # word id for negative
    wordID = -1


    def readWordmap(self, Dir):
        print 'Read wordmap.'
        # get trained dictionary
        f_wordmap = open(Dir, 'r')

        for wordpair in f_wordmap.readlines():
            wordpair = wordpair.split()
            self.dic_wordTonum[wordpair[0]] = int(wordpair[1])
        f_wordmap.close()

    def readTweet(self, Dir):
        print 'Read tweets.'
        # get tweets
        f_tweet = open(Dir, 'r')

        count=0
        for tweet in f_tweet.xreadlines():
            words = tweet.split()            
            for word in words:
                if word in self.dic_wordTonum:
                    pass
                # assign negative number to words not in dictionary and add it to
                # dictionary
                elif word not in self.dic_wordTonum:
                    self.dic_wordTonum[word] = self.wordID
                    self.wordID -= 1
            count+=1
            if count%50000==0:
                print '%s tweets.'%str(count)
        f_tweet.close()

    def creat_new_wordmap(self, Dir):
        print 'Creat new Wordmap file.'
        f = open(Dir, 'wb')

        for word in self.dic_wordTonum:
            f.write(word + ' ' + str(self.dic_wordTonum[word]) + '\n')

        f.close()

def new_wordmap(lan):

    path = os.getcwd()
    #path=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    #parentpath=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))

    WM = wordMap()
    WM.readWordmap(path+'\\topic assign\\wordmap_'+lan+'.txt')
    WM.readTweet(path + '\\tweets\\'+lan+'_tweet_final.txt')
    # for i in range(divide):
    #     print 'Read '+lan+' file ' + str(i)
    #     WM.readTweet(
    #         path + '\\tweets\\splitted\\f_final_'+lan+'-' + str(i) + '.txt')
    WM.creat_new_wordmap(path + '\\tf-idf\\new_wordmap_'+lan+'.txt')


new_wordmap('ja')