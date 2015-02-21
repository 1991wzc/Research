#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

path=os.getcwd()

number=30

#print path

#f_en=open('en_tweet_final.txt','r')
#f_ja=open('ja_tweet_final.txt','r')
f_ja=open('ja_tweet_final.txt','r')

#tweets_en=f_en.readlines()
tweets_ja=f_ja.readlines()


divide=len(tweets_ja)/number
count=0
start=0
for i in range(number):
	print 'File'+ str(i+1)
	f_final=open(path+'\\splitted\\f_final_ja-'+str(i)+'.txt','w')
	f_final.write('')
	f_final=open(path+'\\splitted\\f_final_ja-'+str(i)+'.txt','a')
	if i !=number-1:
		for tweet in tweets_ja[start:start+divide]:
			f_final.write(tweet)
		start+=divide
	elif i==number-1:
		for tweet in tweets_ja[start:]:
			f_final.write(tweet)
