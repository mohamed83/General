#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
# Import modules for CGI handling

try:
	import sys
	import cgi, cgitb 
	#print sys.version
	import eventUtils as utils
	import logging
	
	topK = 10
	intersectionTh = 2
	warcFile = '/Users/dlrl/Dropbox/workspace/General/src/testing/test.warc.gz'
	form = cgi.FieldStorage() 
	#warc = form['uploader']
	warc = form.getvalue('uploader')
	
	
	#print warc
	#print warc.file
	if warc: #and warc.file:
		f = open(warcFile,"wb")
		f.write(warc)
		f.close()
		print "file saved"
		#warcFile = warc.file.name
		#print warcFile
		#texts = utils.expandWarcFile(warcFile)
		texts = utils.expandWarcFile(warcFile)
	else:
		texts = utils.expandWarcFile(warcFile)			

	urls = form.getvalue('urls')
	#if not urls: 
	#	urls = 'http://www.nbcnews.com/storyline/ebola-virus-outbreak/why-its-not-enough-just-eradicate-ebola-n243891\nhttp://www.npr.org/blogs/thetwo-way/2014/11/09/362770821/maine-nurse-to-move-out-of-state-following-ebola-quarantine-row'
	
	if urls:
		webpagesURLs = urls.split('\n')
		webpagesText = utils.getWebpageText(webpagesURLs)
		texts = [t['text'] for t in webpagesText if t.has_key('text') and len(t['text'])>0]
	
	print texts
	
	#Get LDA Topics
	ldaTopics = utils.getLDATopics(texts)
	
	#Get Frequent Tokens
	sortedTokensFreqs = utils.getFreqTokens(texts)

	#Get Indicative tokens
	sortedToksTFDF = utils.getIndicativeWords(texts)
	'''
	filteredToksTFDF = []
	toks = " ".join([])
	#print toks
	tokEntsDict = utils.getEntities(toks)[0]
	tokEntsList = []
	for te in tokEntsDict:
		if te in ['LOCATION','DATE']:
			tokEntsList.extend(tokEntsDict[te])
	ntokEntsList= []
	for s in tokEntsList:
		s = s.lower()
		ps = s.split()
		if len(ps) > 1:
			ntokEntsList.extend(ps)
		else:
			ntokEntsList.append(s)
	print ntokEntsList
	print '--------------'
	print toks
	for k in toksTFDF:
		if k not in ntokEntsList:
			filteredToksTFDF.append((k,toksTFDF[k]))
	'''
	
	# Get Indicative Sentences	
	sortedImptSents = utils.getIndicativeSents(sortedToksTFDF,topK,intersectionTh)
	
	# Get Event Model
	eventModelInstances = utils.getEventModelInsts(sortedImptSents)
	
	rs = "<tr>"
	re = "</tr>"
	outputs = "<td>"
	outpute = "</td>"
	wordsOutput = "<tr><td>Frequent Words (term Frequency)</td><td>Important Words (term Freq * Doc Freq)</td></tr>"
	for i in range(topK):
		wordsOutput += rs + outputs + str(sortedTokensFreqs[i]) + outpute + outputs + str(sortedToksTFDF[i]) + outpute + re
	
	sents_ents = "<tr><td>Important Sentences</td><td>Named Entities</td></tr>"
	for i in range(len(sortedImptSents)):
		sents_ents += rs + outputs + str(sortedImptSents[i]) + outpute + outputs + str(eventModelInstances[i]) + outpute + re

	print wordsOutput
	print "<br>============<br>"

	print sents_ents
	print "<br>============<br>"
	print ldaTopics
	print "</body>"
	print "</html>"
except:
	print sys.exc_info()
	logging.exception('')