'''
Created on Nov 12, 2014

@author: mmagdy
'''
d = []
numBins = 20

f = open("z_403_users.txt","r")
for l in f:
    p = l.split(",")
    u = p[0]
    c = int(p[1])
    if c > 10:
        d.append((u,c))
f.close()
ft = open("users_freq.txt","w")
for l in d:
    ft.write(str(l)+"\n")   
ft.close()    
tweetCounts = [v for _,v in d]
binSize = max(tweetCounts)/numBins
bins = [(i,0) for i in range(numBins+1)]
usersCount = dict(bins)
     
for u,c in d:
    binNo = c / binSize
    usersCount[binNo]+= 1

fu = open('usersBinCount.txt','w')
for k in usersCount:
    fu.write(str((k+1) * binSize) + ","+str(usersCount[k])+"\n")
fu.close()
