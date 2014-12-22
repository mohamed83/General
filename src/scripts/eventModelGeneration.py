'''
Created on Oct 10, 2014

@author: dlrl
'''
import utils

    

def writeToFileSystem(data,filename,let):
    
    f = open(filename,"w")
    for s in data:
        
        if type(s) == type('str'):
            l = s + "\n"
        elif type(s) == type(u'unicode'):
            l = s + "\n"
        else:
            l = str(s) +"\n"
            
        f.write(l.encode('utf-8'))
        print let+": "+l.encode('utf-8')
    f.close()


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

'''
def getTokensTFDF(texts):
    tokensTF = []
    allTokens = []
    for t in texts:
        toks = utils.getTokens(t)
        toksFreqs = utils.getFreq(toks)
        allTokens.extend(toksFreqs.keys())
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
        
    return tokensTFDF
'''



if __name__ == "__main__":
    webpagesURLs = utils.readFileLines("../input/seedURLs.txt")
    #webpageURLs = ["http://www.accuweather.com/en/weather-news/tropical-storm-vongfong-slams/35196345","http://www.ctvnews.ca/world/dozens-injured-as-typhoon-vongfong-batters-southwestern-japan-1.2050625","http://www.cbc.ca/news/world/typhoon-vongfong-batters-japan-injures-28-1.2796005"]
    
    webpagesText = utils.getWebpageText(webpagesURLs)
    
    texts = [t['text'] for t in webpagesText if t.has_key('text') and len(t['text'])>0]
    
    #Get All Sentences
    #sents = utils.getSentences(texts)
    #writeToFileSystem(sents, "../output/sentences.txt","S")
    #print "============================="
    
    #Get All Tokens
    #tokens = utils.getTokens(sents)
    #writeToFileSystem(tokens, "../output/tokens.txt","T")
    
    #Get Frequent Tokens
    #f = utils.getFreq(tokens)
    #tokensFreqs = f.items()
    #sortedTokensFreqs = utils.getSorted(tokensFreqs,1)
    #writeToFileSystem(sortedTokensFreqs, "../output/tokensFreqs.txt","FT")
    
    print len(texts)
    toksTFDF,allSents = getTokensTFDF(texts)
    sortedToksTFDF = sorted(toksTFDF.items(), key=lambda x: x[1][0]*x[1][1], reverse=True)
    writeToFileSystem(sortedToksTFDF, '../output/toksTFDF_NY.txt',"TFDF")
    
    topToksTuples = sortedToksTFDF[:10]
    topToks = [k for k,_ in topToksTuples]
    
    allImptSents = []
    eventModelInstances = []
    
    for sents in allSents:
        impSents =[]
        #print len(sents)
        for sent in sents:
            sentToks = utils.getTokens(sent)
            intersect = utils.getIntersection(topToks, sentToks)
            
            if len(intersect) > 1:
            #if not utils.isListsDisjoint(topToks, sentToks):
                impSents.append(sent)
                evtModelInstance = {}
                sentEnts = utils.getEntities(sent)[0]
                evtModelInstance["Topic"] = list(intersect)
                for ent in sentEnts:
                    evtModelInstance[ent] = sentEnts[ent]
                eventModelInstances.append(evtModelInstance)
        #print len(impSents)
        allImptSents.append(impSents)
    
    for impSents in allImptSents:
        print "\n".join(impSents)
        print "=================="
        
    # Get Entities
    #sentEntities = []
    #for impSents in allImptSents:
    #    sentEnts = utils.getEntities(impSents)
    #    sentEntities.append(sentEnts)
        
    #for se in sentEntities:
    #    print "\n".join([str(s) for s in se])
    #    print "============"
    
    #Print Entities
    print "\n".join([str(emi) for emi in eventModelInstances])
    print "============"
    
    