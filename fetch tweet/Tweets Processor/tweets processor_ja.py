#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import MeCab
import os

count = 0
path = os.getcwd()


# stopwords=['年','日','月','こと','的','ため','出典','フリー','百科','事典','ウィキペディア','百科事典','検索','記事','ノート','ページ','目次','その他','できる','情報源',
# 'まり','編集','ジャンル','複数','文献','情報','概要','基本','要出典','種類','漫画','アニメ','作品','巻','原作','本','話','人物','ドラマ','コミックス','項目','日本','人','舞台','漫画家','編','作者','版',
# 'テレビアニメ','コミック','カテゴリ','漫画雑誌','巻数','エピソード','ゲーム','第','ストーリー','全','最終','題材','レーベル','名前','期間','外部','内容','人間','公式','男','番組']

stopwords = ['注釈','ー','年', '日', '月', 'こと', '的', 'ため', '出典', 'フリー', '百科', '事典', 'ウィキペディア', '百科事典', '検索', '記事', 'ノート', 'ページ', '目次', 'その他', 'できる', '情報源',
         'まり', '編集', 'ジャンル', '複数', '文献', '情報', '概要', '基本', '要出典', '種類','外部','ウィキ', 'ペ', 'ディア']

symbols = ['[', ']', '–', '・', '?', '\\', '（', '）', '）', '→', '☆', '@', '「', '〈', '〉',
           '」', '『', '』', '。', '、', '#', '&', '�', '！', 'ﾟ', 'ξ', '≡', 'д', '&', 'Ф', '=', '○']

f_final = open(path+'\\ac\\ja_tweet_final.txt', 'w')
print 'Start!'
# 读取tweets文件
f1 = open(path+'\\ac\\tweets_ja_ac.txt', 'r')

tweets= f1.readlines()

#print count
# 对于每一条tweet
for line in tweets:
    text=line.replace('\n', ' ')
    text = re.sub("http://\S*",'', text)
    text = re.sub("https://\S*",'', text)
    text = re.sub("@\S*",'', text)
    text = re.sub("<a href=.*</a>",'', text)
    # text = re.sub("[\[\]\|'\*;:\(\)-\./{}&=!%#]", ' ', text)
    #text = re.sub("\w+", ' ', text)
    text = re.sub("\w+年",'', text)
    text = re.sub("\w+月",'', text)
    text = re.sub("\w+日",'', text)
    text = re.sub(" +", ' ', text)
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
                        f_final.write(node.surface+' ')
                elif '名詞,一般,' in node.feature:
                    #print node.feature
                    f_final.write(node.surface+' ')           
        node = node.next

    # 生成最终文档(保留空白tweet，以便推荐)
    f_final.write('\n')
    count = count + 1
    #print str(count) + ' document have been processed.'
    if count % 1000 == 0:
        print str(count) + ' tweets have been processed.'

print 'Final file generated.'
#f_jasw.close()
f1.close()
f_final.close()
print 'Completed!'
