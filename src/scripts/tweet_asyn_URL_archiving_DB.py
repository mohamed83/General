import sys
import requests
import hashlib
from bs4 import BeautifulSoup,Comment
import re
import sunburnt
import pymysql
from operator import itemgetter
from contextlib import closing
import grequests

import logging
logging.basicConfig(filename='output.log',format='%(asctime)s %(message)s',level=logging.DEBUG)

#logging.info(message)

def eh(request,exception):
	print 'request failed'

def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head']:
		return False
	return True

thresh = 0
solr_url = "http://jingluo.dlib.vt.edu:8080/solr/"
'''
archiveID = "z_279"
event = "9/11_Anniversary"
event_type = "Building_Collapse"
'''

archiveID = "z_225"
event = "Ebola"
event_type = "Disease_Outbreak"

#solr_instance = solr.Solr(solr_url)

#Read Tweets from mysql DB
#-------------------------------
solr_instance = sunburnt.SolrInterface(solr_url)
'''
conn = pymysql.connect(host="spare05.dlib.vt.edu", user="ctrnet", passwd="tweetctr!!", db="twapperkeeper_2",charset='utf8')
cursor = conn.cursor()

#f = open(sys.argv[1],"r")
query = "select id,text from twapperkeeper_2." + archiveID + " where iso_language_code like 'en'"
print query
cursor.execute(query)
docs=[]

print "tweets read from DB"

# Extract short URLs from Tweets
#-------------------------------
shortURLsList =[]
for row in cursor.fetchall():
	
	line = row[1]
	regExp = "(?P<url>https?://[a-zA-Z0-9\./-]+)"
	url_li = re.findall(regExp, line)  # find all short urls in a single tweet
	while (len(url_li) > 0): 
		shortURLsList.append(url_li.pop())
print "short Urls extracted"
print len(shortURLsList)
surls = []
for url in shortURLsList:
	i = url.rfind("/")
	if i+1 >= len(url):
		continue
	p = url[i+1:]
	if len(p) < 10:
		continue
	surls.append(url)
print "cleaned"
print len(surls)
surlsDic ={}
for url in surls:
	if url in surlsDic:
		surlsDic[url] = surlsDic[url] + 1
	else:
		surlsDic[url] = 1
print "dic created"
print len(surlsDic)
sorted_list = sorted(surlsDic.iteritems(), key=itemgetter(1), reverse=True)
#print "sorted"
#print len(sorted_list)
freqShortURLs =[]

for surl,v in sorted_list:
	if v > thresh:
		freqShortURLs.append(surl)
print len(freqShortURLs)

fs = open("shortURLs.txt","w")
for surl,v in sorted_list:
	fs.write(surl +"," + str(v)+"\n")
fs.close()
'''
# Expand Short URLs
#-------------------------------
expanded_url_dict = {}
#freqShortURLs = freqShortURLs[:2000]
i=0
e=0

freqShortURLs = []
f = open("shortURLs.txt","r")
for line in f:
	freqShortURLs.append(line.strip().split(",")[0])
f.close()
freqShortURLs= freqShortURLs[10000:20000]

for url in freqShortURLs:
	try:
		with closing(requests.get(url,timeout=10, stream=True, verify=False)) as r:
			#page = r.text or r.content
			ori_url =r.url
		
		if ori_url != "":
			# add the expanded original urls to a python dictionary with their count
			if ori_url in expanded_url_dict:
				expanded_url_dict[ori_url] = expanded_url_dict[ori_url] + 1
			else:
				expanded_url_dict[ori_url] = 1
			i+=1
			if i%1000 == 0:
				print "Unshortened %s short URLs" % str(i)
				logging.info("Unshortened %s short URLs" , str(i))
			
		
	except :
		print sys.exc_info()[0]
		e = e +1
print "urls expanded"
logging.info("urls expanded")
print i
logging.info("Valid URLs: %s",i)
print e
logging.info("Invalid URLs: %s",e)

print len(expanded_url_dict)
logging.info("Unique URLs %s",len(expanded_url_dict))
# sort expanded_url_dict in descending order of the url count
sorted_list = sorted(expanded_url_dict.iteritems(), key=itemgetter(1), reverse=True)
#print "sorted"

fs = open("origURLs.txt","w")
for ourl,v in sorted_list:
	fs.write(ourl +"," + str(v)+"\n")
fs.close()

#Retrieve Long URLs
#-------------------------
webpages=[]
#try:
rs=[grequests.get(u,timeout=10) for u,v in sorted_list]

re= grequests.map(rs)
#except:
#	print sys.exc_info()[0]

#for url,_ in sorted_list:
print len(re)
for r in re:
	'''
	try:
		r = requests.get(url,timeout=10,verify=False)
	except:
		print sys.exc_info()[0]
		continue
	
	page = r.content or r.text
	'''
	page = r.content
	url = r.url
	#with closing(requests.get(url,timeout=10, stream=True)) as r:
	#	page = r.text or r.content
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
logging.info("URLs Downloaded")
print len(webpages)
logging.info("No of webpages: %s", len(webpages))
#Index retrieved webpages into SOLR
#----------------------------------------
for url,title, webpage in webpages:
	
	html_id = hashlib.md5(url).hexdigest()
	doc = {"id":html_id, "content":webpage, "title":title, "collection_id":archiveID, "url":url, "event":event, "event_type":event_type}
	
	# attempt to add it to the index, make sure to commit later
	#try:
	solr_instance.add(doc)
	#except Exception as inst:
	#	print "Error indexting file, with message" + str(inst)

try:
	solr_instance.commit()
except:
	print "Could not Commit Changes to Solr, check the log files."
	logging.info("Could not Commit Changes to Solr, check the log files.")
else:
	print "Successfully committed changes"
	logging.info("Successfully committed changes")