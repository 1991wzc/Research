#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import csv

def creat(lan):
	reload(sys)
	sys.setdefaultencoding('utf8')

	f=open(lan+'_acg.csv')
	writer=csv.writer(open(lan+'_edge.csv','wb'))
	writer.writerow(['Source','Target'])

	count=0
	for line in f.xreadlines():
		try:
			#Tweet,Tweet_ID,Author_name,Author_ID,Statuses_Count,Mentioned_ID,Mentioned_Name,Hashtags=line.split(",")
			split=line.split(",")
			Author_name=split[2]
			Mentioned_Name=split[6]
			names=Mentioned_Name.split('分隔符')
			if len(names)>0:
				#print Mentioned_Name				
				for name in names:
					if name!='':
						writer.writerow([Author_name,name])
				if len(names)>1:
					for name in names:						
						index=names.index(name)						
						for coappear in names[index:]:
							if coappear!='' and coappear!=name:
								writer.writerow([name,coappear])
				count+=1
				if count%50000==0:
					print '%s tweets.'%str(count)
		except:
			pass

	f.close()

#creat('en')
creat('en')
	