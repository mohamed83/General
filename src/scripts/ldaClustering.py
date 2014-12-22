'''
Created on Nov 2, 2014

@author: mmagdy
'''
#from readability.readability import Document
    
import utils
from operator import itemgetter

def convertTextFilesToSentFiles(fldr = '../input/Islip13Rain/'):
    
    
    for i in range(11):
        f = open(fldr+str(i+1)+".txt","r")
        fileText = f.read().decode('utf-8')
        csts = utils.getSentences(fileText)
        j = 0
        for s in csts:
            fi = open(str(i+1)+"-"+str(j)+".txt","w")
            fi.write(s.encode('utf-8'))
            fi.close()
            j+=1
    
def parseClusteringOutputFile(filename="../input/sentDump"):
    f = open(filename,"r")
    lines = []
    for line in f:
        lines.append(line)
    clustersInfo = []
    centroids=[]
    clusterMembers=[]
    clusterPointMembers = []
    points = []
    for l in lines:
        if l.startswith("VL-"):
            clustersInfo.append(l.strip())
            s = l.find("n=")+2
            end = l.find("c=")
            n = l[s:end]
            clusterMembers.append(int(n))
        if l.strip().startswith("1.0: /"):
            s = l.find("[")
            e = l.find("]")+1
            p = l[s:e]
            points.append(p)
    for ci in clustersInfo:
        st = ci.find("c=")+2
        end = ci.find("]")+1
        li = ci[st:end]
        centroids.append(li)
    
    i=0
    for cm in clusterMembers: 
        clusterPointMembers.append(points[i:i+cm])
        i = i+cm
        
    centroidsList= []
    for c in centroids:
        c = c[1:-1]
        p = c.split(',')
        centroidsList.append(p)
    clusterPointMemebersList = []
    for cpm in clusterPointMembers:
        cml = []
        for c in cpm: 
            c = c[1:-1]
            p = c.split(',')
            cml.append(p)
        clusterPointMemebersList.append(cml)
    
    #### Get K Closest sentences to the centroid of each cluster
    closestSentsToCentroids = []
    
    for i in range(len(centroidsList)):
        points = clusterPointMemebersList[i]
        sims = []
        for p in points:
            sim = getVectorsSimilarity(centroidsList[i], p)
            sims.append((sim,p))
        sortedSims_list = sorted(sims, key=itemgetter(0), reverse=True)
        closestSentsToCentroids.append(sortedSims_list[:3])
    
    for i in range(len(closestSentsToCentroids)):
        print ("centroid: %s \n Sentence: %s \n === \n")%( centroidsList[i], "\n".join([str(t) for t in closestSentsToCentroids[i]]))
    
    
def getVectorsSimilarity(v1,v2):
    cv1 = {}
    cv2= {}
    
    for e in v1:
        p = e.split(":")
        cv1[p[0].strip()] = float(p[1].strip())
    for e in v2:
        p = e.split(":")
        cv2[p[0].strip()] = float(p[1].strip())
    sim = 0
    for k in cv1.keys():
        if k in cv2:
            sim += cv1[k]* cv2[k] 
    return sim
    
if __name__ == "__main__":
    parseClusteringOutputFile("../input/sentDump")
