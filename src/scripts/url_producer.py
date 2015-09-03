import sys
import requests
import hashlib
from bs4 import BeautifulSoup,Comment
import re
import pymysql
from operator import itemgetter
from contextlib import closing

def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head']:
		return False
	return True

def produce_url():
	thresh = 1
	archiveID = "z_447"
	event = "Marsyville_School_Shooting"
	event_type = "Shooting"
	
	#Read Tweets from mysql DB (
	#-------------------------------

	conn = pymysql.connect(host="lancelot.dlib.vt.edu", user="mmagdy", passwd="pw4mmagdy", db="twitter",charset='utf8')
	cursor = conn.cursor()

	query = "select id,text from twitter." + archiveID + " where iso_language_code like 'en'"
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
		url_li = re.findall(regExp, line)
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
	freqShortURLs =[]

	for surl,v in sorted_list:
		if v > thresh:
			freqShortURLs.append(surl)
	print len(freqShortURLs)
	fs = open("shortURLs.txt","w")
	for surl,v in sorted_list:
		fs.write(surl +"," + str(v)+"\n")
	fs.close()
	
	# Expand Short URLs
	#-------------------------------
	expanded_url_dict = {}
	i=0
	e=0
	for url in freqShortURLs:
		try:
			with closing(requests.get(url,timeout=10, stream=True, verify=False)) as r:
				#page = r.text or r.content
				ori_url = r.url
		
			if ori_url != "":
				if ori_url in expanded_url_dict:
					expanded_url_dict[ori_url] = expanded_url_dict[ori_url] + 1
				else:
					expanded_url_dict[ori_url] = 1
					surlsDic[url]=[surlsDic,ori_url]
				i+=1
			
			
		
		except :
			print sys.exc_info()[0]
			e = e +1
	print "urls expanded"
	print i
	print e

	print len(expanded_url_dict)
	sorted_list = sorted(expanded_url_dict.iteritems(), key=itemgetter(1), reverse=True)


	# This file should have the expanded urls
	fs = open("seeds.txt","w")
	for ourl, v in sorted_list:
		fs.write(ourl + "\n")
	fs.close()
	
	# Using this list, request the urls and then index and add to solr
	
