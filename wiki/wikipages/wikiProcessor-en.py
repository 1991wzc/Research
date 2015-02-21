#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import nltk
from nltk.stem import SnowballStemmer
import os
import sys

def en_processor(filename):
    path = os.getcwd()
    f_final = open(filename+'_final.txt', 'wb')
    count = 1

    stopwords=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','wikipedia','encyclopedia','navigation','centralnotice',
    'april','may','june','july','august','september','october','november','december']


    print 'Start English'

    f = open(filename+'.txt')
    lines=f.xreadlines()

    for text in lines:

        # text=(wiki.split('Search Navigation Main page Contents Featured content Current events Random article Donate to Wikipedia Wikimedia Shop Interaction Help About Wikipedia'))[0]

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
        #st = SnowballStemmer("english")

        untagged=list()
        for word in tokens:
            #词形还原            
            word=lemma.lemmatize(word)
            #word=st.stem(word)
            untagged.append(str(word))

        #标记词性
        #untagged=nltk.word_tokenize(text)
        tagged=nltk.pos_tag(untagged)

        for word in tagged:
            #去除停用词，只保留名词
            if word[0] not in stopwords and len(word[0])>2:          
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
en_processor('en_AC_all')