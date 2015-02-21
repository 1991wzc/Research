#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import nltk
import MeCab
import os

f=open('wiki_ja_unprocessed.txt')
f_titltes=open('wikititles_ja.txt','wb')
count=0
for line in f.xreadlines():
	spl=line.split('出典: フリー百科事典『ウィキペディア（Wikipedia）』')
	t=spl[0].strip()
	spl2=t.split(' ')
	title=str()
	for i in spl2:
		if spl2.index(i)!=0:
			title+=i+' '
	title=title.strip()
	title=title.replace('amp;', '')
	f_titltes.write(title+'\n')
	count+=1
	if count%50000==0:
		print '%s titles.'%str(count)
f_titltes.close()