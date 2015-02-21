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


def recommend_user(userID, top):
    path = os.path.abspath(
        os.path.join(os.path.dirname("__file__"), os.path.pardir))

    f_theta_candicates = open('theta_ja.txt')
    theta_candicates = f_theta_candicates.readlines()

    f_theta_user = open('theta_en_' + str(userID) + '.txt')
    theta_user = []
    user_all = f_theta_user.readlines()
    # print user_all
    for i in user_all:
        theta_user.append(string.atof(i))

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

    db = MySQLdb.connect("localhost", "root", "0000", "mydb")

    # 仍然是，第一步要获取连接的cursor对象，用于执行查询
    cur = db.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    # 类似于其他语言的query函数，execute是python中的执行查询函数

    right=0
    wrong=0

    for i in cosine:

        dbid = i[0] + 1
        sql="SELECT * FROM ja_f1 where id=%d;"% dbid
        cur.execute(sql) 
        rows = cur.fetchall()
        if rows[0][2] ==1:
            right+=1
        elif rows[0][2] ==0:
            wrong+=1

        if right+wrong == top:
            break

    precision=right/(right+wrong)
    recall=right/5000
    f1=(2*precision*recall)/(precision+recall)

    print 'Right: %d'%right
    print 'Wrong: %d'%wrong
    print 'Precision: %s'%str(precision)
    print 'Recall: %s'%str(recall)
    print 'F1 Score: %s'%str(f1)

    db.close()

recommend_user(2, 5000)
