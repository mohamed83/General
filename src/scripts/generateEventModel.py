'''
Created on Nov 24, 2014

@author: mmagdy
'''
#!/usr/bin/env python
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
# Import modules for CGI handling


def getTokensTFDF(texts):
    tokensTF = []
    #allTokensList=[]
    allTokens = []
    allSents = []
    for t in texts:
        sents = utils.getSentences(t)
        toks = utils.getTokens(sents)
        toksFreqs = utils.getFreq(toks)
        allTokens.extend(toksFreqs.keys())
        #allTokensList.append(toks)
        allSents.append(sents)
        sortedToksFreqs = utils.getSorted(toksFreqs.items(), 1)
        tokensTF.append(sortedToksFreqs)
    tokensDF = utils.getFreq(allTokens).items()
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

#try:
import sys
import cgi, cgitb 
import utils
#from eventUtils import getWebpageText, getTokens, getFreq, getSorted, getSentences, getIntersection, getEntities
# Create instance of FieldStorage

form = cgi.FieldStorage() 

# Get data from fields
urls = form.getvalue('urls')
if not urls: 
    urls = 'http://www.nbcnews.com/storyline/ebola-virus-outbreak/why-its-not-enough-just-eradicate-ebola-n243891\nhttp://www.npr.org/blogs/thetwo-way/2014/11/09/362770821/maine-nurse-to-move-out-of-state-following-ebola-quarantine-row'
topK = 10
intersectionTh = 2

webpagesURLs = urls.split('\n')
webpagesText = utils.getWebpageText(webpagesURLs)
texts = [t['text'] for t in webpagesText if t.has_key('text') and len(t['text'])>0]

#Get Frequent Tokens
tokens = utils.getTokens(texts)
f = utils.getFreq(tokens)
tokensFreqs = f.items()
sortedTokensFreqs = utils.getSorted(tokensFreqs,1)

#Get Indicative tokens
toksTFDF,allSents = getTokensTFDF(texts)

#sortedToksTFDF = sorted(filteredToksTFDF, key=lambda x: x[1][0]*x[1][1], reverse=True)
sortedToksTFDF = sorted(toksTFDF.items(), key=lambda x: x[1][0]*x[1][1], reverse=True)
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
topToksTuples = sortedToksTFDF[:topK]
topToks = [k for k,_ in topToksTuples]
allImptSents = []
'''
uSents= []
for sts in allSents:
    for s in sts:
        if s not in uSents:
            uSents.append(s)
'''
impSentsF = {}
for sents in allSents:
#for sent in uSents:
    #impSents =[]
    impSents ={}
    for sent in sents:
        if sent not in impSents:
            sentToks = utils.getTokens(sent)
            if len(sentToks) > 100:
                continue
            intersect = utils.getIntersection(topToks, sentToks)
            if len(intersect) > intersectionTh:
                #impSents.append((sent,len(intersect)))
                impSents[sent] = len(intersect)
                if sent not in impSentsF:
                    #impSentsF.append((sent,len(intersect)))
                    impSentsF[sent] = len(intersect)
    allImptSents.append(impSents)

sortedImptSents = utils.getSorted(impSentsF.items(),1)

#print 'testing <br>' + str(len(allImptSents))
#try:
#    impsents = [s.replace("\"","") for isents in allImptSents for s in isents]
#    st = "\n".join(impsents)
#    print st.encode("utf-8")
#except:
#    print sys.exc_info()

# Get Indicative Entities    
eventModelInstances = []
#for sents in allImptSents:
#    evtModelInstance = {}
#    for sent in sents:
for sent in sortedImptSents:
    sentEnts = utils.getEntities(sent[0])[0]
    #evtModelInstance["Topic"] = list(intersec
    #if sentEnts and sentEnts not in eventModelInstances:
    eventModelInstances.append(sentEnts)

#output1 = "<br>".join([str(t) for t in sortedTokensFreqs[:topK]])

#output2 = "<br>".join([str(t) for t in sortedToksTFDF[:topK]])
rs = "<tr>"
re = "</tr>"
outputs = "<td>"
outpute = "</td>"
wordsOutput = "<tr><td>Frequent Words (term Frequency)</td><td>Important Words (term Freq * Doc Freq)</td></tr>"
for i in range(topK):
    wordsOutput += rs + outputs + str(sortedTokensFreqs[i]) + outpute + outputs + str(topToksTuples[i]) + outpute + re

sents_ents = "<tr><td>Important Sentences</td><td>Named Entities</td></tr>"
for i in range(len(sortedImptSents)):
    sents_ents += rs + outputs + str(sortedImptSents[i]) + outpute + outputs + str(eventModelInstances[i]) + outpute + re
'''
lis = "<li>" 
lie = "</li>"
sentsOut = []

#for sents in allImptSents:
    #for s in sents:
for s in sortedImptSents:
    li = lis + str(s) + lie
    sentsOut.append( li )
output3 = " ".join(sentsOut)
output4 = "<br>".join([str(ents) for ents in eventModelInstances])
'''

#print "OK"

#print output1
#print "<br>============<br>"
#print output2
print wordsOutput
print "<br>============<br>"


#print output3
#print "<br>============<br>"
#print output4
print sents_ents
print "</body>"
print "</html>"
#except:
#    print sys.exc_info()