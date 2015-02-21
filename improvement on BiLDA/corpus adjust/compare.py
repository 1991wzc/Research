#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import goslate
import sys
import random
import wikiProcessor_en
import wikiProcessor_ja
import math
import os

class constructor():

	unprocessed_en=list()
	unprocessed_ja=list()
	translated_ja=list()
	processed_en=list()
	processed_ja=list()

	word2id=dict()

	en_all=list()
	ja_all=list()

	doclist=list()

	def sentence(self,dir_en,dir_ja):
		f_en=open(dir_en)
		f_ja=open(dir_ja)
		f_len_en=open('sentence_en_all.txt','wb')
		f_len_ja=open('sentence_ja_all.txt','wb')


		en=f_en.readlines()
		ja=f_ja.readlines()

		for i in range(len(ja)):
			t_ja=(ja[i].split('http://ja.wikipedia.org/w/index.php?title='))[0]
			t_en=(en[i].split('http://en.wikipedia.org/w/index.php?title='))[0]
			l_ja=len(t_ja.split('。'))
			l_en=len(t_en.split('. '))
			f_len_en.write(str(l_en)+'\n')
			f_len_ja.write(str(l_ja)+'\n')

			if i%50000==0:
				print '%d docs.'%i

		f_en.close
		f_ja.close
		f_len_en.close
		f_len_ja.close

	def random_lineno(self,ratio,minimum,maximum):
		f_en=open('sentence_en.txt')
		f_ja=open('sentence_ja.txt')

		en=f_en.readlines()
		ja=f_ja.readlines()

		linelist=list()
		for i in range(len(ja)):
			if ratio<(int(ja[i])/int(en[i]))<(1/ratio) and maximum>int(ja[i])>minimum:
				linelist.append(i)

		lineno=linelist[int(len(linelist)*random.random())]
		print lineno
		return lineno

	def tf_idf(self,sentences):
		print 'Calculate TF-IDF.'
		df=dict()
		tf=[0]*len(sentences)
		tf_idf=[0]*len(sentences)

		for ID in self.word2id.values():
			df[ID]=0
		for i in range(len(sentences)):
			tf[i]=dict()
			exsit=[]
			for j in range(len(sentences[i])):
				tf[i][sentences[i][j]]=sentences[i].count(sentences[i][j])
				if sentences[i][j] not in exsit:
					df[sentences[i][j]]+=1
					exsit.append(sentences[i][j])

		for i in range(len(sentences)):
			tf_idf[i]=dict()
			for wordid in tf[i].keys():
				tf_idf[i][wordid]=tf[i][wordid]* math.log(len(sentences) / df[wordid])

		return tf_idf
		

	def cosine(self,tf_idf_v1,tf_idf_v2):

		if len(tf_idf_v1)==0 or len(tf_idf_v2)==0:
			return 0.0
		else:
			xx=0
			yy=0
			xy=0
			for value in tf_idf_v1.values():
				xx+=value*value
			for value in tf_idf_v2.values():
				yy+=value*value
			for wordid in tf_idf_v1.keys():
				if wordid in tf_idf_v2.keys():
					xy+=tf_idf_v1[wordid]*tf_idf_v2[wordid]
			return xy/math.sqrt(xx * yy)


	def get_doc(self,lineno):
		
		print 'Choose doc %d'%lineno	


		en=self.en_all[lineno]
		ja=self.ja_all[lineno]

		en=(en.split('http://en.wikipedia.org/w/index.php?title='))[0]
		ja=(ja.split('http://ja.wikipedia.org/w/index.php?title='))[0]

		sentence_en=en.split('. ')
		sentence_ja=ja.split('。')

		self.unprocessed_en=[]
		self.unprocessed_ja=[]
		self.translated_ja=[]

		#if ratio<(len(sentence_en)/len(sentence_ja))<(1/ratio):

		gs = goslate.Goslate()
		for i in sentence_en:
			translated=gs.translate(i, 'en')
			self.unprocessed_en.append(translated)

		for i in sentence_ja:
			self.unprocessed_ja.append(i)
			translated=gs.translate(i, 'en')
			self.translated_ja.append(translated)

		# else:
		# 	return 0

	def process(self):

		self.processed_en=[]
		self.processed_ja=[]

		print 'Start English!'
		for i in self.unprocessed_en:
			procssed=wikiProcessor_en.en_processor(i)
			self.processed_en.append(procssed)
		print 'Complete!'

		
		print 'Start Translated!'
		for i in self.translated_ja:
			procssed=wikiProcessor_en.en_processor(i)
			self.processed_ja.append(procssed)

		print 'Complete!'

	def compare(self,number):
		path=os.getcwd()

		sentence_en=[0]*len(self.processed_en)
		sentence_ja=[0]*len(self.processed_ja)

		for i in range(len(self.processed_en)):
			en=self.processed_en[i].replace('\n',' ')
			words=en.split()
			sentence_en[i]=[0]*len(words)
			for j in range(len(words)):
				if words[j] not in self.word2id:
					self.word2id[words[j]]=len(self.word2id)
				sentence_en[i][j]=self.word2id[words[j]]

		for i in range(len(self.processed_ja)):
			ja=self.processed_ja[i].replace('\n',' ')
			words=ja.split()
			sentence_ja[i]=[0]*len(words)
			for j in range(len(words)):
				if words[j] not in self.word2id:
					self.word2id[words[j]]=len(self.word2id)
				sentence_ja[i][j]=self.word2id[words[j]]


		tf_idf_ja=self.tf_idf(sentence_ja)
		tf_idf_en=self.tf_idf(sentence_en)

		#consider length of Englsih and length of Japanese

		f_combine_en=open(path+'\\final\\en_AC.txt','ab')
		f_combine_ja=open(path+'\\final\\ja_AC.txt','ab')

		f_all_en=open(path+'\\final\\en_AC_all.txt','ab')
		f_all_ja=open(path+'\\final\\ja_AC_all.txt','ab')

		f_all_en.write(str(number)+' '+self.en_all[number])
		f_all_ja.write(str(number)+' '+self.ja_all[number])
		f_combine_en.write(str(number)+' ')
		f_combine_ja.write(str(number)+' ')
		# f_remain_en=open(path+'\\final\\en_AC_remain.txt','ab')
		# f_remain_ja=open(path+'\\final\\ja_AC_remain.txt','ab')

		#f_final_allocated=open(path+'\\final\\%d_final_allocated.txt'%number,'wb')
		# f_final_en=open(path+'\\final\\%d_final_en.txt'%number,'wb')
		# f_final_ja=open(path+'\\final\\%d_final_ja.txt'%number,'wb')

		# f_unprocessed_en=open(path+'\\final\\%d_unprocessed_en.txt'%number,'wb')
		# f_unprocessed_ja=open(path+'\\final\\%d_unprocessed_ja.txt'%number,'wb')
		# for i in self.unprocessed_en:
		# 	f_unprocessed_en.write(i+'\n')
		# for i in self.unprocessed_ja:
		# 	f_unprocessed_ja.write(i+'\n')
		# f_unprocessed_en.close()
		# f_unprocessed_ja.close()

		# f_processed_en=open(path+'\\final\\%d_processed_en.txt'%number,'wb')
		# f_processed_ja=open(path+'\\final\\%d_processed_ja.txt'%number,'wb')
		# for i in self.processed_en:
		# 	f_processed_en.write(i+'\n')
		# for i in self.processed_ja:
		# 	f_processed_ja.write(i+'\n')
		# f_processed_ja.close()
		# f_processed_en.close()

		# f_tfidf_en=open(path+'\\final\\%d_tfidf_en.txt'%number,'wb')
		# f_tfidf_ja=open(path+'\\final\\%d_tfidf_ja.txt'%number,'wb')
		# for sentence in tf_idf_ja:
		# 	for value in sentence.values():
		# 		f_tfidf_ja.write(str(value)+' ')
		# 	f_tfidf_ja.write('\n')
		# for sentence in tf_idf_en:
		# 	for value in sentence.values():
		# 		f_tfidf_en.write(str(value)+' ')
		# 	f_tfidf_en.write('\n')
		# f_tfidf_en.close()
		# f_tfidf_ja.close()

		if len(sentence_en)>=len(sentence_ja):
			#assign English sentences to Japanese
			print 'English is longer.'
			print 'Pair format Japanese:English.'
			pair=dict()
			score_dict=dict()
			score=[0]*len(sentence_en)
			for i in range(len(sentence_en)):
				score[i]=[0]*len(sentence_ja)
				for j in range(len(sentence_ja)):
					score[i][j]=self.cosine(tf_idf_en[i],tf_idf_ja[j])
					score_dict[(j,i)]=score[i][j]

			score_dict= sorted(score_dict.iteritems(), key=lambda d:d[1], reverse = True)
			for i in score_dict:
				if i[1]!=0.0:
					if i[0][0] not in pair:
						if i[0][1] not in pair.values():
							pair[i[0][0]]=i[0][1]


			for i in pair:
#				f_final_allocated.write(self.unprocessed_en[pair[i]]+'\n'+self.unprocessed_ja[i]+'\n\n')

				f_combine_en.write(self.unprocessed_en[pair[i]]+' ')
				f_combine_ja.write(self.unprocessed_ja[i]+' ')

			# for i in range(len(self.unprocessed_en)):
			# 	if i not in pair.values():
			# 		f_final_en.write(self.unprocessed_en[i]+'\n')
			# 		f_remain_en.write(self.unprocessed_en[i])
			
			# for i in range(len(self.unprocessed_ja)):
			# 	if i not in pair.keys():
			# 		f_final_ja.write(self.unprocessed_ja[i]+'\n')
			# 		f_remain_ja.write(self.unprocessed_ja[i])


		elif len(sentence_en)<len(sentence_ja):
			#assign Japanese sentences to English
			print 'Japanese is longer.'
			print 'Pair format English:Japanese.'
			pair=dict()
			score_dict=dict()
			score=[0]*len(sentence_en)
			for i in range(len(sentence_en)):
				score[i]=[0]*len(sentence_ja)
				for j in range(len(sentence_ja)):
					score[i][j]=self.cosine(tf_idf_en[i],tf_idf_ja[j])
					score_dict[(i,j)]=score[i][j]

			score_dict= sorted(score_dict.iteritems(), key=lambda d:d[1], reverse = True)
			for i in score_dict:
				if i[1]!=0.0:
					if i[0][0] not in pair:
						if i[0][1] not in pair.values():
							pair[i[0][0]]=i[0][1]

			for i in pair:
#				f_final_allocated.write(self.unprocessed_en[i]+'\n'+self.unprocessed_ja[pair[i]]+'\n\n')
				f_combine_en.write(self.unprocessed_en[i]+' ')
				f_combine_ja.write(self.unprocessed_ja[pair[i]]+' ')

			# for i in range(len(self.unprocessed_en)):
			# 	if i not in pair.keys():
			# 		#print i
			# 		f_final_en.write(self.unprocessed_en[i]+'\n')
			# 		f_remain_en.write(self.unprocessed_en[i])
			
			# for i in range(len(self.unprocessed_ja)):
			# 	if i not in pair.values():
			# 		f_final_ja.write(self.unprocessed_ja[i]+'\n')
			# 		f_remain_ja.write(self.unprocessed_ja[i])

		f_combine_ja.write('\n')
		f_combine_en.write('\n')
		# f_remain_ja.write('\n')
		# f_remain_en.write('\n')

		f_combine_ja.close()
		f_combine_en.close()
		f_all_ja.close()
		f_all_en.close()
		# f_remain_ja.close()
		# f_final_allocated.close()
		# f_final_ja.close()
		# f_final_en.close()

	def get_doclist(self):
		f_en_sen=open('sentence_en_all.txt')
		f_ja_sen=open('sentence_ja_all.txt')
		sen_en=f_en_sen.readlines()
		sen_ja=f_ja_sen.readlines()

		# count_en=0
		# for i in sen_en:
		# 	if int(i)>18.419625718*10:
		# 		count_en+=1
		# print count_en

		# count_ja=0
		# for i in sen_ja:
		# 	if int(i)>7.76499169811*10:
		# 		count_ja+=1
		# print count_ja

		# average en 18.419625718
		# average ja 7.76499169811

		ratio=0.5
		count=0
		self.doclist=list()
		for i in range(len(sen_en)):
			if ratio<int(sen_ja[i])/int(sen_en[i])<1/ratio and int(sen_ja[i])>7.76499169811*5:
				count+=1
				self.doclist.append(i)
		print count


		
		# f_doclist=open('doclist.txt','wb')

		# for i in doclist:
		# 	f_doclist.write(str(i)+'\n')
		# f_doclist.close()


if __name__=='__main__':

	CON=constructor()
	CON.get_doclist()
	# CON.sentence('wiki_en_unprocessed.txt', 'wiki_ja_unprocessed.txt')

	f_en=open('wiki_en_unprocessed.txt')
	f_ja=open('wiki_ja_unprocessed.txt')
	CON.en_all=f_en.readlines()
	CON.ja_all=f_ja.readlines()

	for i in CON.doclist:
		try:
			CON.get_doc(i)
			CON.process()
			CON.compare(i)
		except:
			continue
