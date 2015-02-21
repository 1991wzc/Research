#!/usr/bin/python
# -*- coding: utf-8 -*-

# tf 换成词的总频率
# idf

from __future__ import division
import sys
import string
import math
import os


class topicAssign:
    # dictionary
    dic_wordTonum = {}

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
            #self.dic_numToword[int(wordpair[1])] = wordpair[0]
        f_wordmap.close()

    def readTweet(self, Dir):
        print 'Read tweets.'
        # get tweets
        f_tweet = open(Dir, 'r')

        tweets = f_tweet.readlines()
        # document length
        self.M = len(tweets)

        for m in xrange(self.M):
            words = tweets[m].split()
            N = len(words)
            for n in xrange(N):
                if words[n] in self.dic_wordTonum:
                    pass
                # assign negative number to words not in dictionary and add it to
                # dictionary
                elif words[n] not in self.dic_wordTonum:
                    self.dic_wordTonum[words[n]] = self.wordID
                    self.wordID -= 1

        f_tweet.close()

    def creat_new_wordmap(self, Dir):
        print 'Creat new Wordmap file.'
        f = open(Dir, 'w')
        f.write('')
        f = open(Dir, 'a')

        for word in self.dic_wordTonum:
            f.write(word + ' ' + str(self.dic_wordTonum[word]) + '\n')

        f.close()


def new_wordmap_user(ID):

    path = os.getcwd()
    #path=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    #parentpath=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    en = topicAssign()
    en.readWordmap(path+'\\topic assign\\wordmap_en.txt')
    en.readTweet(path + '\\tweets\\'+ID + '_processed.txt')
    en.creat_new_wordmap(path + '\\tf-idf\\new wordmap\\new_wordmap_en_'+ID+'.txt')