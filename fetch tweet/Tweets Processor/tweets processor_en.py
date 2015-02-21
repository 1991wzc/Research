#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import nltk
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')  

def processor(Dir):

    count = 1

    f_final = open('en_tweet_final.txt', 'w')
    stopwords=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','wikipedia','encyclopedia','navigation','centralnotice',
    'april','may','june','july','august','september','october','november','december']

    final = ''
    print 'Start!'
    #读取tweets
    f1 = open(Dir, 'r')
    # 对于每一条tweet
    tweets = f1.readlines()
    for line in tweets:
        # 对于每一条tweet
        text = line.replace('\n', '')
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
                    f_final.write(word[0]+' ')
                elif word[1] == 'NNP':
                    f_final.write(word[0]+' ')
                # elif word[1] == 'NNPS':
                #     f_final.write(word[0]+' ')
                # elif word[1] == 'NNS':
                #     f_final.write(word[0]+' ')

        # 生成最终文档
        f_final.write('\n')
        count = count + 1
        if count % 100 == 0:
            print str(count) + ' tweets have been processed.'

    print 'Final file generated.'
    #f_ensw.close()
    f1.close()
    f_final.close()

    print 'Completed!'

def processor_user(usernum):
    path = os.getcwd()
    for i in range(usernum):
        title=str(i+1)
        print title

        count = 1

        f_final = open(path+'\\ac user tweets\\processed\\'+title+'_processed.txt', 'wb')
        stopwords=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','wikipedia','encyclopedia','navigation','centralnotice',
        'april','may','june','july','august','september','october','november','december']


        print 'Start!'
        #读取tweets
        f1 = open(path+'\\ac user tweets\\raw\\'+title+'.txt', 'r')
        # 对于每一条tweet
        tweets = f1.readlines()
        for line in tweets:
            # 对于每一条tweet
            text = line.replace('\n', '')
            # 去除标签和文本中的符号
            text = re.sub("http://\S*",'', text)
            text = re.sub("https://\S*",'', text)
            text = re.sub("@\S*",'', text)
            text = re.sub("<a href=.*</a>",'', text)
            text = text.replace('&gt;', ' ')
            text = text.replace('&lt;', ' ')
            text = text.replace('&quot;', ' ')
            text = text.replace('&amp;', ' ')
            # text = re.sub("[\[\]\|'\*;:\(\)-\./{}&=!%#]", ' ', text)
            # text = re.sub("<.+>", ' ', text)
            # text = re.sub("\=\=.+\=\=", ' ', text)
            text = re.sub("\W+", ' ', text)
            text = re.sub(" +", " ", text)
            text = text.lower()
            text=text.replace('rt', ' ')

            
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
                        f_final.write(word[0]+' ')
                    elif word[1] == 'NNP':
                        f_final.write(word[0]+' ')
                    # elif word[1] == 'NNPS':
                    #     f_final.write(word[0]+' ')
                    # elif word[1] == 'NNS':
                    #     f_final.write(word[0]+' ')

            # 生成最终文档
            f_final.write('\n')
            count = count + 1
            if count % 100 == 0:
                print str(count) + ' tweets have been processed.'

        print 'Final file generated.'
        #f_ensw.close()
        f1.close()
        f_final.close()

    print 'Completed!'

processor_user(5)
