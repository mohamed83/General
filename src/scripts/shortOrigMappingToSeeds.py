'''
Created on Dec 11, 2014

@author: mmagdy
'''
import random
def convertMappingToSeeds():
    fileName = 'short_origURLsMapping_z_474_en.txt'
    seedFileName = 'seeds_'+fileName.split("_")[-1]
    seedURLs = []
    with open(fileName,"r") as f:
        for l in f:
            l = l.strip()
            p = l.split(":--")
            origURL = p[0]
            seedURLs.append(origURL)
            #shortURLs = p[1].split(",")
            
    with open(seedFileName,"w") as fw:
        fw.write("\n".join(seedURLs))
 
def createRandomSeedFiles():
    #colls = ['459','460','474','475','477','478']
    colls = ['474_en']
    nb = 3
    for c in colls:
        urls ={}
        #for i in range(3):
        fn = 'seeds_'+c
        with open(fn+'.txt','r') as f:
            seeds = f.readlines()
        
        l = len(seeds)
        size = l/nb
        
        ind = [j for j in range(len(seeds))]
        random.shuffle(ind)
        
        for n in range(nb):
            pin = ind[n*size:(n+1)*size]
            urls[n] = [seeds[i] for i in pin]
        
        urls[nb-1].extend(seeds[nb*size:])
        
        for k in urls:
            with open(fn+'_'+str(k)+'.txt','w') as f:
                f.write(''.join(urls[k]))
        ''' This way of randomizing will produce uneven sets
        ind = [j for j in range(len(seeds))]
        random.shuffle(ind)
        ind = [j%3 for j in ind]
        
        for i,s in zip(ind,seeds):
            urls[i].append(s.strip())
        for k in urls:
            with open(fn+'_'+k+'.txt','r') as f:
                f.write('\n'.join(urls[k]))
        '''    
                
#convertMappingToSeeds()
createRandomSeedFiles()