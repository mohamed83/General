# Filename: ext_unique_urls3.py
# Description: This file extracts shortened urls from a text file that is provided as 
#              the first argument. The extracted shortened urls are expanded. 
#              Unique urls are written to an output file, whose name is provided as the second argument.
# Usage: shell> python ext_unique_urls3.py inputfilename.txt outputfilename.txt
# Name: Seungwon Yang  <seungwon@vt.edu>
# Date: Jan. 25, 2012

import base64
import sys
import re
# import urllib
# import urllib2
import datetime
from operator import itemgetter # to sort dictionaries by the values in (key, value) pairs
from contextlib import closing
import requests

def getLongUrl(url):
	visited = []
	#if url in ["http://t.co","http://t.co/","https://t.co/","https://t.co","https://t.c","https://t","https://t.","http://t.c"]:
	#	return ""
	#try:
	response = requests.head(url)
	if response.status_code/100 == 4:
		return ""
	while response.status_code/100 == 3:

		url = response.headers['location']
		print url
		if url in visited:
			l = [(u,len(u)) for u in visited]
			lsorted = sorted(l, key=lambda l: l[1])
			return lsorted[0][0]
		response = requests.head(url)
		visited.append(url)
	if response.status_code/100 == 2:
		return url
	else:
		return ""
	#except ValueError:
	#	print "e" + str(sys.exc_info()[0])
	#	return ""

# check start time -------------------------------------------
start_time = datetime.datetime.now()

# Open the input data file, and the output file --------------
#ifd = open(sys.argv[1], "r")
ifd = open(sys.argv[1], "r")
filename = sys.argv[1].rsplit("_")[0]
ofd = open(filename+"_extractedURLs.txt", "w+")


expanded_url_dict = {}
# Once we collect short urls, next step is to expand each url to its original form
# considering that two different short urls might point to the same webiste.
i = 0
e = 0
for line in ifd:
	line = line.strip()
	try:
		#if line in ["http://t.co","http://t.co/","https://t","http://t","http://t.c"]:
		#	e = e+1
		#	continue
		#print line
		
		#ori_url = requests.get(line, timeout=10,stream=True).url

		with closing(requests.get(line,timeout=10, stream=True)) as r:
			ori_url =r.url
		
		#ori_url = requests.get(line).url
		#ori_url = getLongUrl(line)
		
		if ori_url != "":
			# add the expanded original urls to a python dictionary with their count
			if ori_url in expanded_url_dict:
				expanded_url_dict[ori_url] = expanded_url_dict[ori_url] + 1
			else:
				expanded_url_dict[ori_url] = 1
			i+=1
	
	except:  # ignore the exceptions/HTTP errors, and simply process the next tweet
		print "erro" + str(sys.exc_info()[0])
		e = e +1
print "urls expanded"
print i
print e
		

print len(expanded_url_dict)
# sort expanded_url_dict in descending order of the url count
sorted_list = sorted(expanded_url_dict.iteritems(), key=itemgetter(1), reverse=True)
print "sorted"
# add the urls to a list, in descending order of their count
#total = 0
for expanded_url, count in sorted_list:
	ofd.write(expanded_url + "," + str(count)+"\n")
	#total = total + count
	
#print total

# check end time ----------------------------------------------
end_time = datetime.datetime.now()
diff = end_time - start_time
time_taken = diff.seconds
hours = 0
mins = 0
secs = 0
#if time_taken >= 3600:
hours = time_taken/3600
time_taken = time_taken - hours*3600
mins = time_taken/60
time_taken = time_taken - mins * 60
secs = time_taken
print "time to process tweets: " + str(hours)+ " hours, " + str(mins) + " mins, " + str(secs) + " seconds"

#print "Seconds to process tweets: " + str(diff.seconds)
#print "\nMinutes to process tweets: " +str(diff.seconds/60)
#print "\nHours to process tweets: " +str(diff.seconds/3600)

ifd.close()
ofd.close()

