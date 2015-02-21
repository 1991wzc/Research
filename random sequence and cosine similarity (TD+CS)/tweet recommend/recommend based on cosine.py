#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import sys
import string
import math
import os
import MySQLdb
import re


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


def recommend_user(usersum, top):
    # path = os.path.abspath(
    #     os.path.join(os.path.dirname("__file__"), os.path.pardir))
    path = os.getcwd()

    f_theta_candicates = open(path + '\\recommend\\theta_ja.txt')
    theta_candicates = f_theta_candicates.readlines()

    pattern = re.compile(r'http://\S*')

    for i in range(usersum):
        ID = i+1
        print 'user ' + str(ID)

        f_theta_user = open(
            path + '\\recommend\\user\\topic probability\\theta_en_' + str(ID) + '.txt')
        theta_user = []
        user_all = f_theta_user.readlines()
        # print user_all
        for i in user_all:
            theta_user.append(string.atof(i))

        # recommend tweets
        # f_tweet_ja = open(path + '\\tweets\\tweets_ja_ac.txt', 'r')
        f_related_ja = open(
            path + '\\recommended tweets\\based on cosine\\related_ja_tweets_' + str(ID) + '.txt', 'w')

        # tweet_ja = f_tweet_ja.readlines()
        cosine = dict()
        cosine.clear()
        # print len(theta_candicates)
        for lineno in range(len(theta_candicates)):
            theta_tweet = []
            theta_tweet = theta_candicates[lineno].split()
            for i in range(len(theta_tweet)):
                theta_tweet[i] = string.atof(theta_tweet[i])

            cosine[lineno] = cosine_similarity(theta_user, theta_tweet)
            if lineno % 10000 == 0:
                # print cosine[lineno-1]
                print 'cosine calculating %d.' % lineno

        cosine = sorted(cosine.iteritems(), key=lambda d: d[1], reverse=True)

        count = 0
        db = MySQLdb.connect("localhost", "root", "0000", "mydb")

        # 仍然是，第一步要获取连接的cursor对象，用于执行查询
        cur = db.cursor()
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        # 类似于其他语言的query函数，execute是python中的执行查询函数
        exist=list()
        for i in cosine:
            dbid = i[0] + 1
            sql="SELECT * FROM ja_ac where id=%d;"% dbid
            #print sql
            #break
            cur.execute(sql) 
            rows = cur.fetchall()
            match = pattern.search(rows[0][1])
            if match and i[1] not in exist:
                f_related_ja.write(
                    'cosine: ' + str(i[1]) + ' ' + rows[0][1]+'\n')
                exist.append(i[1])
                count += 1
                if count == top:
                    break

        f_related_ja.close()

recommend_user(5, 1000)
