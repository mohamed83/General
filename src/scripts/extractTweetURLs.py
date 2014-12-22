import re
import sys
import datetime
from operator import itemgetter # to sort dictionaries by the values in (key, value) pairs

thresh = 1


#inFile = open("ferrysank.csv", "r")
print sys.argv[1]
inFile = open(sys.argv[1], "r")
filename = sys.argv[1].split(".")[0]
outFile = open(filename+"_shortenedURLs.txt", "w+")

shortURLsList = []

# extract short URLs from the tweets --------------------------
#while line:
start_time = datetime.datetime.now()
for line in inFile:
	#print line
	if line.startswith("\"twitter-search\""):
		parts = line.split("\",\"") 
		if len(parts) > 6:
			if parts[6] != "en":
				#print "not en"
				continue
		#else:
		#	print "lang not found"
		
		line = parts[1]
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
	#if url in ["http://t.co","http://t.co/","https://t","http://t","http://t.c","http://t.","https://t."]:
	#	continue
	#else:
	surls.append(url)
print "List cleaned"
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
print "sorted"

#print len(sorted_list)
freqShortURLs =[]

for surl,v in sorted_list:
	if v > thresh:
		freqShortURLs.append(surl)

print len(freqShortURLs)

#for surl in shortURLsList:
for surl in freqShortURLs:
	outFile.write(surl+"\n")

# check end time ----------------------------------------------
end_time = datetime.datetime.now()
diff = end_time - start_time
print "Seconds to process tweets: " + str(diff.seconds)
print "\nMinutes to process tweets: " +str(diff.seconds/60)
print "\nHours to process tweets: " +str(diff.seconds/3600)

inFile.close()
outFile.close()

