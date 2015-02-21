#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

path=os.getcwd()

number=50

#print path
lan='ja'
#f_en=open('en_tweet_final.txt','r')
#f_ja=open('ja_tweet_final.txt','r')
f_ja=open('tweets_ja_ac.txt')

#tweets_en=f_en.readlines()
tweets_ja=f_ja.readlines()


divide=len(tweets_ja)/number
count=0
start=0
for i in range(number):
	print 'File'+ str(i+1)
	f_final=open(path+'\\splitted\\f_final_'+lan+'-'+str(i)+'.txt','w')

	if i !=number-1:
		for tweet in tweets_ja[start:start+divide]:
			f_final.write(tweet)
		start+=divide
	elif i==number-1:
		for tweet in tweets_ja[start:]:
			f_final.write(tweet)

f_final.close()