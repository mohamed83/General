'''
Created on Oct 15, 2014

@author: mohamed
'''
import os
import grequests
from utils import getWebpageText, extractTextFromHTML
def combineFiles():
    dirName = "/home/dlrl/ebola/outputs/output"
    outputs = [1,2,3,4,6,7,8,9]
    urls =[]
    for o in outputs:
        dname = dirName + str(o)
        dirs = os.listdir(dname)
        for f in dirs:
            if f.startswith("part"):
                fn = open(dname+"/"+f)
                c = fn.readlines()
                urls.extend(c)
                fn.close()
        fo = open(dname+"/"+"urls"+str(o)+".txt","w")
        s = "".join(urls)
        fo.write(s)
        fo.close()

def combineURLs():            
    dirName = "/Users/dlrl/ebola/allURLs/"
    outputs = [1,2,3,4,6,7,8,9]
    allURLs =[]
    for o in outputs:
        fname = dirName + "urls"+str(o) +".txt"
        f = open(fname)
        c = f.readlines()
        allURLs.extend(c)
        f.close()
    #this file will be in General project on Dropbox
    fo = open("allURLs.txt","w")
    s = "".join(allURLs)
    fo.write(s)
    fo.close()
    
def getUniqueURLs():
    allURLs = []
    uniqueURLs = {}
    f = open("allURLs.txt","r")
    allURLs.extend(f.readlines())
    f.close()
    print len(allURLs)
    for u in allURLs:
        u = u.strip()
        p = u.split("\t")
        url = p[0]
        count = p[1]
        if url in uniqueURLs:
            uniqueURLs[url]+= int(count)
        else:
            uniqueURLs[url] = int(count)
    f = open("ebolaUniqueURLs.txt","w")
    for u in uniqueURLs:
        f.write(u+'\n')
    f.close()
    return uniqueURLs
    '''
    print len(uniqueURLs)
    c = 0
    for u in uniqueURLs:
        if uniqueURLs[u] == 0:
            c+= 1
    print c
    '''
def createWebpagesFiles():
    uUrls = getUniqueURLs()
    urls = uUrls.keys()
    print len(urls)
    
    rs=[grequests.get(u,timeout=10) for u in urls]

    re= grequests.map(rs)

    print len(re)
    
    
    #texts = getWebpageText(urls)
    
    #print len(texts)
    i = 1
    #for t in texts:
    fm = open("ebolaFiles/mapping.txt","w")
    for r in re:
        if r.content and r.content !="":
        #if t != "":
            text = extractTextFromHTML(r.content)
            f = open("ebolaFiles/" + str(i)+".txt","w")
            f.write(text)
            #fm.write(str(i) +"--"+ r.url + "\n")
            fm.write(r.url + "\n")
            f.close()            
            print i
            i+= 1
    #print i
    fm.close()
        
if __name__ == "__main__":
    
    #combineURLs()
    #getUniqueURLs()
    createWebpagesFiles()