#!/usr/bin/python
# -*- coding: utf-8 -*-


def docFilter():

	#keyword=['歌','歌手','歌詞','バンド','アルバム']
	keyword=['アニメ','アニメーション','漫画','コミック']


	
	f_doc=open('wiki_ja_unprocessed.txt')
	#f_en_doc=open('en.txt')
	docs=f_doc.readlines()
	docList=[]
	#docs_en=f_en_doc.readlines()
	docWeight=[0]*len(docs)
	f_final=open('ja_AC.txt','wb')
	#f_en_final=open('en_AC.txt','wb')
	m=0
	docID=0
	for doc in docs:
		#docID=docs.index(doc)
		for i in keyword:
			if i in doc:
				docWeight[docID]+=1
		if docWeight[docID]>4:
			m+=1
			f_final.write(doc)
			docList.append(docID)
			#f_en_final.write(docs_en[docID])
		docID+=1
		if docID%5000==0:
			print 'No. %s'%str(docID)
	print m

	return docList

def creatDoc():
	docList=docFilter()
	f_doc=open('wiki_en_unprocessed.txt')
	docs=f_doc.readlines()
	f_final=open('en_AC.txt','wb')
	
	for i in docList:  
		f_final.write(docs[i])

if __name__ == '__main__':
	creatDoc()