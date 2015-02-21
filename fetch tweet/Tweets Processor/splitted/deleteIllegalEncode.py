

import chardet
import sys

tweets=open('1.txt').read()
f_final=open('2.txt','w')
true=0
false=0



for i in tweets:
	if chardet.detect(i)['encoding']=='windows-1252':
		true+=1
		f_final.write(i)
	elif chardet.detect(i)['encoding']=='ascii':
		true+=1
		f_final.write(i)
	else:
		print chardet.detect(i)['encoding']
		false+=1

f_final.close()

print true
print false