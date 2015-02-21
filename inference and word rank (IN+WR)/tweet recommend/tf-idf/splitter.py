#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

path=os.getcwd()

#print path

#f_en=open('tf_idf_en.txt','r')
f_ja=open('tf_idf_ja.txt','r')

#tweets_en=f_en.readlines()
tweets_ja=f_ja.readlines()

# divide=len(tweets_en)/10
# count=0
# start=0
# for i in range(10):
# 	print 'File'+ str(i+1)
# 	f_final=open(path+'\\splitted\\tf_idf_en-'+str(i)+'.txt','w')
# 	f_final.write('')
# 	f_final=open(path+'\\splitted\\tf_idf_en-'+str(i)+'.txt','a')
# 	if i !=9:
# 		for tweet in tweets_en[start:start+divide]:
# 			f_final.write(tweet)
# 		start+=divide
# 	if i==9:
# 		for tweet in tweets_en[start:]:
# 			f_final.write(tweet)

divide=len(tweets_ja)/50
count=0
start=0
for i in range(50):
	print 'File '+ str(i+1)
	f_final=open(path+'\\splitted\\tf_idf_ja-'+str(i)+'.txt','w')
	f_final.write('')
	f_final=open(path+'\\splitted\\tf_idf_ja-'+str(i)+'.txt','a')
	if i !=49:
		for tweet in tweets_ja[start:start+divide]:
			f_final.write(tweet)
		start+=divide
	if i==49:
		for tweet in tweets_ja[start:]:
			f_final.write(tweet)
