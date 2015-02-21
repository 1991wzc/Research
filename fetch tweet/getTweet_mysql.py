# -*- coding: UTF-8 -*-

import MySQLdb
import sys
import tweets_processor_ja
import tweets_processor_en

def fetch_f1():
    f = open('ja_f1.txt', 'w')
    # 连接mysql，获取连接的对象
    db = MySQLdb.connect("localhost", "root", "0000", "mydb")

    with db:
        # 仍然是，第一步要获取连接的cursor对象，用于执行查询
        cur = db.cursor()
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        # 类似于其他语言的query函数，execute是python中的执行查询函数
        cur.execute("SELECT * FROM ja_f1;")
        # print cur.execute("SELECT count(*) FROM en_tweet where ac!='NULL';")
        # 使用fetchall函数，将结果集（多维元组）存入rows里面
        rows = cur.fetchall()

        # 依次遍历结果集，发现每个元素，就是表中的一条记录，用一个元组来显示
        count = 0
        for row in rows:            
            processed=tweets_processor_ja.process(row[1])
            f.write(processed + '\n')
            count += 1
            if count % 1000 == 0:
                print '%d tweets.' % count
        print count
        f.close()

def fetch_en():
    f = open('en_final_ac.txt', 'w')
    # 连接mysql，获取连接的对象
    db = MySQLdb.connect("localhost", "root", "0000", "mydb")

    with db:
        # 仍然是，第一步要获取连接的cursor对象，用于执行查询
        cur = db.cursor()
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        # 类似于其他语言的query函数，execute是python中的执行查询函数
        cur.execute("SELECT * FROM en_ac;")
        # print cur.execute("SELECT count(*) FROM en_tweet where ac!='NULL';")
        # 使用fetchall函数，将结果集（多维元组）存入rows里面
        rows = cur.fetchall()

        # 依次遍历结果集，发现每个元素，就是表中的一条记录，用一个元组来显示
        count = 0
        for row in rows:            
            processed=tweets_processor_en.process(row[1])
            f.write(processed + '\n')
            count += 1
            if count % 1000 == 0:
                print '%d tweets.' % count
        print count
        f.close()


def fetch_ja():
    f = open('ja_final_ac.txt', 'w')
    # 连接mysql，获取连接的对象
    db = MySQLdb.connect("localhost", "root", "0000", "mydb")

    with db:
        # 仍然是，第一步要获取连接的cursor对象，用于执行查询
        cur = db.cursor()
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        # 类似于其他语言的query函数，execute是python中的执行查询函数
        cur.execute("SELECT * FROM ja_ac;")
        # print cur.execute("SELECT count(*) FROM en_tweet where ac!='NULL';")
        # 使用fetchall函数，将结果集（多维元组）存入rows里面
        rows = cur.fetchall()

        # 依次遍历结果集，发现每个元素，就是表中的一条记录，用一个元组来显示
        count = 0
        for row in rows:            
            processed=tweets_processor_ja.process(row[1])
            f.write(processed + '\n')
            count += 1
            if count % 1000 == 0:
                print '%d tweets.' % count
        print count
        f.close()

fetch_ja()
