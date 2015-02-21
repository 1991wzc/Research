#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import sys
import string
import math
import os


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


def recommend_user(usersum, lan, top):
    path = os.path.abspath(
        os.path.join(os.path.dirname("__file__"), os.path.pardir))

    f_theta_candicates = open(path + '\\recommend\\theta_ja.txt')
    theta_candicates = f_theta_candicates.readlines()

    for i in range(usersum):
        ID = 500 + 1000 * i
        print 'user ' + str(ID)

        f_theta_user = open(
            path + '\\recommend\\user\\topic probability\\theta_en_' + str(ID) + '.txt')
        theta_user = list()
        user_all = f_theta_user.readlines()
        for i in range(len(user_all)):
            theta_user.append(string.atof(i))

        #probability = sorted(probability.iteritems(), key=lambda d: d[1], reverse=True)

        # recommend tweets
        f_tweet_ja = open(path + '\\tweets\\tweets_ja_ac.txt', 'r')
        f_related_ja = open(
            path + '\\recommended tweets\\based on cosine\\related_ja_tweets_' + str(ID) + '.txt', 'w')

        tweet_ja = f_tweet_ja.readlines()
        cosine = dict()
        #print len(theta_candicates)
        lineno=0
        for tweet in tweet_ja:

            theta_tweet = theta_candicates[lineno].split()
            for i in range(len(theta_tweet)):
                theta_tweet[i] = string.atof(theta_tweet[i])

            cosine[lineno] = cosine_similarity(theta_user, theta_tweet)
            lineno+=1
            if lineno % 10000 == 0:
                print '%d cosine calculated.' % lineno

        cosine = sorted(cosine.iteritems(), key=lambda d: d[1], reverse=True)

        count = 0
        for i in cosine:
            f_related_ja.write(
                'cosine: ' + str(i[1]) + ' ' + tweet_ja[i[0]])
            count += 1
            if count == top:
                break

        f_related_ja.close()

recommend_user(10, 'ja', 5000)
