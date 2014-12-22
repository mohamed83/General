#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
'''
Created on Oct 10, 2014

@author: dlrl
'''
import nltk
import sys, os
import re
from bs4 import BeautifulSoup, Comment
import requests
from nltk.corpus import stopwords
from readability.readability import Document
from operator import itemgetter
import warcunpack_ia
from contextlib import closing
from hanzo.warctools import ArchiveRecord, WarcRecord
import logging

import ner
from gensim import corpora, models

stopwordsList = stopwords.words('english')
stopwordsList.extend(["news","people","said","comment","comments","share","email","new","would","one","world"])
allSents = []

def getEntities(texts):
        
        if type(texts) != type([]):
            texts = [texts]   
        """
        Run the Stanford NER in server mode using the following command:
        java -mx1000m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/english.muc.7class.distsim.crf.ser.gz -port 8000 -outputFormat inlineXML
        """
        
        tagger = ner.SocketNER(host='localhost',port=8000)
        entities = []
        for t in texts:
            sentence_entities = tagger.get_entities(t)
            entities.append(sentence_entities)
        return entities

def isListsDisjoint(l1,l2):
    s1 = set(l1)
    s2 = set(l2)
    return s1.isdisjoint(s2)

def getIntersection(l1,l2):
    s1 = set(l1)
    s2 = set(l2)
    return s1.intersection(s2)

def readFileLines(filename):
    f = open(filename,"r")
    lines = f.readlines()
    return lines
        

def getSorted(tupleList,fieldIndex):
    sorted_list = sorted(tupleList, key=itemgetter(fieldIndex), reverse=True)
    return sorted_list

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head']:
        return False
    return True

def getTokens(texts):
    tokens=[]
    if type(texts) != type([]):
        texts = [texts]
    for s in texts:
        toks = nltk.word_tokenize(s.lower())
        tokens.extend(toks)
    tokens = [t.lower() for t in tokens if len(t)>2]
    tokens = [t for t in tokens if t not in stopwordsList]
    return tokens

def getFreq(tokens):
    return nltk.FreqDist(tokens)

def getSentences(textList =[]):
    #stopwordsList = stopwords.words('english')
    #stopwordsList.extend(["news","people","said"])
    if type(textList) != type([]):
        textList = [textList]
    sents = []
    for text in textList:
        sentences = nltk.sent_tokenize(text)
        newSents = []
        for s in sentences:
			if len(re.findall(r'.\..',s))>0:
				ns = re.sub(r'(.)\.(.)',r'\1. \2',s)
				newSents.extend(nltk.sent_tokenize(ns))
			else:
				newSents.append(s)

        sentences = newSents
        sentences = [s for sent in sentences for s in sent.split("\n") if len(s) > 3]
        cleanSents = [sent.strip() for sent in sentences if len(sent.split()) > 3]
        sents.extend(cleanSents)
    return sents

def _cleanSentences(sents):
    sentences = [s for sent in sents for s in sent.split("\n") if len(s) > 3]
    cleanSents = [sent.strip() for sent in sentences if len(sent.split()) > 3]
    return cleanSents


def getLDATopics(documents):
	texts = []
	for doc in documents:
		docToks = getTokens(doc)
		texts.append(docToks)
		
		
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]

	notopics = 3
	lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=notopics)


	outputTopics = []
	for i in range(0, lda.num_topics):
		
		#outputTopics.append( "Topic"+ str(i+1) + ":"+ lda.print_topic(i))
		t = lda.show_topic(i)
		#print type(t)
		t = [w for _,w in t]
		#for tu in t:
		#	print tu[1]
		outputTopics.append( "Topic"+ str(i+1) + ":"+ ", ".join(t))
	return "<br>".join(outputTopics)

def extractMainArticle(html):
    p = Document(html)
    readable_article = p.summary()
    readable_title = p.short_title()
    
    soup = BeautifulSoup(readable_article)
    text_nodes = soup.findAll(text=True)
    text = ''.join(text_nodes)
    
    #text = readable_title + " " + text
    #return text
    
    wtext = {"title":readable_title, "text": text}
    return wtext

def extractTextFromHTML(page):
    try:
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
        
        #text = title + text
        wtext = {"text":text,"title":title}
    except:
        print sys.exc_info()
        #text = ""
        wtext = {}
    #return text
    return wtext

def getWebpageText(URLs = []):
    webpagesText = []
    if type(URLs) != type([]):
        URLs = [URLs]
    for url in URLs:
        try:
            page = requests.get(url).content
            #text = extractMainArticle(page)
            text = extractTextFromHTML(page)
        except:
            #print sys.exc_info()
            #text = ""
            text = {}
        webpagesText.append(text)
    return webpagesText

#Get Frequent Tokens
def getFreqTokens(texts):
	tokens = getTokens(texts)
	f = getFreq(tokens)
	tokensFreqs = f.items()
	sortedTokensFreqs = getSorted(tokensFreqs,1)
	return sortedTokensFreqs

def getIndicativeWords(texts):
	global allSents
	#Get Indicative tokens
	toksTFDF,allSents = getTokensTFDF(texts)
	
	#sortedToksTFDF = sorted(filteredToksTFDF, key=lambda x: x[1][0]*x[1][1], reverse=True)
	sortedToksTFDF = sorted(toksTFDF.items(), key=lambda x: x[1][0]*x[1][1], reverse=True)
	return sortedToksTFDF
	
def getIndicativeSents(sortedToksTFDF,topK,intersectionTh):
	# Get Indicative Sentences
	topToksTuples = sortedToksTFDF[:topK]
	topToks = [k for k,_ in topToksTuples]
	allImptSents = []
	
	impSentsF = {}
	for sents in allSents:
		impSents ={}
		for sent in sents:
			if sent not in impSents:
				sentToks = getTokens(sent)
				if len(sentToks) > 100:
					continue
				intersect = getIntersection(topToks, sentToks)
				if len(intersect) > intersectionTh:
					impSents[sent] = len(intersect)
					if sent not in impSentsF:
						impSentsF[sent] = len(intersect)
		allImptSents.append(impSents)
	
	sortedImptSents = getSorted(impSentsF.items(),1)
	return sortedImptSents

def getEventModelInsts(sortedImptSents):
		
	eventModelInstances = []
	for sent in sortedImptSents:
		sentEnts = getEntities(sent[0])[0]
		eventModelInstances.append(sentEnts)
	return eventModelInstances


def getTokensTFDF(texts):
	tokensTF = []
	#allTokensList=[]
	allTokens = []
	allSents = []
	for t in texts:
		sents = getSentences(t)
		toks = getTokens(sents)
		toksFreqs = getFreq(toks)
		allTokens.extend(toksFreqs.keys())
		#allTokensList.append(toks)
		allSents.append(sents)
		sortedToksFreqs = getSorted(toksFreqs.items(), 1)
		tokensTF.append(sortedToksFreqs)
	tokensDF = getFreq(allTokens).items()
	tokensTFDF = {}
	for t in tokensTF:
		for tok in t:
			if tok[0] in tokensTFDF:
				tokensTFDF[tok[0]] += tok[1]
			else:
				tokensTFDF[tok[0]] = tok[1]
	for t in tokensDF:
		tokensTFDF[t[0]] = (tokensTFDF[t[0]],t[1])
	
	return tokensTFDF,allSents
	
	
	
def parseLogFileForHtml(log_file):
    htmlList = []
    
    with open(log_file, 'r+b') as f:
        for line in f:
            splitext = line.split('\t')
            if len(splitext) >= 9:
                content_type = splitext[6]
                if content_type.find("text/html") == 0:
                    htmlList.append({"file":splitext[7], "wayback_url":splitext[8], "url":splitext[5]})
                
    return htmlList

# Extracts text from a given HTML file and indexes it into the Solr Instance
def extractText(html_files):
    textFiles = []
    #print html_files
    titles = {}
    for f in html_files:
    	#print f
        html_file = f["file"].strip()
        file_url = f["url"].strip()
        wayback_url = f["wayback_url"].strip()
        # read the file into a string so beautifulsoup can use it 
        #print html_file
        try:   
        	html_fileh = open(html_file, "r")
        	html_string = html_fileh.read()
        	#print html_string
        except:
        	print "Error reading"
        	logging.exception('')
        
        if len(html_string) < 1:
            print "error parsing html file " + str(html_file)
            continue
        try:   
            #soup = BeautifulSoup(html_string)
            d = extractTextFromHTML(html_string)
            #print d['text']
        except:
            print "Error: Cannot parse HTML from file: " + html_file
            #print sys.exc_info()
            logging.exception('')
            continue    
        
        
        
        title = d['title']
        if title and title in titles:
            print "Title already exists"
            continue
        else:
            titles[title]=1
        html_body = d['text']
        textFiles.append(html_body)
	
    return textFiles

        #html_id = hashlib.md5(file_url).hexdigest()
        
    #     text_file = open(html_file + ".txt", "w+b")
    #     text_file.write(html_body)
    #     text_file.close()

# Processes the given directory for .warc files
#def main(argv):
def expandWarcFile(warcFile):
#     if (len(argv) < 1):
#         print >> sys.stderr, "usage: processWarcDir.py -d <directory> -i <collection_id> -e <event> -t <event_type>"
#         sys.exit()
#         
#     if (argv[0] == "-h" or  len(argv) < 4):
#         print >> sys.stderr, "usage: processWarcDir.py -d <directory> -i <collection_id> -e <event> -t <event_type>"
#         sys.exit()
    
    
    rootdir = os.path.dirname(warcFile)
    filename = os.path.basename(warcFile)
    filePath =warcFile
    if filename.endswith(".warc") or filename.endswith(".warc.gz"):# or filename.endswith(".arc.gz"):
		# processWarcFile(filePath, collection_id, event, event_type)
		splitext = filePath.split('.')
		output_dir = splitext[0] + "/"
		
		log_file = os.path.join(output_dir, filePath[filePath.rfind("/")+1:] + '.index.txt')
		
		# output_file = output_dir + filePath.split("/")[1] + ".index.txt"
		if os.path.exists(output_dir) == False:                    
		
			os.makedirs(output_dir)

			# unpackWarcAndRetrieveHtml(filePath, collection_id, event, event_type)
			# output_dir = filePath.split(".")[0] + "/"
			default_name = 'crawlerdefault'
			wayback = "http://wayback.archive-it.org/"
			collisions = 0
				
			#log_file = os.path.join(output_dir, filePath[filePath.rfind("/")+1:] + '.index.txt')
			
			log_fileh = open(log_file, 'w+b')
			warcunpack_ia.log_headers(log_fileh)
		
			try:
				with closing(ArchiveRecord.open_archive(filename=filePath, gzip="auto")) as fh:
					collisions += warcunpack_ia.unpack_records(filePath, fh, output_dir, default_name, log_fileh, wayback)
		
			except StandardError, e:
				print >> sys.stderr, "exception in handling", filePath, e
				return
		else:
			print "Directory Already Exists"
		
			#print "Warc unpack finished"
		
		html_files = parseLogFileForHtml(log_file)
		#print "Log file parsed for html files pathes"
		#print len(html_files)
		
		# for i in html_files:
			# extractTextAndIndexToSolr(i["file"], i["url"], i["wayback_url"], collection_id, event, event_type)
		tf = extractText(html_files)
		#print "extracting Text finished"
		return tf