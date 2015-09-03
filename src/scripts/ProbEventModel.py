'''
Created on Apr 9, 2015

@author: mmagdy
'''

import eventUtils
import math,sys
import logging

logging.basicConfig(filename='/home/mmagdy/Dropbox/logging.log',level=logging.DEBUG)
log = logging.getLogger(__name__)

def getCollectionDocs(filename):
    f = open(filename)
    ls = f.readlines()
    f.close()
    ls = [l.strip() for l in ls]
    docsL = eventUtils.getWebpageText(ls)
    return docsL

def buildProbEventModel(docsList):
    t = ''
    docsTotalFreqs=[]
    docsEntities=[]
    docsEntitiesFreq = []
    entitiesProb = {}
    
    # Convert each doc to tokens, locations, dates lists and their corresponding frequency distributions
    # Also produces the total frequency for each document of each list (tokens, locations, and dates)
    for doc in docsList:
        
        if doc.has_key('text'):
            t = doc['text']
            if doc.has_key('title'):
                t =doc['title']+ " "+t
        if t:
            print 'Reading ' + t[:100]
            ents = eventUtils.getEntities(t)[0]
            docEnt = {}
            docEnt['LOCATION']={}
            if 'LOCATION' in ents:
                docEnt['LOCATION'] =  ents['LOCATION']
            docEnt['DATE']={}
            if 'DATE' in ents:
                docEnt['DATE'] = ents['DATE']
            toks = eventUtils.getTokens(t)
            docEnt['Topic'] = toks
            docsEntities.append(docEnt)
            
            docEntFreq = {}
            #docTotals = {}
            for k in docEnt:
                docEntFreq[k] = eventUtils.getFreq(docEnt[k])
                #totalFreq = sum([v for _,v in docEntFreq[k].items()])
                
                #docTotals[k] = totalFreq
            docsEntitiesFreq.append(docEntFreq)
            #docsTotalFreqs.append(docTotals)
    
    # Collection-level frequency for each entity(tokens, locations, dates)
    
    # Total Frequency of keywords, locations, and dates in all documents
    '''
    allDocsTotal = {}
    allDocsTotal['LOCATION'] = 0
    allDocsTotal['DATE']=0
    allDocsTotal['Topic'] = 0
    
    for docTotFreq in docsTotalFreqs:
        for k in docTotFreq:
            allDocsTotal[k]+= docTotFreq[k]
    '''
    
    #Calculating prob for each item in each entity lists (tokens, locations, and dates) as 
    # freq of item in all docs / total freq of all terms in that list
    entitiesProb['LOCATION']={}
    entitiesProb['DATE']={}
    entitiesProb['Topic']={}
    
    for docEntFreq in docsEntitiesFreq:
        for entity in docEntFreq:
            for val in docEntFreq[entity]:
                if val in entitiesProb[entity]:
                    entitiesProb[entity][val] += docEntFreq[entity][val]
                else:
                    entitiesProb[entity][val] = docEntFreq[entity][val]
    
    for ent in entitiesProb:
        allvalsFreq = sum([v for _,v in entitiesProb[ent].items()])
        for k in entitiesProb[ent]:
            #entitiesProb[ent][k] = (1.0 + (entitiesProb[ent][k] *1.0)) / (docsTotalFreqs[ent] + allDocsTotal[ent])
            
            entitiesProb[ent][k] = (1.0 + (entitiesProb[ent][k] *1.0)) / (len(entitiesProb[ent]) + allvalsFreq)
            
        
            
    return docsEntities, entitiesProb

def getMLEEventEntities(probEventModel,topK):
    mleEnts = {}
    for k in probEventModel:
        d = probEventModel[k]
        ds = eventUtils.getSorted(d.items(), 1)
        if topK:
            mleEnts[k] = ds[:topK]
        else:
            mleEnts[k] = ds
    return mleEnts

def getDocProb(docEnts, probEvtModel):
    docsProbs = []
    
    for docEnt in docEnts:
        docProb = {}
        for k in docEnt:
            #total = 1
            total = 0.0
            docProb[k]={}
            for e in docEnt[k]:
                p = probEvtModel[k][e.lower()]
                docProb[k][e.lower()] = p
                #total = total * p
                total = total + math.log(p) #p 
                
            docProb[k]['Total'] = total
        
    #finalDocProb = 1
        finalDocProb = 0.0
        for k in docProb:
            #finalDocProb = finalDocProb * docProb[k]['Total']
            finalDocProb = finalDocProb + docProb[k]['Total']
        docProb['Total'] = finalDocProb
        docsProbs.append(docProb)
    return docsProbs#finalDocProb

if __name__ == '__main__':
    #'Output-walterScottShooting.txt','Output-boatCapsized.txt','Output-garissa attack.txt'
    #collectionURLsFile = 'Output-germanwings_crash.txt'
    collectionURLsFile = sys.argv[1]
    topK = 10
    docsList = getCollectionDocs(collectionURLsFile)
    #log.info(len(docsList))
    docEnts, probEventModel = buildProbEventModel(docsList)
    eventUtils.saveObjUsingPickle(docEnts, collectionURLsFile.split(".")[0]+"_docEnts.p")
    eventUtils.saveObjUsingPickle(probEventModel, collectionURLsFile.split(".")[0]+"_probEventModel.p")
    #log.info(probEventModel)
    #print probEventModel
    docsProb = getDocProb(docEnts,probEventModel)
    eventUtils.saveObjUsingPickle(docsProb, collectionURLsFile.split(".")[0]+"_docsProb.p")
    print [d['Total'] for d in docsProb]
    #log.info(docsProb)
    mleEnts = getMLEEventEntities(probEventModel, 0)
    eventUtils.saveObjUsingPickle(mleEnts, collectionURLsFile.split(".")[0]+"_mleEnts.p")
    #log.info(mleEnts)
    for k in mleEnts:
        print k, mleEnts[k][:10]
    #print mleEnts
    #print probEventModel.getMLE_Entites()