#!/usr/bin/python
# -*- coding: utf-8 -*-

# tf 换成词的总频率
# idf

from __future__ import division
import sys
import string
import math
import os
import tf_idf
import csv


class topicDistribution:
    alpha = 0
    K = 0
    nsum=0
    # dictionary
    dic_wordTonum = {}
    #dic_numToword = {}

    #word to topic
    word2topic=dict()

    # tweets document length
    M = 0

    # documents
    document = []

    # topic of words in tweets
    word_topic = []

    # topic of tweets
    tweet_topic = []

    # topic count
    topic_count = {}

    #theta
    theta=[]

    #number of words in each topic
    n = []

    # word id for negative
    wordID = -1

    # tf-idf
    tf_idf = []

    def setParameters(self,alpha,K):
        self.alpha=alpha
        self.K=K
        self.n=[0]*K
        self.theta=[0]*K

    def readWordmap(self, Dir):
        print 'Read new wordmap.'
        # get trained dictionary
        f_wordmap = open(Dir, 'r')

        for wordpair in f_wordmap.readlines():
            wordpair = wordpair.split()
            self.dic_wordTonum[wordpair[0]] = int(wordpair[1])
            #self.dic_numToword[int(wordpair[1])] = wordpair[0]
        f_wordmap.close()

    def read_word2topic(self,Dir):
        print 'Read word to topic file.'       
        #get probability of current Topic for each word in old vocabulary
        f = open(Dir, 'r')

        for line in f.xreadlines():
            split=line.split()
            self.word2topic[int(split[0])]=int(split[1])

        f.close()

    def readTweet(self, Dir):
        print 'Read tweets.'
        # get tweets
        f_tweet = open(Dir, 'r')

        tweets = f_tweet.readlines()
        # document length
        self.M = len(tweets)
        self.document = [0] * self.M
        self.word_topic = [0] * self.M

        for m in xrange(self.M):
            words = tweets[m].split()
            N = len(words)
            #self.nsum+=N
            self.document[m] = [0] * N
            self.word_topic[m] = [0] * N
            for n in xrange(N):
                if words[n] in self.dic_wordTonum:
                    self.document[m][n] = self.dic_wordTonum[words[n]]
                # assign negative number to words not in dictionary and add it to
                # dictionary
                if words[n] not in self.dic_wordTonum:
                    self.dic_wordTonum[words[n]] = self.wordID
                    #self.dic_numToword[self.wordID] = words[n]
                    self.document[m][n] = self.wordID
                    self.wordID -= 1

        f_tweet.close()

    def readTFIDF(self, Dir):
        print 'Read tf-idf.'
        f_tfidf = open(Dir, 'r')

        tweets = f_tfidf.readlines()
        # document length
        self.M = len(tweets)
        self.tf_idf = [0] * self.M

        for m in xrange(self.M):
            words = tweets[m].split()
            N = len(words)
            self.tf_idf[m] = [0] * N
            #self.word_topic[m] = [0] * N
            for n in xrange(N):
                self.tf_idf[m][n] = string.atof(words[n])

        f_tfidf.close()

    def assignTopic_word(self):
        print 'Assign topic to each word (without tf-idf).'

        # topic assign for each word
        for m in xrange(self.M):
            if len(self.document[m])==0:
                continue
            elif len(self.document[m])!=0:
                for n in xrange(len(self.document[m])):
                    #multiply tf-idf as weight
                    if self.document[m][n] >= 0:
                        # words in dictionary                                       
                        # assign topic
                        self.word_topic[m][n] = self.word2topic[self.document[m][n]]

                    # assign topic of their front word to unseen words
                    elif self.document[m][n] < 0:
                        if n > 0:
                            self.word_topic[m][n] = self.word_topic[m][n - 1]

                        #if no front word,assign -1,after all words assgined, assign topic of next word to it
                        elif n==0:
                            self.word_topic[m][n]=-1
                if self.word_topic[m][0]==-1  and len(self.document[m])>1:
                    self.word_topic[m][0]=self.word_topic[m][1]

        #calculate nd and ndsum
        for m in xrange(self.M):
            for n in range(len(self.document[m])):
                if self.word_topic[m][n]==-1:                    
                    pass
                elif self.word_topic[m][n]!=-1:
                    self.nsum+=1
                    self.n[self.word_topic[m][n]] += 1

    def calculateTheta(self):
        print 'Calculate theta.'
        #summary=0
        for k in range(self.K):
            self.theta[k]=(self.n[k] + self.alpha) / (self.nsum + self.K*self.alpha)
            #summary+=self.theta[k]
        #print summary

    def create_theta_file(self,Dir):
        print 'Creat theta file.'
        # print self.topic_count
        f = open(Dir, 'wb')

        for i in self.theta:
            f.write(str(i) + '\n')

        f.close()


def topicDistribution_user(lan, ID,alpha,K):
    path = os.getcwd()
    #path=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    # parentpath=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    #divide = 10

    TD = topicDistribution()
    TD.setParameters(alpha,K)
    TD.readWordmap(
        path + '\\tf-idf\\new wordmap\\new_wordmap_'+ lan +'_'+ID+'.txt')
    TD.readTweet(path + '\\tweets\\'+ID + '_processed.txt')
    TD.read_word2topic(path+'\\topic assign\\model_'+ lan +'-final.phi_word2topic')    
    TD.assignTopic_word()
    TD.calculateTheta()
    TD.create_theta_file(path + '\\recommend\\topic probability\\theta_' + lan + '_' + ID + '.txt')
