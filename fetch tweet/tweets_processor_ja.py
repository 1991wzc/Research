#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import MeCab

def process(text):
    stopwords = ['注釈','ー','年', '日', '月', 'こと', '的', 'ため', '出典', 'フリー', '百科', '事典', 'ウィキペディア', '百科事典', '検索', '記事', 'ノート', 'ページ', '目次', 'その他', 'できる', '情報源',
             'まり', '編集', 'ジャンル', '複数', '文献', '情報', '概要', '基本', '要出典', '種類','外部','ウィキ', 'ペ', 'ディア']

    symbols = ['[', ']', '–', '・', '?', '\\', '（', '）', '）', '→', '☆', '@', '「', '〈', '〉',
               '」', '『', '』', '。', '、', '#', '&', '�', '！', 'ﾟ', 'ξ', '≡', 'д', '&', 'Ф', '=', '○']

    final=''
    #print count
    # 对于每一条tweet
    text=text.replace('\n', ' ')
    text = re.sub("http://\S*",'', text)
    text = re.sub("https://\S*",'', text)
    text = re.sub("@\S*",'', text)
    text = re.sub("<a href=.*</a>",'', text)
    # text = re.sub("[\[\]\|'\*;:\(\)-\./{}&=!%#]", ' ', text)
    #text = re.sub("\w", ' ', text)
    text = re.sub(" +", ' ', text)
    text = re.sub("\w+年",'', text)
    text = re.sub("\w+月",'', text)
    text = re.sub("\w+日",'', text)
    text=text.lower()
    text=text.replace('rt ', ' ')
    #print text

    # 分词+标记词性
    m = MeCab.Tagger("mecabrc")  
    node = m.parseToNode(text)
    # only nouns
    while node:
        #print node.feature
        if '名詞,' in node.feature and len(node.surface)>3:
            if node.surface not in stopwords and node.surface not in symbols:
                if '名詞,固有名詞,' in node.feature:
                    #if '名詞,固有名詞,人名,名,' not in node.feature:
                        #print node.feature
                        final+=node.surface+' '
                elif '名詞,一般,' in node.feature:
                    #print node.feature
                    final+=node.surface+' '          
        node = node.next

    return final
