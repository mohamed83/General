'''
Created on Oct 10, 2014

@author: dlrl
'''
import nltk
import sys
from bs4 import BeautifulSoup, Comment
import requests
from nltk.corpus import stopwords
from readability.readability import Document
from operator import itemgetter

import ner


stopwordsList = stopwords.words('english')
stopwordsList.extend(["news","people","said","comment","comments","share","email"])

def getEntities(texts):
        
        if type(texts) != type([]):
            texts = [texts]   
        """
        Run the Stanford NER in server mode using the following command:
        java -mx1000m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/english.muc.7class.distsim.crf.ser.gz -port 8080 -outputFormat inlineXML
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
    tokens = [t for t in tokens if len(t)>2]
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
        sentences = [s for sent in sentences for s in sent.split("\n") if len(s) > 3]
        cleanSents = [sent.strip() for sent in sentences if len(sent.split()) > 3]
        sents.extend(cleanSents)
    return sents

def _cleanSentences(sents):
    sentences = [s for sent in sents for s in sent.split("\n") if len(s) > 3]
    cleanSents = [sent.strip() for sent in sentences if len(sent.split()) > 3]
    return cleanSents

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
            print sys.exc_info()
            #text = ""
            text = {}
        webpagesText.append(text)
    return webpagesText