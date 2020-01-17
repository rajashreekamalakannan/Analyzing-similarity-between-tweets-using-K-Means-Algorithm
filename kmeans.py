import re
import numpy as np

f=open("bbchealth.txt",'r')
i=1
tweet=list()
print("Data : ")
for x in f.readlines():
	tweet.append(x.split('|')[2])
	print (i,'.',tweet[-1])
	i+=1

def preprocessing(tweet):
	for x in range(len(tweet)):
		tweet[x]=tweet[x].lower()
		temp=tweet[x].split(" ")
		for y in range(len(temp)):
			if re.match("(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",temp[y]):
				del(temp[y])
			elif re.match("@\w+",temp[y]):
				del(temp[y])
			elif re.match("#\w+",temp[y]):
				t=list(temp[y])
				t1=str()
				del(t[0])
				temp[y]=''
				for z in t:
					temp[y]+=z
		tweet[x]=''
		for y in temp:
			if y!=temp[-1]:
				tweet[x]+=y+' '
			else:
				tweet[x]+=y
	return tweet

def jaccard(A,B):
	AUB=0
	AnB=0
	A=A.split(" ")
	B=B.split(" ")
	for x in A: 
		if x in B:
			AnB+=1
		else:
			AUB+=1
	AUB+=len(B)
	return float((AUB-AnB)/AUB)

def SSE(l):
	minj=2**31
	for i in range(0,len(l)):
		val=0
		pos=0
		for j in range(0,len(l)):
			if i!=j:
				val+=jaccard(tweet[i],tweet[j])
		if val<minj:
			minj=val
			pos=i
	return pos

def newcentroid(km,init):
	for i in range(1,len(km)+1):
		init[i-1]=SSE(km[i])
	return init

tweet=preprocessing(tweet)
print("Pre-Processed Data : ")
i=1
for x in tweet:
	print(str(i)+'.'+x)
	i+=1
k=10
cent=np.random.randint(low=0,high=3928,size=k)
km=dict()
for i in range(1,k+1):
	km[i]=list()
change=1
while change==1:
	init=cent
	change=0
	for x in range(len(tweet)):
		minj=2**31
		pos=0
		for i in range(k):
			t=jaccard(tweet[cent[i]],tweet[x])
			if t<minj:
				minj=t
				pos=i
		km[pos+1].append(x)
	init=newcentroid(km,init)
	for i in range(0,len(cent)):
		if init[i]!=cent[i]:
			change=1
			break
	cent=init
	if change==1:
		for i in range(1,k+1):
			km[i]=[]
for i in range(1,k+1):
	print("Cluster",i,":",km[i])
print("\nSize of the clusters : ")
for i in range(1,k+1):
	print("Cluster",i,":",len(km[i]))
sse=0
for i in range(1,k+1):	
	for x in km[i]:
		if x!=km[i][0]:
			sse+=(jaccard(tweet[x],tweet[cent[i-1]]))**2
print("SSE = ",sse)
