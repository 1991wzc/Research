#!/usr/bin/python
# -*- coding: utf-8 -*-


import tweepy
import sys
import time
import string
import csv
import MySQLdb


def fetch_mysql_right():
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

	#keyword=['アニメ','アニメーション','漫画','コミック']
	keyword=['アニメ','漫画']
	topicword=['性格','彼女','自分', '関係', 'それ', '女性', '母親', '父親', '少女' ,'本人',
				'バス', 'ドラ', 'リトル', 'パン', 'ターズ', 'クリスタニア', 'angel', 'エルフ', 'beats', 'ノヴァ', 
				'収録', '作曲', '劇場', '編曲', '特典', '映像', 'テーマ', '映画', '音楽', '初回', 
				'パン', '吸血鬼', 'メディアファクトリー', 'ガールズ', '学園', 'ツァー', '月刊コミックアライブ', 'イヴ' ,'ブレイ', 'りす',
				'part', 'シーズン', 'マン', 'エイリアン', 'ベン', '日本語', '英語', 'ヒーロー', 'カートゥーン', 'パワー']
	#keyword=['歌','歌手','歌詞','バンド','アルバム']

	#f=open('id_count_ja_song.txt','a')
	count=0
	for i in topicword:
		for word in keyword:
			query=word+' '+i
			search_result = api.search(q=query, lang='ja', count=100)
			for tweet in search_result:
				# if tweet.user.id_str not in idlist:
				# 	f.write(tweet.user.id_str+' '+str(tweet.user.statuses_count)+'\n')

				if isinstance(tweet.text, unicode)==True:
					tweetText=tweet.text.replace('\n',' ')
					tweetText=tweetText.replace(',',' ')
					tweetText=tweetText.strip()

					sql="""INSERT INTO `mydb`.`ja_f1` (`tweet`,`related`) 
					VALUES ('%s',%d);""" % (tweetText,1)

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

					sql="""SELECT count(*) FROM mydb.ja_f1 where related=1;"""
					cursor.execute(sql)
					rows = cursor.fetchall()

					if rows[0][0]==20000:
						sys.exit()
	db.close()

class StreamListener(tweepy.StreamListener):
	def on_status(self, status):

		if status.lang=='ja':
			db = MySQLdb.connect("localhost","root","0000","mydb" )
			db.set_character_set('utf8')
			cursor = db.cursor()
			cursor.execute('SET NAMES utf8;')
			cursor.execute('SET CHARACTER SET utf8;')
			cursor.execute('SET character_set_connection=utf8;')

			tweetText=status.text
			sql="""INSERT INTO `mydb`.`ja_f1` (`tweet`,`related`) VALUES ('%s',%d);""" % (tweetText,0)
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()
				pass

			sql="""SELECT count(*) FROM mydb.ja_f1 where related=0;"""
			cursor.execute(sql)
			rows = cursor.fetchall()
			if rows[0][0]==20000:
				sys.exit()

			db.close()

def fetch_mysql_wrong():
	#db = MySQLdb.connect("localhost","root","0000","mydb" )


	reload(sys)
	sys.setdefaultencoding('utf8')


	ckey = 'uIefD73jTyjgVRSN6AjoehWtE'
	csecret = 'k6F12T7025bdlx3VW3nZhuyH0jI44EhaV97JDNGpeuDuMkcnJA'
	atoken = '1886636162-tcgnYgX7Z3qVV0zK6rcIIrO1IaUKl1yDGw91eVE'
	asecret = '683xhP4C04W7uUEKWaxLYDbMbGHPs3gVScP45dAFcNkPA'

	auth = tweepy.OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)

	stream = tweepy.Stream(auth, StreamListener())
	stream.sample()
	
#fetch_mysql_right()
fetch_mysql_wrong()