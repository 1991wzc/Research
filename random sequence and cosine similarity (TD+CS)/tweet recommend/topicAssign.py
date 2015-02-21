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
    alpha = 0
    K = 0
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

    nd = []
    ndsum = []
    theta = []
    
    #
    max_prob=[]

    # word id for negative
    wordID = -1

    # tf-idf
    tf_idf = []

    def setParameters(self,alpha,K):
        self.alpha=alpha
        self.K=K

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
        self.word_topic = [-1] * self.M
        self.max_prob=[0]*self.M

        for m in xrange(self.M):
            words = tweets[m].split()
            N = len(words)
            self.document[m] = [0] * N
            self.word_topic[m] = [-1] * N
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

    def readTFIDF(self,Dir):
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
       
        self.nd = [0] * self.M
        self.ndsum = [0] * self.M
        self.theta = [0] * self.M
        #initiate nd and theta
        for m in xrange(self.M):
            self.nd[m] = [0] * self.K
            self.theta[m] = [0] * self.K

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
                    self.nd[m][self.word_topic[m][n]] += 1
                    self.ndsum[m] += 1

    # def assignTopic_word_tfidf(self):
    #     print 'Assign topic to each word (with tf-idf).'
       
    #     self.nd = [0] * self.M
    #     self.ndsum = [0] * self.M
    #     self.theta = [0] * self.M
    #     #initiate nd and theta
    #     for m in xrange(self.M):
    #         self.nd[m] = [0] * self.K
    #         self.theta[m] = [0] * self.K

    #     # topic assign for each word
    #     for m in xrange(self.M):
    #         if len(self.document[m])==0:
    #             continue
    #         elif len(self.document[m])!=0:
    #             for n in xrange(len(self.document[m])):
    #                 #multiply tf-idf as weight
    #                 if self.document[m][n] >= 0:
    #                     # words in dictionary                                       
    #                     # assign topic
    #                     self.word_topic[m][n] = self.word2topic[self.document[m][n]] 

    #                 # assign topic of their front word to unseen words
    #                 elif self.document[m][n] < 0:
    #                     if n > 0:
    #                         self.word_topic[m][n] = self.word_topic[m][n - 1]

    #                     #if no front word,assign -1,after all words assgined, assign topic of next word to it
    #                     elif n==0:
    #                         self.word_topic[m][n]=-1
    #             if self.word_topic[m][0]==-1  and len(self.document[m])>1:
    #                 self.word_topic[m][0]=self.word_topic[m][1]

    #     #calculate nd and ndsum
    #     for m in xrange(self.M):
    #         for n in range(len(self.document[m])):
    #             if self.word_topic[m][n]==-1:
    #                 pass
    #             elif self.word_topic[m][n]!=-1:
    #                 self.nd[m][self.word_topic[m][n]] += 1*self.tf_idf[m][n]
    #                 self.ndsum[m] += 1*self.tf_idf[m][n]

    def assignTopic_tweet(self):
        print 'Assign topic to each tweets.'
        # compute theta of tweets
        for m in xrange(self.M):
            for k in xrange(self.K):
                self.theta[m][k] = (
                    self.nd[m][k] + self.alpha) / (self.ndsum[m] + self.K*self.alpha)

        # assign topic to tweets and get topic ranking of tweets
        self.tweet_topic = [0] * self.M
        self.topic_count.clear()
        self.topic_count[-1]=0
        for k in range(self.K):
            self.topic_count[k]=0
        for m in xrange(self.M):
            if len(self.document[m])==0:
                self.tweet_topic[m]=-1
                self.topic_count[-1]+=1
            elif len(self.document[m])!=0:
                maximum = 0
                topic = -1
                allminus=True
                for n in range(len(self.document[m])):
                    if self.word_topic[m][n]!=-1:
                        allminus=False

                
                for k in xrange(self.K):
                    if maximum < self.theta[m][k]:
                        maximum = self.theta[m][k]
                        # -1th topic is meaningless
                        topic = k
                #if the max probability is equal to average probability, assign topic -1 to it
                if allminus==True:
                    topic=-1

                self.tweet_topic[m] = topic
                self.topic_count[topic] += 1


    def create_topic_count_file(self, Dir):
        print 'Creat topic count file.'
        # print self.topic_count
        f = open(Dir, 'w')
        f.write('')
        f = open(Dir, 'a')

        for topic in self.topic_count:
            if topic==-1:
                continue
            f.write(str(self.topic_count[topic]) + '\n')

        f.close()

    def create_tweet_topic_file(self, Dir):
        print 'Creat tweet topic file.'
        f = open(Dir, 'w')
        f.write('')
        f = open(Dir, 'a')

        for topic in self.tweet_topic:
            f.write(str(topic) + '\n')
        f.close()


    def create_word_topic_file(self, Dir):
        print 'Creat word topic file.'
        # print self.topic_count
        f = open(Dir, 'w')
        f.write('')
        f = open(Dir, 'a')

        for m in range(len(self.word_topic)):
            for topic in self.word_topic[m]:
                f.write(str(topic) + ' ')
            f.write('\n')

    def create_max_prob_file(self,Dir):
        print 'Creat max prob file.'
        # print self.topic_count
        f = open(Dir, 'wb')

        for maximum in self.max_prob:
            f.write(str(maximum)+'\n')

        f.close()

    def create_theta_file(self,Dir):
        print 'Creat theta file.'
        # print self.topic_count
        f = open(Dir, 'wb')

        for m in range(self.M):
            for k in range(self.K):
                f.write(str(self.theta[m][k])+' ')
            f.write('\n')

        f.close()

    def create_word_topic_file(self,Dir):
        print 'Creat word topic file.'
        # print self.topic_count
        f = open(Dir, 'wb')

        for m in range(self.M):
            for topic in self.word_topic[m]:
                f.write(str(topic)+' ')
            f.write('\n')

        f.close()

    def create_nd_file(self,Dir):
        print 'Creat nd file.'
        # print self.topic_count
        f = open(Dir, 'wb')

        for m in range(self.M):
            f.write(str(self.ndsum[m])+': ')
            for number in self.nd[m]:
                f.write(str(number)+' ')
            f.write('\n')

        f.close()

def main(lan,divide,alpha,K):
    path = os.getcwd()
    #path=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    #parentpath=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    TA = topicAssign()
    TA.setParameters(alpha,K)
    TA.readWordmap(path+'\\tf-idf\\new_wordmap_'+lan+'.txt')
    TA.read_word2topic(path+'\\topic assign\\model_'+ lan +'-final.phi_word2topic')
    #TA.readPhi(path+'\\topic assign\\model_'+lan+'-final.phi')
    for i in range(divide):
        print 'Read '+lan+' file ' + str(i)
        TA.readTweet(
            path + '\\tweets\\splitted\\f_final_'+lan+'-' + str(i) + '.txt')        
        TA.assignTopic_word()
        TA.assignTopic_tweet()
        TA.create_topic_count_file(
            path + '\\temp\\topic_count_'+lan+'-' + str(i) + '.txt')
        TA.create_tweet_topic_file(path + '\\temp\\tweet_topic_'+lan+'-' + str(i) + '.txt')
        TA.create_theta_file(path + '\\temp\\theta_'+lan+'-' + str(i) + '.txt')


main('ja',30,0.5,100)