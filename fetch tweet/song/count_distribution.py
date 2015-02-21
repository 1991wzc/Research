import csv

def count():
	f=open('id_count_ja_song.txt')

	lines=f.readlines()

	f1=open('count.csv','wb')
	writer = csv.writer(f1)
	prob={}
	for line in lines:
		count=(line.split())[1]
		if count not in prob:
			prob[count]=1
		if count in prob:
			prob[count]+=1

	for count in prob:
		writer.writerow([count, prob[count]])

	f1.close()

count()