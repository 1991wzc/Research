#!/usr/bin/python
# -*- coding: utf-8 -*-


import tweepy
import sys
import time
import os


def get_all_tweets(user_id):

	consumer_key = 'uIefD73jTyjgVRSN6AjoehWtE'
	consumer_secret = 'k6F12T7025bdlx3VW3nZhuyH0jI44EhaV97JDNGpeuDuMkcnJA'
	access_key = '1886636162-tcgnYgX7Z3qVV0zK6rcIIrO1IaUKl1yDGw91eVE'
	access_secret = '683xhP4C04W7uUEKWaxLYDbMbGHPs3gVScP45dAFcNkPA'
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(user_id = user_id,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(user_id = user_id,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))

		#if len(alltweets)%3200==0:
	print 'Write to file.'
	outtweets = [tweet.text for tweet in alltweets]
	for tweet in outtweets:
		f_en.write(tweet.replace('\n',' ')+'\n')


def getTweetByList():
	reload(sys)
	sys.setdefaultencoding('utf8')
	path=os.getcwd()
	#alltweets = []
	f=open('id_statuscount.txt')
	lines=f.readlines()
	userno=0
	for line in lines:
		userID=int((line.split())[0])
		if userno<962 :
			userno+=1
			continue
		#oldestID=get_oldestID(userID)
		# if userno==1000:			
		# 	exit()
		else:
			f_en = open(path+'\\user_tweets\\'+'en_'+str(userno)+'.txt', 'w')
			f_en.write('')
			f_en = open(path+'\\user_tweets\\'+'en_'+str(userno)+'.txt', 'a')
			#f_en.write(str(userID)+'\n')
			#pass in the userid of the account you want to download
			print 'No.'+str(userno)
			try:
				get_all_tweets(userID)
			except:
				print 'Sleeping.'
				time.sleep(240)
				continue		
			f_en.write(str(userID))
			print 'Sleeping.'
			time.sleep(240)
			userno+=1
			if userno%500==0:
				print str(userno)+' users\' tweets collected.'

reload(sys)
sys.setdefaultencoding('utf8')
f_en = open('5.txt', 'wb')
get_all_tweets(18089213)
f_en.close()
