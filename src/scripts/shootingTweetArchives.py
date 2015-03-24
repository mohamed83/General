'''
Created on Sep 23, 2014

@author: mohamed
'''
import sys
import requests
#import hashlib
#from bs4 import BeautifulSoup,Comment
import re
#import sunburnt
import pymysql
from operator import itemgetter
from contextlib import closing
import eventUtils
#import grequests
requests.packages.urllib3.disable_warnings()
def eh(request,exception):
    print 'request failed'

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head']:
        return False
    return True

def extractShortURLs(tweetsText):
    shortURLsList = []
    regExp = "(?P<url>https?://[a-zA-Z0-9\./-]+)"
    for t in tweetsText:
        t = t[0]
        url_li = re.findall(regExp, t)  # find all short urls in a single tweet
        while (len(url_li) > 0): 
            shortURLsList.append(url_li.pop())
    return shortURLsList

def getValidShortURLs(shortURLs):
    surls = []
    for url in shortURLs:
        i = url.rfind("/")
        if i+1 >= len(url):
            continue
        p = url[i+1:]
        if len(p) < 10:
            continue
        while url.endswith("."):
            url = url[:-1]
        surls.append(url)
    return surls

def getShortURLsFreqDic(shortURLs):
    shortURLsFreqDic = eventUtils.getFreq(shortURLs)
    return shortURLsFreqDic

def getTopFreqShortURLs(shortURLsTuples,fthresh):
    freqShortURLs =[(s,v) for s,v in shortURLsTuples if v> fthresh]
    
    '''    
    for surl,v in shortURLsTuples:
        if v > fthresh:
            freqShortURLs.append(surl)
    '''
    return freqShortURLs

def getOrigLongURLs(shortURLs):
    expandedURLs = {}
        #freqShortURLs = freqShortURLs[:2000]
    i=0
    e=0
    
    for surl,v in shortURLs:
        try:
            with closing(requests.get(surl,timeout=10, stream=True, verify=False)) as r:
                #print r.status_code
                if r.status_code == requests.codes.ok:
                    #print surl
                    ori_url =r.url
                    if ori_url in expandedURLs:
                        expandedURLs[ori_url].append((surl,v))
                    else:
                        expandedURLs[ori_url] = [(surl,v)]
                    #expandedURLs.append(ori_url)
                    i  =i+1
                elif r.url != surl or r.request.url != surl:
                    ori_url =r.url
                    if ori_url in expandedURLs:
                        expandedURLs[ori_url].append((surl,v))
                    else:
                        expandedURLs[ori_url] = [(surl,v)]
                    i  =i+1
                else:
                    e = e+1    
                    print r.status_code , surl, r.url, r.request.url
                    #expandedURLs.append("")
        except :
            print sys.exc_info()[0], surl
            #expandedURLs.append("")
            e = e +1
    print "urls expanded: ", i
    print "bad Urls: ",e
    return expandedURLs

def getOrigLongURLsFreqDic(shortLongURLsTuples):
    origLongURLsFreqDic = {}
    for s,f,l in shortLongURLsTuples:
        if l in origLongURLsFreqDic:
            origLongURLsFreqDic[l]+= f
        else:
            origLongURLsFreqDic = f
    return origLongURLsFreqDic

def getSourceFreqDic(origLongURLsFreqDic):
    sourcesFreqDic = {}
    for k,v in origLongURLsFreqDic.items():
        su = sum([l for s,l in v])
        dom = eventUtils.getDomain(k)
        if dom in sourcesFreqDic:
            sourcesFreqDic[dom].append(su)
        else:
            sourcesFreqDic[dom] = [su]
            
    return sourcesFreqDic
            
def createShortLongURLsTuples(shortURLsDic,freqShortURLs,origLongURLs):
    slURLsTuples = []
    for su,ou in zip(freqShortURLs,origLongURLs):
        if ou != "":
            f = shortURLsDic[su]
            slURLsTuples.append((su,f,ou))
    '''
    for i in range(len(origLongURLs)):
        if origLongURLs[i] != "":
            slURLsTuples.append((shortURLsTuples[i][0],shortURLsTuples[i][1],origLongURLs[i]))
    '''
    return slURLsTuples

def saveSourcesFreqDic(sourcesFreqDic,filename):
    t = [(k, len(v),sum(v)) for k,v in sourcesFreqDic.items()]
    st = eventUtils.getSorted(t, 1)
    f= open(filename,'w')
    #for k,v in sourcesFreqDic.items():
    for k,l,s in st:
        #f.write(k +"," + str(len(v))+"," + str(sum(v))+"\n")
        f.write(k +"," + str(l)+"," + str(s)+"\n")
    f.close()

def extractShortURLsFreqDic(tweetsText):
    shortURLsDic = {}
    regExp = "(?P<url>https?://[a-zA-Z0-9\./-]+)"
    for t in tweetsText:
        t = t[0]
        url_li = re.findall(regExp, t)  # find all short urls in a single tweet
        while (len(url_li) > 0): 
            surl = url_li.pop()
            i = surl.rfind("/")
            if i+1 >= len(surl):
                continue
            p = surl[i+1:]
            if len(p) < 10:
                continue
            while surl.endswith("."):
                surl = surl[:-1]
            if surl in shortURLsDic:
                shortURLsDic[surl] += 1
            else:
                shortURLsDic[surl]=1
            #shortURLsList.append()
    return shortURLsDic#shortURLsList

def processEventTweets(tweetsSource,thres,sourcesFilename,archiveID):
    #for t in tweetsSource:
    #t = t[0]
    '''
    shURLs = extractShortURLs(tweetsSource)
    print "short Urls extracted: ", len(shURLs)
    
    vsURLs = getValidShortURLs(shURLs)
    print "cleaned: ", len(vsURLs)
    
    sURLsFreq = getShortURLsFreqDic(vsURLs)
    print "Unique URLs dic created: ", len(sURLsFreq)
    '''
    sURLsFreq = extractShortURLsFreqDic(tweetsSource)
    print "Unique URLs dic created: ", len(sURLsFreq)
    
    freqShortURLs = getTopFreqShortURLs(sURLsFreq.items(), thres)
    print "Freq URLs (>"+str(thres)+"): ",len(freqShortURLs)
    f = open('shortURLs_'+archiveID+'.txt','w')
    f.write('\n'.join([s for s,v in freqShortURLs]))
    f.close()
    origURLs = getOrigLongURLs(freqShortURLs)
    print "Orig Url dic len: ", len(origURLs)
    f = open('origURLs_'+archiveID+'.txt','w')
    f.write('\n'.join(origURLs.keys()))
    f.close()
    #slURLsTuples = createShortLongURLsTuples(sURLsFreq,freqShortURLs, origURLs)
    #origURLsFreq = getOrigLongURLsFreqDic(slURLsTuples)
    sourcesFreq = getSourceFreqDic(origURLs)
    saveSourcesFreqDic(sourcesFreq, sourcesFilename)
    return sourcesFreq

def batchProcessing():
    thresh = 1
    #archiveList = [40,41,42,43,44,45,55,72,78,89,121,122,128,140,145,146,157,159,186,241,242,286,416,419,435,436,437,438,439,441,443,444,445,459,473,502,504,522,530,540,542,543,544,568,569,570,581,582,592]
    archiveList = [440]
    for aid in archiveList:
        
        archiveID = "z_"+str(aid)
        
        conn = pymysql.connect(host="twitter.dlib.vt.edu", user="mmagdy", passwd="pw4cinnamon", db="twitter",charset='utf8')
        cursor = conn.cursor()
        
        #f = open(sys.argv[1],"r")
        query = "select text from twitter." + archiveID + " where iso_language_code like 'en'"
        #print query
        cursor.execute(query)
        docs=[]
        
        print "tweets read from DB"
        
        tweets = cursor.fetchall()
        processEventTweets(tweets, thresh, archiveID+'_Sources.txt', archiveID)
        # Extract short URLs from Tweets
        #-------------------------------
        #shortURLsList =[]
        #for row in cursor.fetchall():
        #    line = row[0]
            
'''
def batchProcessing():
    thresh = 5
    archiveList = [40,41,42,43,44,45,55,72,78,89,121,122,128,140,145,146,157,159,186,241,242,286]
    #archiveList = [241,242,286]
    for aid in archiveList:
        
        archiveID = "z_"+str(aid)
        
        conn = pymysql.connect(host="twitter.dlib.vt.edu", user="mmagdy", passwd="pw4cinnamon", db="twitter",charset='utf8')
        cursor = conn.cursor()
        
        #f = open(sys.argv[1],"r")
        query = "select text from twitter." + archiveID + " where iso_language_code like 'en'"
        print query
        cursor.execute(query)
        docs=[]
        
        print "tweets read from DB"
        
        # Extract short URLs from Tweets
        #-------------------------------
        shortURLsList =[]
        for row in cursor.fetchall():
            line = row[0]
            regExp = "(?P<url>https?://[a-zA-Z0-9\./-]+)"
            url_li = re.findall(regExp, line)  # find all short urls in a single tweet
            while (len(url_li) > 0): 
                shortURLsList.append(url_li.pop())
        print "short Urls extracted: ", len(shortURLsList)
        surls = []
        for url in shortURLsList:
            i = url.rfind("/")
            if i+1 >= len(url):
                continue
            p = url[i+1:]
            if len(p) < 10:
                continue
            surls.append(url)
        print "cleaned: ", len(surls)
        surlsDic ={}
        for url in surls:
            if url in surlsDic:
                surlsDic[url] = surlsDic[url] + 1
            else:
                surlsDic[url] = 1
        print "Unique URLs dic created: ", len(surlsDic)
        sorted_list = sorted(surlsDic.iteritems(), key=itemgetter(1), reverse=True)
        #print "sorted"
        #print len(sorted_list)
        freqShortURLs =[]
        
        for surl,v in sorted_list:
            if v > thresh:
                freqShortURLs.append(surl)
        print "Freq URLs (>1): ",len(freqShortURLs)
        
        fs = open("shortURLs_"+ archiveID+".txt","w")
        for surl,v in sorted_list:
            fs.write(surl +"," + str(v)+"\n")
        fs.close()
        
        # Expand Short URLs
        #-------------------------------
        expanded_url_dict = {}
        #freqShortURLs = freqShortURLs[:2000]
        i=0
        e=0
        
        for url in freqShortURLs:
            try:
                with closing(requests.get(url,timeout=10, stream=True, verify=False)) as r:
                    ori_url =r.url
        
                    if ori_url != "":
                        # add the expanded original urls to a python dictionary with their count
                        if ori_url in expanded_url_dict:
                            expanded_url_dict[ori_url].append(url)
                        else:
                            expanded_url_dict[ori_url] = [url]
                        i+=1
            except :
                print sys.exc_info()[0]
                e = e +1
        print "urls expanded: ", i
        print "bad Urls: ",e
        
        print "Orig Url dic len: ", len(expanded_url_dict)
        fs = open("short_origURLsMapping_" + archiveID +".txt","w")
        for ourl,surls in expanded_url_dict.items():
            fs.write(ourl +":--"+",".join(surls)+"\n")
        fs.close()
        
        # sort expanded_url_dict in descending order of the url count
        #sorted_list = sorted(expanded_url_dict.items(), key=lambda x: len(x[1]), reverse=True)
        
        
        
        fs = open("origURLs_" + archiveID +".txt","w")
        for ourl,v in sorted_list:
            fs.write(ourl +"," + str(v)+"\n")
        fs.close()
        
        #Retrieve Long URLs
        #-------------------------
        freqOrigURLs = []
        for u,v in sorted_list:
            if v > thresh:
                freqOrigURLs.append(u)
        print len(freqOrigURLs)
        webpages=[]
        #try:
        #rs=[grequests.get(u,timeout=10) for u,v in sorted_list]
        rs=[grequests.get(u,timeout=10) for u in freqOrigURLs]
        
        re= grequests.map(rs)
        #except:
        #    print sys.exc_info()[0]
        
        #for url,_ in sorted_list:
        print len(re)
        for r in re:
            page = r.content
            url = r.url
            #with closing(requests.get(url,timeout=10, stream=True)) as r:
            #    page = r.text or r.content
            soup = BeautifulSoup(page)
            title = ""
            text = ""
            if soup.title:
                if soup.title.string:
                    title = soup.title.string
            
            comments = soup.findAll(text=lambda text:isinstance(text,Comment))
            [comment.extract() for comment in comments]
            text_nodes = soup.findAll(text=True)
            
            visible_text = filter(visible, text_nodes)
            text = ''.join(visible_text)
            #text = title + " " + text
            webpages.append((url,title, text))
        print "URLs downloaded"
        print len(webpages)
    
    
    #Index retrieved webpages into SOLR
    #----------------------------------------
    for url,title, webpage in webpages:
        
        html_id = hashlib.md5(url).hexdigest()
        doc = {"id":html_id, "content":webpage, "title":title, "collection_id":archiveID, "url":url, "event":event, "event_type":event_type}
        
        # attempt to add it to the index, make sure to commit later
        #try:
        solr_instance.add(doc)
        #except Exception as inst:
        #    print "Error indexting file, with message" + str(inst)
    
    try:
        solr_instance.commit()
    except:
        print "Could not Commit Changes to Solr, check the log files."
    else:
        print "Successfully committed changes"
    '''
if __name__ == "__main__":
    batchProcessing()
