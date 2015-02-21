#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import sys

class unification():
	word2id_en=dict()
	word2id_ja=dict()

	word2topic_en=dict()
	word2topic_ja=dict()

	word2topic_en_all=dict()
	word2topic_ja_all=dict()

	pair_en=dict()
	pair_ja=dict()

	def combine_dictionary(self):

		f_en_all=open('all_en.phi_word2topic')
		f_ja_all=open('all_ja.phi_word2topic')
		f_en_combine=open('combine_en.phi_word2topic')
		f_ja_combine=open('combine_ja.phi_word2topic')

		for line in f_en_combine.xreadlines():
			pair=line.split()
			if pair[0] not in self.word2id_en and len(pair)>1:
				self.word2id_en[pair[0]]=len(self.word2id_en)
				self.word2topic_en[pair[0]]=int(pair[1])

		for line in f_en_all.xreadlines():
			pair=line.split()
			if pair[0] not in self.word2id_en and len(pair)>1:
				self.word2id_en[pair[0]]=len(self.word2id_en)
				self.word2topic_en_all[pair[0]]=int(pair[1])

		for line in f_ja_combine.xreadlines():			
			pair=line.split()
			if pair[0] not in self.word2id_ja and len(pair)>1:
				self.word2id_ja[pair[0]]=len(self.word2id_ja)
				self.word2topic_ja[pair[0]]=int(pair[1])

		for line in f_ja_all.xreadlines():
			pair=line.split()
			if pair[0] not in self.word2id_en and len(pair)>1:
				self.word2id_ja[pair[0]]=len(self.word2id_ja)
				self.word2topic_ja_all[pair[0]]=int(pair[1])

		f_en=open('wordmap_en.txt','wb')
		f_ja=open('wordmap_ja.txt','wb')

		for word in self.word2id_en:
			f_en.write(word+' '+str(self.word2id_en[word])+'\n')

		for word in self.word2id_ja:
			f_ja.write(word+' '+str(self.word2id_ja[word])+'\n')

		f_en.close()
		f_ja.close()

	def cosine(self,v1,v2):
		l_v1=len(v1)
		l_v2=len(v2)
		if l_v1==0 or l_v2==0:
			return 0.0
		else:
			dot=0
			calculated=list()
			for i in v1:
				if i in v2 and i not in calculated:
					dot+=1
					calculated.append(i)
			return dot/math.sqrt(l_v1 * l_v2)

	def topic_unify(self):
		f_en_all=open('all_en.twordsnoProb')
		f_ja_all=open('all_ja.twordsnoProb')
		f_en_combine=open('combine_en.twordsnoProb')
		f_ja_combine=open('combine_ja.twordsnoProb')

		score_en=dict()
		score_ja=dict()

		print 'Japanese topic unification.'
		all_all_ja=f_ja_all.readlines()
		all_combine_ja=f_ja_combine.readlines()

		for i in range(len(all_combine_ja)):
			words2=all_combine_ja[i].split()
			topWords_ja_combine=list()
			for word2 in words2:
				topWords_ja_combine.append(self.word2id_ja[word2])
				if len(topWords_ja_combine)==50:
					continue

			for j in range(len(all_all_ja)):
				words=all_all_ja[i].split()
				topWords_ja_all=list()
				for word in words:
					topWords_ja_all.append(self.word2id_ja[word])
					if len(topWords_ja_all)==50:
						continue
				score_ja[(j,i)]=self.cosine(topWords_ja_all,topWords_ja_combine)

		score_ja= sorted(score_ja.iteritems(), key=lambda d:d[1], reverse = True)
		#print score_ja
#		print self.pair_ja		
		for i in score_ja:
			if i[1]!=0.0:
				if i[0][0] not in self.pair_ja.keys():
					if i[0][1] not in self.pair_ja.values():						
						self.pair_ja[i[0][0]]=i[0][1]
						print i
		print self.pair_ja

		print 'English topic unification.'
		all_all_en=f_en_all.readlines()
		all_combine_en=f_en_combine.readlines()

		for i in range(len(all_combine_en)):
			words2=all_combine_en[i].split()
			topWords_en_combine=list()
			for word2 in words2:
				topWords_en_combine.append(self.word2id_en[word2])
				if len(topWords_en_combine)==50:
					continue

			for j in range(len(all_all_en)):
				words=all_all_en[i].split()
				topWords_en_all=list()
				for word in words:
					topWords_en_all.append(self.word2id_en[word])
					if len(topWords_en_all)==50:
						continue
				score_en[(j,i)]=self.cosine(topWords_en_all,topWords_en_combine)

		score_en= sorted(score_en.iteritems(), key=lambda d:d[1], reverse = True)
		#print score_en
#		print self.pair_en
		for i in score_en:
			if i[1]!=0.0:
				if i[0][0] not in self.pair_en.keys():
					if i[0][1] not in self.pair_en.values():						
						self.pair_en[i[0][0]]=i[0][1]
						print i						
		print self.pair_en
		
	def word_topic_reassign(self):

		for word in self.word2topic_en_all:
			if word not in self.word2topic_en:
				oldtopic=self.word2topic_en_all[word]
				newtopic=self.pair_en[oldtopic]
				self.word2topic_en[word]=newtopic

		for word in self.word2topic_ja_all:
			if word not in self.word2topic_ja:
				oldtopic=self.word2topic_ja_all[word]
				newtopic=self.pair_ja[oldtopic]
				self.word2topic_ja[word]=newtopic

		f_en=open('model_en-final.phi_word2topic','wb')
		f_ja=open('model_ja-final.phi_word2topic','wb')

		for word in self.word2topic_en:
			f_en.write(str(self.word2id_en[word])+' '+str(self.word2topic_en[word])+'\n')

		for word in self.word2topic_ja:
			f_ja.write(str(self.word2id_ja[word])+' '+str(self.word2topic_ja[word])+'\n')

		f_en.close()
		f_ja.close()


if __name__=='__main__':	
	uni=unification()
	uni.combine_dictionary()
	uni.topic_unify()
	uni.word_topic_reassign()