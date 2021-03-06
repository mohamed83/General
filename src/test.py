import sys
import requests
#import hashlib
from bs4 import BeautifulSoup,Comment
import re
#import sunburnt
#import pymysql
from operator import itemgetter
from contextlib import closing
import scripts.eventUtils as eu

sources = []
lines = []
with open('/Users/mmagdy/Dropbox/z_40_Sources.txt','r') as f:
    lines = f.readlines()
    
for l in lines:
    l = l.strip()
    p,s,v = l.split(",")
    sources.append((p,int(s),v))
sources = eu.getSorted(sources, 1)
s = sum([f for _,f,_ in sources ])
print s
'''
with open('/Users/mmagdy/Dropbox/z_40_Sources2.txt','w') as f:
    lines = "\n".join([p +","+str(s)+","+ v for p,s,v in sources])
    f.write(lines)
'''
print sources
'''
urls = []
f = open('/Users/mmagdy/Dropbox/shortURLs.txt','r')
urls = f.readlines()
f.close()
urls = [u.strip() for u in urls]
expanded_url_dict = {}
i = 0
e=0
for url in urls:
    with closing(requests.get(url,timeout=10, stream=True, verify=False)) as r:
                #page = r.text or r.content
        if r.status_code == requests.codes.ok:
            
            ori_url =r.url
                # add the expanded original urls to a python dictionary with their count
            if ori_url in expanded_url_dict:
                expanded_url_dict[ori_url].append(url)
            else:
                expanded_url_dict[ori_url] = [url]
                i+=1
            
        else:
            e = e+1
        print r.status_code
'''
'''
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head']:
        return False
    return True

thresh = 10
archiveID = sys.argv[1].split(".")[0]

tweetFile = sys.argv[1]
#tweetFile = archiveID+'.csv'
#Read Tweets from given file
#-------------------------------
#solr_instance = sunburnt.SolrInterface(solr_url)

#conn = pymysql.connect(host="spare05.dlib.vt.edu", user="ctrnet", passwd="tweetctr!!", db="twapperkeeper_2",charset='utf8')
#cursor = conn.cursor()

#query = "select id,text from twapperkeeper_2." + archiveID + " where iso_language_code like 'en'"
#print query
#cursor.execute(query)
tweets = []
f = open(tweetFile,"r")
us = f.readlines()
f.close()
for l in us[1:]:
    l = l.strip()
    p = l.split("\t")
    t = p[0]
    tweets.append(t)

docs=[]

print "tweets is read from File"

# Extract short URLs from Tweets
#-------------------------------
shortURLsList =[]
#for row in cursor.fetchall():
for line in tweets:    
    #line = row[1]
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
    while url.endswith("."):
        url = url[:-1]
    surls.append(url)
print "cleaned short URLs: ", len(surls)
surlsDic ={}
for url in surls:
    if url in surlsDic:
        surlsDic[url] = surlsDic[url] + 1
    else:
        surlsDic[url] = 1
print "Unique short URLs: ", len(surlsDic)
sorted_list = sorted(surlsDic.iteritems(), key=itemgetter(1), reverse=True)
#print "sorted"
#print len(sorted_list)
freqShortURLs =[]

for surl,v in sorted_list:
    if v > thresh:
        freqShortURLs.append(surl)
print "Freq short URLs (>"+str(thresh)+"): ",len(freqShortURLs)

fs = open("shortURLs_" + archiveID +".txt","w")
for surl,v in sorted_list:
    fs.write(surl +"," + str(v)+"\n")
fs.close()
# Expand Short URLs
#-------------------------------
expanded_url_dict = {}
#freqShortURLs = freqShortURLs[:2000]
i=0
e=0
webpages=[]
for url in freqShortURLs:
    try:
        with closing(requests.get(url,timeout=10, stream=True, verify=False)) as r:
            #page = r.text or r.content
            if r.status_code == requests.codes.ok:
                
                ori_url =r.url
            
                if ori_url != "":
                    # add the expanded original urls to a python dictionary with their count
                    if ori_url in expanded_url_dict:
                        expanded_url_dict[ori_url].append(url)
                    else:
                        expanded_url_dict[ori_url] = [url]
                        i+=1
                        page = r.content or r.text
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
    except :
        print sys.exc_info()[0],url
        e = e +1
print "Unique Orig URLs expanded: ", i
print "Bad URLs: ",e

#print "Unique Orig URLs: ", len(expanded_url_dict)
fo = open('seedsURLs_'+archiveID+'.txt','w')
fs = open("short_origURLsMapping_" + archiveID +".txt","w")
for ourl,surls in expanded_url_dict.items():
    fs.write(ourl +":--"+",".join(surls)+"\n")
    fo.write(ourl+'\n')
fs.close()
fo.close()

#Saving Webpages text to file
i=1
for wp in webpages:
    f = open(str(i)+'.txt','w')
    cont = wp[1]+ ' ' + wp[2]
    f.write(cont.encode('utf8'))
    f.close()
    i+=1

print "Webpages text saved"

#Retrieve Original URLs
#-------------------------
# sort expanded_url_dict in descending order of the url count
esorted_list = sorted(expanded_url_dict.iteritems(), key=lambda x: len(x[1]), reverse=True)
webpages=[]
for url,_ in esorted_list:
    page = ''
    try:
        #r = requests.get(url,timeout=10,verify=False)
        with closing(requests.get(url,timeout=10, verify=False)) as r:
            page = r.content or r.text
    except:
        print sys.exc_info()[0], url
        continue
    
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
print "URLs downloaded: ", len(webpages)
'''

'''
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