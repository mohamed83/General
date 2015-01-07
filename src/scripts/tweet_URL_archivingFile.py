import sys
import requests
#import hashlib
#from bs4 import BeautifulSoup,Comment
import re
#import sunburnt
#import pymysql
from operator import itemgetter
from contextlib import closing


def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head']:
		return False
	return True

thresh = 10
archiveID = "z_534"
#solr_instance = solr.Solr(solr_url)

#tweetFile = sys.argv[1]
tweetFile = '../'+archiveID+'.csv'
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
for l in f:
	l = l.strip()
	p = l.split(",")
	t = p[1]
	tweets.append(t)
f.close()
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
	while url.endswith("."):
		url = url[:-1]
	surls.append(url)
print "cleaned"
print len(surls)
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
print "Freq URLs: ",len(freqShortURLs)

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
for url in freqShortURLs:
	try:
		with closing(requests.get(url,timeout=10, stream=True, verify=False)) as r:
			#page = r.text or r.content
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
fo = open('seedsURLs_'+archiveID+'.txt','w')
fs = open("short_origURLsMapping_" + archiveID +".txt","w")
for ourl,surls in expanded_url_dict.items():
	fs.write(ourl +":--"+",".join(surls)+"\n")
	fo.write(ourl+'\n')
fs.close()
fo.close()

# sort expanded_url_dict in descending order of the url count
#sorted_list = sorted(expanded_url_dict.iteritems(), key=lambda x: len(x[1]), reverse=True)
#print "sorted"
'''
fs = open("origURLs.txt","w")
for ourl,v in sorted_list:
	fs.write(ourl +"," + str(v)+"\n")
fs.close()
'''
#Retrieve Long URLs
#-------------------------
'''
webpages=[]
for url,_ in sorted_list:
	try:
		r = requests.get(url,timeout=10,verify=False)
	except:
		print sys.exc_info()[0]
		continue
	page = r.content or r.text
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
'''
#Index retrieved webpages into SOLR
#----------------------------------------
'''
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
else:
	print "Successfully committed changes"
'''