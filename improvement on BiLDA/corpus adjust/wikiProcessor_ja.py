#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import MeCab

def ja_processor(text):

    stopwords = ['注釈','ー','年', '日', '月', 'こと', '的', 'ため', '出典', 'フリー', '百科', '事典', 'ウィキペディア', '百科事典', '検索', '記事', 'ノート', 'ページ', '目次', 'その他', 'できる', '情報源',
             'まり', '編集', 'ジャンル', '複数', '文献', '情報', '概要', '基本', '要出典', '種類','外部','ウィキ', 'ペ', 'ディア',
             'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'wikipedia', 'encyclopedia', 'navigation',
             'search', 'com', 'edit', 'info', 'site',  'link', 'log', 'ch', 'isbn', 'centralnotice', 'th', 'bb', 'ii', 'co', 'ltd', 'the','vf','ver','vol',
             'about','above','after','again','against','all','am','an','and','any','are','as','at','be','because','been','before','being','below','between','both','but','by','could','did','do','does','doing','down','during',
             'each',',few','for','from','further','had','has','have','having','he','her','here','hers','herself','him','himself','his','how','i','if','in','into','is','it','its','itself','me','more','most','my','myself',
             'no','nor','not','of','off','on','once','only','or','other','ought','our','ours','ourselves','out','over','own','same','she','should','so','some','such','than','that','the','their','theirs','them',
             'themselves','then','there','these','they','this','those','through','to','too','under','until','up','very','was','we','were','what','when','where','which','while','who','whom','why','with','would','you',
             'your','yours','yourself','yourselves','category','january','february','march','april','may','june','july','august','september','october','november','december']

    symbols = ['[', ']', '–', '・', '?', '\\', '（', '）', '）', '→', '☆', '@', '「', '〈', '〉',
               '」', '『', '』', '。', '、', '#', '&', '�', '！', 'ﾟ', 'ξ', '≡', 'д', '&', 'Ф', '=', '○']


    text = text.replace('&gt;', ' ')
    text = text.replace('&lt;', ' ')
    text = text.replace('&quot;', ' ')
    text = text.replace('&amp;', ' ')
    text = re.sub("http://\S*", '', text)
    text = re.sub("https://\S*", '', text)
    text = re.sub("\w+年", '', text)
    text = re.sub("\w+月", '', text)
    text = re.sub("\w+日", '', text)

    #text = re.sub("\w+", ' ', text)
    text = re.sub(" +", ' ', text)
    text = text.lower()
    # print text

    # 分词+标记词性
    m = MeCab.Tagger("mecabrc")
    node = m.parseToNode(text)

    # only nouns
    final=str()
    while node:
        if '名詞,' in node.feature and len(node.surface)>3:
            if node.surface not in stopwords and node.surface not in symbols:
                if '名詞,固有名詞,' in node.feature:
                    final+=node.surface + ' '

                elif '名詞,一般,' in node.feature:
                    final+=node.surface + ' '
        node = node.next

    return final
