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
    tf = {}

    # df
    df = {}

    #tf idf word
    tf_idf_word = {}

    # tf-idf
    tf_idf = {}

    #total words
    corpusLen=0

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

        for m in xrange(self.M):
            words = tweets[m].split()
            N = len(words)
            self.document[m] = [0] * N

            for n in xrange(N):
                self.document[m][n] = self.dic_wordTonum[words[n]]

    def calculateTf(self):
        print 'Calculate Tf.'
        for word in self.dic_numToword:
            self.tf[word] = 0
        for m in self.document:
            self.corpusLen+=len(m)
        for m in xrange(self.M):
            for word in self.document[m]:
                    self.tf[word] += self.document[m].count(word)/self.corpusLen
        
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
            N = len(self.document[m])

            p = 0
            for word in self.document[m]:
                # calculate tf_idf for each word
                self.tf_idf_word[word] = self.tf[
                    word] * math.log(self.M / self.df[word])
                p = p + self.tf_idf_word[word]
            # final tf_idf is for weight of each tweet
            if len(self.document[m])>0:
                self.tf_idf[m] = p / N
            else:
                self.tf_idf[m] = 0
    
    def creat_tf_file(self,Dir):
        print 'Creat tf file.'
        f = open(Dir, 'w')
        f.write('')
        f = open(Dir, 'a')

        for word in self.tf:
            f.write(str(self.tf[word]) + '\n')

    def creat_df_file(self,Dir):
        print 'Creat df file.'
        f = open(Dir, 'w')
        f.write('')
        f = open(Dir, 'a')

        for word in self.df:
            f.write(str(self.df[word]) + '\n')

    def creat_tf_idf_word_file(self,Dir):
        print 'Creat tf_idf_word file.'
        f = open(Dir, 'w')
        f.write('')
        f = open(Dir, 'a')

        for word in self.tf_idf_word:
            f.write(str(self.tf_idf_word[word]) + '\n')

    def creat_tf_idf_file(self,Dir):
        print 'Creat Tf_idf file.'
        f = open(Dir, 'w')
        f.write('')
        f = open(Dir, 'a')

        for tweet in self.tf_idf:
            f.write(str(self.tf_idf[tweet]) + '\n')

#path = os.getcwd()
parentpath=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))

lan='ja'
if lan=='en':
    print 'English'    
    en = Tf_idf()
    en.readNewWordmap('new_wordmap_en.txt')
    en.readTweet(parentpath + '\\tweets\\en_tweet_final.txt')
    en.calculateTf()
    en.calculateDf()
    en.calculateTf_idf()
    # en.creat_tf_file('tf_en.txt')
    # en.creat_df_file('df_en.txt')
    # en.creat_tf_idf_word_file('tf_idf_word_en.txt')
    en.creat_tf_idf_file('tf_idf_en(doc weight).txt')

if lan=='ja':
    print 'Japanese'
    ja = Tf_idf()
    ja.readNewWordmap('new_wordmap_ja.txt')
    ja.readTweet(parentpath+'\\tweets\\ja_tweet_final.txt')
    ja.calculateTf()
    ja.calculateDf()
    ja.calculateTf_idf()
    ja.creat_tf_idf_file('tf_idf_ja(doc weight).txt')
