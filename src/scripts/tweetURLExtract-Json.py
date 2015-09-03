import json
import sys
import cPickle
import eventUtils


#try:
#	tweets = cPickle.load(open('tweets.p','rb'))
#except:
#	tweets = []

#f = open('nepalEarthquake_tweets-2.txt','r')
def getTweets(jsonFileName):
	f = open(tweetFileName,'r')
	texts = {}
	tweets = []
	for line in f:
		l = line.strip()
		if l:
			try:
				s = json.loads(l)
				tweets.append(s)
				if 'id_str' in s:
					#if s['id_str'] in texts:
					#	continue
					if 'text' in s:
						#texts.append(s['text'])
						texts[s['id_str']] = s['text']
			except Exception as e: 
				print(e)
				print l
	f.close()
	print len(texts)
	print len(tweets)
	return texts

if __name__ == "__main__":
	
	tweetFileName = sys.argv[1]
	texts = getTweets(tweetFileName)
	shortURLs = eventUtils.extractShortURLsFreqDic(texts.values())
	f = open(tweetFileName.split(".")[0] + '-ShortURLs.txt','w')
	f.write("\n".join(shortURLs.keys()))
	f.close()
	print 'Short URLs extracted'
	#longURLs = eventUtils.shortToLongURLConversion(shortURLs)
	longURLs = eventUtils.getOrigLongURLs(shortURLs.items())
	f = open(tweetFileName.split(".")[0] + '-LongURLs.txt','w')
	f.write("\n".join(longURLs.keys()))
	f.close()
	print 'Long URLs retrieved'
	
	'''
	f = open('/Users/mmagdy/Dropbox/Nepal Earthquake/nepalEarthquakeTweets-LongURLs.txt','r')
	longURLsL = f.readlines()
	longURLsL = [(l.strip(),[(1,1)]) for l in longURLsL]
	longURLs = dict(longURLsL)
	f.close()
	sourcesFreq = eventUtils.getSourceFreqDic(longURLs)
	tweetFileName = 'nepalEarthquakeTweets.txt'
	sourcesFilename = tweetFileName.split(".")[0] + '-Sources.txt'
	eventUtils.saveSourcesFreqDic(sourcesFreq, sourcesFilename)
	print 'Sources extracted'
	'''