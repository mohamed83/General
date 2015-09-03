import eventUtils,sys

def getLongURLsSourcesMapping(longURLs):
	#domains = [(l,eventUtils.getDomain(l) for l in longURLs]
	urlsDomsMapping = {}
	for url in longURLs:
		urlDom = eventUtils.getDomain(url)
		if urlDom in urlsDomsMapping:
			urlsDomsMapping[urlDom].append(url)
		else:
			urlsDomsMapping[urlDom]= [url]
	return urlsDomsMapping
	
def filterURLsByKeyword(keyword,urlsDomsMapping):
	filteredurlsDomsMap = {}
	for k in urlsDomsMapping:
		if keyword in k.lower():
			continue
		else:
			filteredurlsDomsMap[k.lower()] = urlsDomsMapping[k]
	return filteredurlsDomsMap
	
def rankLongURLsBySources(filteredURLsSourcesMapping):
	mappingList = filteredURLsSourcesMapping.items()
	rankedSourcesList = sorted(mappingList, key=lambda x: len(x[1]), reverse=True)
	rankedURLsList = []
	for rs,urlList in rankedSourcesList:
		#rankedURLsList.extend(filteredURLsSourcesMapping[rs])
		rankedURLsList.extend(urlList)
	return rankedURLsList

if __name__ == '__main__':
	longURLFileName = sys.argv[1]
	#sourcesFileName = ''
	keyword = 'twitter'
	longURLs = eventUtils.readFileLines(longURLFileName)
	longURLsSourcesMapping = getLongURLsSourcesMapping(longURLs)
	filteredURLsSourcesMapping = filterURLsByKeyword(keyword.lower(), longURLsSourcesMapping)
	#sources = eventUtils.readFileLines(sourcesFileName)
	rankedURLs = rankLongURLsBySources(filteredURLsSourcesMapping)
	eventUtils.saveListToFile(rankedURLs,longURLFileName.split('.')[0]+'-Ranked.txt')