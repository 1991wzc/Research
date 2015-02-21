from __future__ import division
import os

def link(devide,K):
	parentpath=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
	#path=os.getcwd()

	f_ja=open(parentpath+'\\tweets\\ja_tweet_final.txt','r')
	M_ja=len(f_ja.readlines())
	f_topic_prob_ja=open(parentpath+'\\recommend\\topic_prob_ja.txt','w')

	count_ja=[0]*K
	prob_ja=[0]*K
	for i in range(devide):
		f=open('topic_count_ja-'+str(i)+'.txt')
		lines=f.readlines()
		for i in range(len(lines)):
			count_ja[i]+=int(lines[i])
	for i in range(K):
		prob_ja[i]=count_ja[i]/M_ja
		f_topic_prob_ja.write(str(prob_ja[i])+'\n')

	f_topic_prob_ja.close()

	f_tweet_topic_ja=open(parentpath+'\\recommend\\tweet_topic_ja.txt','w')
	for i in range(devide):
		f=open('tweet_topic_ja-'+str(i)+'.txt')
		f_tweet_topic_ja.write(f.read())

	f_tweet_topic_ja.close()

	# f_max_prob_ja=open(parentpath+'\\recommend\\max_prob_ja.txt','w')
	# for i in range(devide):
	# 	f=open('max_prob_ja-' + str(i) + '.txt')
	# 	f_max_prob_ja.write(f.read())

	# f_theta_ja=open(parentpath+'\\recommend\\theta_ja.txt','w')
	# for i in range(devide):
	# 	f=open('theta_ja-' + str(i) + '.txt')
	# 	f_theta_ja.write(f.read())

	# f_theta_ja.close()


link(30, 100)