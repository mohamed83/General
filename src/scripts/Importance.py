'''
Created on May 8, 2014

@author: dlrl
'''
'''
Created on Feb 18, 2014

@author: mohamed
'''
import sys    
def getDomain(url):
    #stat = {}
    #url = ""
    domain = ""
    #for elem in data:
        #url = elem[0]
    #url = elem
    #ind = url.find("http")
    ind = url.find("//")
    if ind != -1 :
        #url2 = url[ind:]
        #ind = url2.find("//")
        domain = url[ind+2:]
        ind = domain.find("/")
        domain = domain[:ind]
    return domain
#             if domain not in stat:
#                 stat[domain] = [url]
#             else:
#                 stat[domain].append(url)
#     return stat

def getDataset(filename):
    stat = {}
    f = open(filename,"r")
    fw = open("domains.txt","w")
    
    for line in f:
        #print line
        line = line.strip()
        if line.endswith("\n"):
            line = line[:-1]
#         
        domain = getDomain(line)
        if domain not in stat:
            stat[domain] = [line]
        else:
            stat[domain].append(line)
    sortedList = sorted(stat.items(), key=lambda x: len(x[1]),reverse=True)
    #for k,v in stat.iteritems():
        #print k + " " + str(len(v))
        #fw.write(k + " " + str(len(v)) + "\n")
    for k,v in sortedList:
        print k + " " + str(len(v))
        fw.write(k + " " + str(len(v)) + "\n")
    
    #fw.write(training)
            
    f.close()
    fw.close()
    
def getGlobal(fList):
    stat={}
    #f = open("NYEventOut.txt","r")
    #f2 = open("WAEventOut.txt","r")
    globalList=[]
    fw = open("globalDomains.txt","w")
    for fileName in fList:
        localList = []
        f = open(fileName,"r")
        for line in f:
            line = line.strip()
            p = line.split(",")
            #srcCount = p[1]
            domain = getDomain(p[0])
            
            if domain not in localList:
                localList.append(domain)
            '''
            if domain not in stat:
                stat[domain] = [p[1]]
            else:
                stat[domain].append(p[1])
            '''
        f.close()
        globalList.append(localList)
        
    
    for domList in globalList:
        for dom in domList:
            if dom in stat:
                stat[dom] = stat[dom] + 1
            else:
                stat[dom] = 1
    '''
    for line in f2:
        p = line.split(" ")
        if p[0] not in stat:
            stat[p[0]] = [p[1]]
        else:
            stat[p[0]].append(p[1])
    f2.close()
    '''
    print len(stat)
    #sortedList = sorted(stat.items(), key=lambda x: len(x[1]),reverse=True)
    sortedList = sorted(stat.items(), key=lambda x: x[1],reverse=True)
    #for k,v in stat.iteritems():
        #print k + " " + str(len(v))
        #fw.write(k + " " + str(len(v)) + "\n")
    for k,v in sortedList:
        print k + " " + str(v)
        fw.write(k + " " + str(v) + "\n")
    fw.close()


def getGlobalwFreq(fList):
    stat={}
    #globalList=[]
    fw = open("globalDomainswFreq.txt","w")
    for fileName in fList:
        #localList = {}
        
        f = open(fileName,"r")
        for line in f:
            line = line.strip()
            p = line.split(",")
            #srcCount = p[1]
            #domain = getDomain(p[0])
            domain = p[0]
            
            if domain in stat:
                stat[domain] = stat[domain] + int(p[-1])
            else:
                stat[domain] = int(p[-1])
            '''
            if domain in localList:
                localList[domain] += int(p[-1])
            else:
                localList[domain] = int(p[-1])
        f.close()
        globalList.append(localList)
        '''
    '''
    for domList in globalList:
        for dom,freq in domList.items():
            if dom in stat:
                stat[dom] = stat[dom] + freq
            else:
                stat[dom] = freq
    '''
    print len(stat)
    #sortedList = sorted(stat.items(), key=lambda x: len(x[1]),reverse=True)
    sortedList = sorted(stat.items(), key=lambda x: x[1],reverse=True)
    #for k,v in stat.iteritems():
        #print k + " " + str(len(v))
        #fw.write(k + " " + str(len(v)) + "\n")
    for k,v in sortedList:
        print k + "," + str(v)
        fw.write(k + "," + str(v) + "\n")
    fw.close()

def sourceFreqList(fList):
    #print fList
    stat={}
    #globalList={}
    #fw = open("sourcesFreqList.txt","w")
    fw = open("commonSources.txt","w")
    ids = []
    for fileName in fList:
        eid = int(fileName.split("_")[0])
        ids.append(eid)
        #localList = {}
        f = open(fileName,"r")
        for line in f:
            line = line.strip()
            p = line.split(",")
            #srcCount = p[1]
            domain = p[0]
            
#             if domain in stat:
#                 stat[domain].append( (id,int(p[-1])))
#             else:
#                 stat[domain] = [(id,int(p[-1]))]

            if domain in stat:
                stat[domain][eid]=int(p[-1])
            else:
                stat[domain]= {eid:int(p[-1])}
                
#     print len(stat)
#     sortedList = sorted(stat.items(), key=lambda x: len(x[1]),reverse=True)
#     #sortedList = sorted(stat.items(), key=lambda x: sum(x[1]),reverse=True)
#     for k,v in sortedList:
#         #print k + "," + str(v)
#         fw.write(k + "," + str(v) + ","+str(sum([val for _,val in v]))+ "\n")
    
    print len(stat)
    sortedList = sorted(stat.items(), key=lambda x: len(x[1]),reverse=True)
    #sortedList = sorted(stat.items(), key=lambda x: sum(x[1]),reverse=True)
#     for k,v in sortedList:
#         #print k + "," + str(v)
#         if len(v) > 9:
#             fw.write(k + "," + str(v) + ","+str(sum([val for _,val in v]))+ "\n")

    for k,v in sortedList:
        l = []
        #vals = [x for x,y in v]
        if len(v) > 9:
            for eid in ids:
                if eid in v:
                    l.append(v[eid])
                else:
                    l.append(0)
            fw.write(k + "," + str(l) + ","+str(sum(l))+ "\n")   
            
            
    
    
#     commonDomains = []
#     for d,l in stat.items():
#         if len(l) == len(fList):
#             commonDomains.append((d,sum(l)))
#     sortedList = sorted(commonDomains, key=lambda x: x[1],reverse=True)
#     for k,v in sortedList:
#         print k + "," + str(v)
#         fw.write(k + "," + str(v) + "\n")
    fw.close()
    
    
def shootingTweetArchivesSources():
    archiveList = [40,41,44,45,55,72,78,89,121,122,128,140,145,146,157,159,186]#,241,242,286]
    shortURLsFreq = {}
    origURLsFreq = {}
    for archiveID in archiveList:
        shortURLsFreq[archiveID]= {}
        fileName = "schoolShootingOutputFiles/shortURLs_z_" +str(archiveID) + ".txt"
        f = open(fileName)
        for line in f:
            line = line.strip()
            parts = line.split(",")
            shortURLsFreq[archiveID][parts[0]] = int(parts[1])
        f.close()
        origURLsFreq[archiveID]={}
        domains={}
        fileName = "short_origURLsMapping_z_" + str(archiveID) + ".txt"
        f = open(fileName)
        for line in f:
            line = line.strip()
            parts = line.split(":--")
            origURL = parts[0]
            
            #c = len(parts[1])
            surlList = parts[1].split(",")
            count = 0
            for surl in surlList:
                if surl in shortURLsFreq[archiveID]:
                    count += shortURLsFreq[archiveID][surl]
            if count > 0:
                origURLsFreq[archiveID][origURL] = count
                dom = getDomain(origURL)
                if dom in domains:
                    domains[dom]+= count
                else:
                    domains[dom]=count
        f.close()
        
        f = open(str(archiveID) +"_sources.txt","w")
        
        sorted_list = sorted(domains.items(), key=lambda x: x[1],reverse=True)
        
        for s,v in sorted_list:
            f.write(s + "," + str(v)+"\n")
        f.close()
        
        #f = open(str(archiveID) +"_sources.txt","w")
        #srcFreqs = origURLsFreq[archiveID]
        
        #sorted_list = sorted(srcFreqs.items(), key=lambda x: x[1],reverse=True)
        
        #for s,v in sorted_list:
        #    f.write(s + "," + str(v)+"\n")
        #f.close()
        
    
    #events = []
    #sourcesDist = []
    #return

def shootingSourcesImportance(filename):
    f = open(filename,"r")
    c = f.read()
    lines = c.split("\r")
    #print c
    header = lines[0]
    parts = header.split(",")
    colls = parts[1:-1]
    #collsDic = dict(zip(colls,[[]]*len(colls)))
    #collsDic = dict(enumerate(colls))
    lines = lines[1:]
    for i in range(len(colls)):
        sourceOrderByCollection = [{}]
    for l in lines:
        p = l.split(",")
        src = p[0]
        freqs = p[1:-1]
        for i in range(len(colls)):
            sourceOrderByCollection[i][src] = freqs[i]
    print sourceOrderByCollection
             
        
def getGlobalImportantWebsitesList(f):
    wlist = []
    fl = open(f)
    all = fl.readlines()
    
    for i in range(len(all)):
        if i % 3 == 1:
            wlist.append(all[i].strip())
    print wlist
    print len(wlist)
    f=open("news websites alex rank.txt","w")
    for wl in wlist:
        f.write(wl +'\n')
    f.close()
    
    '''
    l_noNum = [l.strip() for l in all if not l.strip().isdigit()]# and l.strip() != '']
    print l_noNum    
    print len(l_noNum)
    
    for i in range(len(l_noNum)):
        if i % 2 == 0:
            wlist.append(l_noNum[i])
    print wlist
    print len(wlist)
    '''
    #lengs = [len(lg) for lg in l_noNum]
    #print lengs
    #l_noDesc = [el.strip() for el in l_noNum if not len(el)>25] #not len(l)>25 and
    #print l_noDesc
    #print len(l_noDesc)

if __name__ == "__main__":
    #f = sys.argv[1:]
    #getDataset(f)
    #Next time read the previous global and then update it with data from new files
    #getGlobal(f)
    #getGlobalwFreq(f)
    #sourceFreqList(f)
    #shootingTweetArchivesSources()
    
    #f = "sources.csv"
    #shootingSourcesImportance(f)
    
    getGlobalImportantWebsitesList("news website Alexa rank.txt")