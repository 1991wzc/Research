#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import nltk
import os
import sys

def en_processor():
    path = os.getcwd()
    f_final = open('en_final.txt', 'wb')
    count = 1

    stopwords=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','wikipedia','encyclopedia','navigation',
    'search',
    'info','site','link','log','talk','history','ch','isbn','centralnotice','vf','ver','of','to']


    print 'Start English'

    f = open('en_song.txt','r')
    lines=f.xreadlines()

    for wiki in lines:

        text=(wiki.split('Search Navigation Main page Contents Featured content Current events Random article Donate to Wikipedia Wikimedia Shop Interaction Help About Wikipedia'))[0]

        # 去除标点
        text = text.replace('&gt;', ' ')
        text = text.replace('&lt;', ' ')
        text = text.replace('&quot;', ' ')
        text = text.replace('&amp;', ' ')
        text = re.sub("http://\S*",'', text)
        text = re.sub("https://\S*",'', text)

        # text = re.sub("[\[\]\|'\*;:\(\)-\./{}&=!%#]", ' ', text)
        # text = text.replace('\–', ' ')
        # text = text.replace('\\', ' ')

        text = re.sub("\W+", ' ', text)
        text = re.sub(" +", " ", text)
        text = text.lower()

        # 词形还原
        lemma = nltk.WordNetLemmatizer()
        tokens = nltk.word_tokenize(text)

        untagged=list()
        for word in tokens:
            #词形还原            
            word=lemma.lemmatize(word)
            untagged.append(str(word))

        #标记词性
        #untagged=nltk.word_tokenize(text)
        tagged=nltk.pos_tag(untagged)

        for word in tagged:
            #去除停用词，只保留名词
            if word[0] not in stopwords:          
                if word[1] == 'NN' or word[1] == 'NNP':
                    f_final.write(word[0]+' ')

        f_final.write('\n')
        count = count + 1
        print count
        if count % 100 == 0:
            print str(count) + ' document have been processed.'
    f.close()

    #f_ensw.close()
    f_final.close()
    print 'Completed!'

reload(sys)
sys.setdefaultencoding('utf-8') 
en_processor()