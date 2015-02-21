#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import nltk
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')  

def process(text):

    f_final = open('en_tweet_final.txt', 'w')
    
    stopwords=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','wikipedia','encyclopedia','navigation','centralnotice',
    'april','may','june','july','august','september','october','november','december']

    final = ''

    text = text.replace('\n', '')
    # 去除标签和文本中的符号
    text = re.sub("http://\S*",'', text)
    text = re.sub("https://\S*",'', text)
    text = re.sub("@\S*",'', text)
    text = re.sub("<a href=.*</a>",'', text)
    # text = re.sub("[\[\]\|'\*;:\(\)-\./{}&=!%#]", ' ', text)
    text = text.replace('&gt;', ' ')
    text = text.replace('&lt;', ' ')
    text = text.replace('&quot;', ' ')
    text = text.replace('&amp;', ' ')
    # text = re.sub("<.+>", ' ', text)
    # text = re.sub("\=\=.+\=\=", ' ', text)
    text = re.sub("\W+", ' ', text)
    text = re.sub(" +", " ", text)
    text = text.lower()
    text=text.replace('rt ', ' ')
    
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
        if word[0] not in stopwords and len(word[0])>2:            
            if word[1] == 'NN':
                final+=word[0]+' '
            elif word[1] == 'NNP':
                final+=word[0]+' '

    return final

