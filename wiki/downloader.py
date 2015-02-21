#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import sys
from bs4 import BeautifulSoup
import re
import time
import socket

def downlodaArticles():
	reload(sys)
	sys.setdefaultencoding('utf8')

	f_title=open('titles.txt','r')

	titles=f_title.readlines()

	#f_ja=open('wikipedia_ja.txt','w')
	#f_ja.write('')
	f_ja=open('wikipedia_ja.txt','a')

	#f_en=open('wikipedia_en.txt','w')
	#f_en.write('')
	f_en=open('wikipedia_en.txt','a')

	docnum=1
	socket.setdefaulttimeout(10)
	print 'Start!'
	for title in titles:
		if docnum < 0:
			docnum+=1
			#print str(docnum)+'th page.'
		else:
			#try:
			print str(docnum)+'th page.'
			#get Japanese page by title
			try:
				doc_ja=urllib.urlopen('http://ja.wikipedia.org/wiki/'+title).read()
			except IOError:
				print 'IOError, continue'
				docnum+=1
				continue

			parser_ja = BeautifulSoup(''.join(doc_ja))
			#find related English page
			en_Label=parser_ja.find(attrs={"class":"interlanguage-link interwiki-en"})
			#if have related English page, write Japanese and English content into file
			if en_Label!=None:		
				#get link for English page
				en_link=en_Label.a['href']
				#get English page by link
				
				try:
					doc_en=urllib.urlopen('http:'+en_link).read()

				except IOError:
					print 'IOError, continue'
					docnum+=1
					continue


				parser_en=	BeautifulSoup(''.join(doc_en))
				#print parser_ja.html.body
				#write Japanese content
				old=''
				for text in parser_ja.html.body.strings:
					if text!=None and text!= old:
						text=text.replace('\n',' ')
						f_ja.write(text+' ')
						text=old
						

				#write English content
				for text in parser_en.html.body.strings:
					if text!=None:
						text=text.replace('\n',' ')
						f_en.write(text+' ')

				f_en.write('\n')
				print str(docnum)+'th page writed.'
				exit()
			docnum+=1

def downloadJAtitles():
	reload(sys)
	sys.setdefaultencoding('utf8')

	f_title=open('jawiki-latest-all-titles.txt','r')

	titles=f_title.readlines()

	f_ja=open('ja_titles.txt','wb')

	docnum=1
	socket.setdefaulttimeout(10)
	print 'Start!'
	for title in titles:
		if docnum < 0:
			docnum+=1
			#print str(docnum)+'th page.'
		else:
			#try:
			print str(docnum)+'th page.'
			#get Japanese page by title
			try:
				doc_ja=urllib.urlopen('http://ja.wikipedia.org/wiki/'+title).read()
			except IOError:
				print 'IOError, continue'
				docnum+=1
				continue

			parser_ja = BeautifulSoup(''.join(doc_ja))

			f_ja.write(parser_ja.html.title.string+'\n')

			docnum+=1

	f_ja.close()

	

def test():
	reload(sys)
	sys.setdefaultencoding('utf8')

	socket.setdefaulttimeout(10)
	#get Japanese page by title
	try:
		doc_ja=urllib.urlopen('http://ja.wikipedia.org/wiki/連邦通信委員会').read()
	except IOError:
		print 'IOError, continue'

	parser_ja = BeautifulSoup(''.join(doc_ja))
	#find related English page
	en_Label=parser_ja.find(attrs={"class":"interlanguage-link interwiki-en"})
	#if have related English page, write Japanese and English content into file
	if en_Label!=None:		
		#get link for English page
		en_link=en_Label.a['href']
		#get English page by link
		
		try:
			doc_en=urllib.urlopen('http:'+en_link).read()

		except IOError:
			print 'IOError, continue'

		parser_en=	BeautifulSoup(''.join(doc_en))
		for i in parser_ja.html.body.strings:
			print i.replace('\n','')
		#write Japanese content
		old=str()
		for text in parser_ja.html.body.strings:
			if text!=None and text!=old:
				text=text.replace('\n',' ')
				old=text

		#write English content
		for tag in parser_en.html.body.findAll():
			if tag.string!=None:
				text=tag.string.replace('\n',' ')

downlodaArticles()