#!/usr/bin/python
# -*- coding: utf-8 -*-

# tf 换成词的总频率
# idf

from __future__ import division
import sys
import string
import math
import os


class Tf_idf:
    # dictionary
    dic_wordTonum = {}
    dic_numToword = {}

    # tweets document length
    M = 0

    # documents
    document = []

    # tf
    tf = []

    # df
    df = {}

    # tf-idf
    tf_idf = []

    def readNewWordmap(self, Dir):
        print 'Read wordmap.'
        # get trained dictionary
        f_wordmap = open(Dir, 'r')

        for wordpair in f_wordmap.readlines():
            wordpair = wordpair.split()
            self.dic_wordTonum[wordpair[0]] = int(wordpair[1])
            self.dic_numToword[int(wordpair[1])] = wordpair[0]

    def readTweet(self, Dir):
        print 'Read tweets.'
        # get tweets
        f_tweet = open(Dir, 'r')

        tweets = f_tweet.readlines()
        # document length
        self.M = len(tweets)
        self.document = [0] * self.M
        self.tf=[0]*self.M
        self.tf_idf=[0]*self.M

        for m in xrange(self.M):
            words = tweets[m].split()
            N = len(words)
            self.document[m] = [0] * N
            # self.tf[m]=[0]*N
            # self.tf_idf[m]=[0]*N

            for n in xrange(N):
                self.document[m][n] = self.dic_wordTonum[words[n]]

    def calculateTf(self):
        print 'Calculate Tf.'
        for m in xrange(self.M):
            N=len(self.document[m])
            self.tf[m] = [0]*N
            self.tf_idf[m]=[0]*N
            for n in xrange(N):
                    self.tf[m][n] = self.document[m].count(self.document[m][n])/len(self.document[m])
        
        # count=0
        # for word in self.tf:
        #     count+=self.tf[word]
        # print count

    def calculateDf(self):
        print 'Calculate Df.'
        for word in self.dic_numToword:
            self.df[word] = 0
        for m in xrange(self.M):
            exist = []
            for word in self.document[m]:
                if word not in exist:
                    self.df[word] += 1
                    exist.append(word)

        # count=0
        # for word in self.df:
        #     count+=self.df[word]
        # print count

    def calculateTf_idf(self):
        for m in xrange(self.M):
            # calculate tf_idf for each word
            for n in xrange(len(self.document[m])):
                self.tf_idf[m][n] = self.tf[m][n] * math.log(self.M / self.df[self.document[m][n]])

    def creat_tf_idf_file(self,Dir):
        print 'Creat Tf_idf file.'
        f = open(Dir, 'w')
        f.write('')
        f = open(Dir, 'a')
        for m in xrange(self.M):
            for n in xrange(len(self.document[m])):
                f.write(str(self.tf_idf[m][n]) + ' ')
            f.write('\n')


def tf_idf_user(ID):
    path = os.getcwd()
    #parentpath=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))

    TFIDF = Tf_idf()
    TFIDF.readNewWordmap(path + '\\tf-idf\\new wordmap\\new_wordmap_en_'+ID+'.txt')
    TFIDF.readTweet(path + '\\tweets\\'+ID + '_processed.txt')
    TFIDF.calculateTf()
    TFIDF.calculateDf()
    TFIDF.calculateTf_idf()
    TFIDF.creat_tf_idf_file(path + '\\tf-idf\\tf_idf_en_'+ID+'.txt')

    # if lan=='ja':
    #     print 'Japanese'
    #     ja = Tf_idf()
    #     ja.readNewWordmap('new_wordmap_ja.txt')
    #     ja.readTweet(parentpath+'\\tweets\\ja_tweet_final.txt')
    #     ja.calculateTf()
    #     ja.calculateDf()
    #     ja.calculateTf_idf()
    #     ja.creat_tf_idf_file('tf_idf_ja.txt')

# tf_idf('en')
# tf_idf('ja')