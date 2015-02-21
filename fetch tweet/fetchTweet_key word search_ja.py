#!/usr/bin/python
# -*- coding: utf-8 -*-


import tweepy
import sys
import time
import string
import csv
import MySQLdb


def fetch_mysql():
	#db = MySQLdb.connect("localhost","root","0000","mydb" )


	reload(sys)
	sys.setdefaultencoding('utf8')

	db = MySQLdb.connect("localhost","root","0000","mydb" )
	db.set_character_set('utf8')
	cursor = db.cursor()
	cursor.execute('SET NAMES utf8;')
	cursor.execute('SET CHARACTER SET utf8;')
	cursor.execute('SET character_set_connection=utf8;')

	ckey = 'uIefD73jTyjgVRSN6AjoehWtE'
	csecret = 'k6F12T7025bdlx3VW3nZhuyH0jI44EhaV97JDNGpeuDuMkcnJA'
	atoken = '1886636162-tcgnYgX7Z3qVV0zK6rcIIrO1IaUKl1yDGw91eVE'
	asecret = '683xhP4C04W7uUEKWaxLYDbMbGHPs3gVScP45dAFcNkPA'

	auth = tweepy.OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)

	api = tweepy.API(auth)

	keyword=['アニメ','アニメーション','漫画','コミック']
	#keyword=['歌','歌手','歌詞','バンド','アルバム']

	#f=open('id_count_ja_song.txt','a')
	count=0

	for word in keyword:

		search_result = api.search(q=word, lang='ja', count=200)
		for tweet in search_result:
			# if tweet.user.id_str not in idlist:
			# 	f.write(tweet.user.id_str+' '+str(tweet.user.statuses_count)+'\n')

			if isinstance(tweet.text, unicode)==True:
				tweetText=tweet.text.replace('\n',' ')
				tweetText=tweetText.replace(',',' ')
				tweetText=tweetText.strip()

				sql="""INSERT INTO `mydb`.`ja_ac` (`ac`) 
				VALUES ('%s');""" % tweetText

				try:
					cursor.execute(sql)
					db.commit()
					count+=1
					#print count
					if count %100==0:
						print '%s tweets.'%str(count)
				except:
					db.rollback()
					continue
	db.close()

# idlist=list()

# f=open('id_count_ja_song.txt')

# for line in f.xreadlines():
# 	split=line.split()
# 	idlist.append(split[0])

while True:
	try:
		fetch_mysql()
		print 'Sleeping...'
		time.sleep(60)			
	except:
		continue
