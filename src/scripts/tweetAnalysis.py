
from scripts.eventUtils import getTokens, getIntersection, getSorted
#categoriesLabels = ['Event','Resource','Community Building','Operations Update','Study Support','Q&A','Survey','Staff','Club']

categories = {}
with open('/Users/mmagdy/Downloads/Dr Sultan/categories.txt') as f:
	for l in f:
		p = l.strip().split(":")
		catCont = p[1].split(",")
		categories[p[0]] = catCont

#print categories
tweetsToks = []
with open('/Users/mmagdy/Downloads/Dr Sultan/tweets.txt') as tf:
	for l in tf:
		tweetToks = getTokens(l.strip())
		tweetsToks.append(tweetToks)
		
catTokens = dict.fromkeys(categories.keys(),[])
for k in catTokens:
	catText = ' '.join(categories[k])
	tks = getTokens(catText)
	catTokens[k] = tks

#print catTokens

evalResults = []

for k in tweetsToks:
	compRes = {}
	tset = set(k)
	for c in catTokens:
		cset = set(catTokens[c])
		intersect = getIntersection(cset, tset)
		compRes[c] = len(intersect) * 1.0 / len(cset)
	evalResults.append(compRes) 


evalResSorted = []
for e in evalResults:
	s = getSorted(e.items(), 1)
	st = str(s)
	evalResSorted.append(st)

with open('/Users/mmagdy/Downloads/Dr Sultan/results.txt', 'w') as rf:
	rf.write('\n'.join(evalResSorted))


'''
evalResults = {}
for k in students:
    evalResults[k] = {}
    ws = set(wikiTokens[k])
    for d in students[k]:
        s = students[k][d]
        r = getIntersection(ws, set(s))
        #print r
        evalResults[k][d] = r
        print d, k, len(r), len(s)#len(ws)
        #print len(r)* 1.0/len(ws)
        if len(s):
            print len(r)* 1.0/len(s)
        else:
            print 0
'''