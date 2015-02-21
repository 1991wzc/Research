#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

def deduplicate(name_ja,name_en,divide):
	print 'Start.'
	path = os.getcwd()
	title=[]
	#totallenth_en=0
	totallenth_ja=0
	

	for i in range(divide):
		count=0
		f_wiki_ja=open(path+'\\raw\\'+name_ja+'-'+str(i+1)+'.txt')
		f_wiki_en=open(path+'\\raw\\'+name_en+'-'+str(i+1)+'.txt')

		f_deduplicated_ja=open(path+'\\deduplicated\\'+name_ja+'_deduplicated-'+str(i+1)+'.txt','wb')

		f_deduplicated_en=open(path+'\\deduplicated\\'+name_en+'_deduplicated-'+str(i+1)+'.txt','wb')

		lines_ja=f_wiki_ja.readlines()
		lines_en=f_wiki_en.readlines()
		totallenth_ja+=len(lines_ja)
		#totallenth_en+=len(lines_en)

		for i in xrange(len(lines_ja)):
			split=lines_ja[i].split('出典: フリー百科事典『ウィキペディア（Wikipedia）』')
			if len(split)<2:
				count+=1
				if count%500==0:
					print str(count)+' duplicated document pairs deleted.'
			elif len(split)>=2:
				if split[0] not in title:
					title.append(split[0])
					f_deduplicated_ja.write(lines_ja[i])
					f_deduplicated_en.write(lines_en[i])
				elif split[0] in title:
					count+=1
					if count%500==0:
						print str(count)+' duplicated document pairs deleted.'

	f_deduplicated_en.close()
	f_deduplicated_ja.close()
	print 'Complete.'
	print 'Total '+str(totallenth_ja)+' document pairs.'




deduplicate('wikipedia_ja','wikipedia_en', 17)