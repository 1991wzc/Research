#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import nltk
from nltk.stem import SnowballStemmer

def en_processor(text):

    postags=[
    #'JJ','JJR','JJS',
    'NN','NNP'
    ,'VB','VBD','VBG','VBN','VBP','VBZ'
    #,'RB','RBR','RBS'
    ]

    # stopwords=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','wikipedia','encyclopedia','navigation','centralnotice',
    # 'april','may','june','july','august','september','october','november','december']

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

    #text = re.sub("\W+", ' ', text)
    text = re.sub(" +", " ", text)
    text = text.lower()

    # 词形还原
    lemma = nltk.WordNetLemmatizer()
    tokens = nltk.word_tokenize(text)
    #st = SnowballStemmer("english")

    final=str()
    untagged=list()
    for word in tokens:
        #词形还原
        word=lemma.lemmatize(word)
        #word=st.stem(word)
        untagged.append(str(word))

    #标记词性
    tagged=nltk.pos_tag(untagged)

    final=str()
    for word in tagged:
        #去除停用词，只保留名词
        if len(word[0])>2:          
            if word[1] in postags:
                final+=word[0]+' '

    return final