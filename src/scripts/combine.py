'''
Created on Sep 30, 2014

@author: dlrl
'''
total = []
f1 = open("origURLs10000.txt","r")
for line in f1:
    line = line.strip()
    p = line.split(",")
    url = p[0]
    if url.endswith("."):
        url = url[:-2]
    total.append(url)
f1.close()
f1 = open("origURLs20000.txt","r")
for line in f1:
    line = line.strip()
    p = line.split(",")
    url = p[0]
    if url.endswith("."):
        url = url[:-2]
    total.append(url)
f1.close() 
f = open("origURLs_0_20000.txt","w")
s = set(total)
for t in s:
    f.write(str(t)+"\n")
    
f.close()   