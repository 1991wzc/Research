#!/usr/bin/python
# -*- coding: utf-8 -*-

import newwordmap
import tf_idf
import topicAssign
import topicDistribution

#analyse user interests

K=100
alpha=0.5
usersum=5
for i in range(usersum):
	title=str(i+1)
	print title
	newwordmap.new_wordmap_user(title)
	#tf_idf.tf_idf_user(title)
	topicAssign.topicassign_user('en', title,alpha,K)
	topicDistribution.topicDistribution_user('en', title,alpha,K)

