import hashlib
from bs4 import BeautifulSoup,Comment
import sunburnt
import grequests



def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head']:
		return False
	return True

thresh = 1
solr_url = "http://jingluo.dlib.vt.edu:8080/solr/"
archiveID = "z_197"
event = "World_Cup"
event_type = "Community"
#solr_instance = solr.Solr(solr_url)

#Read Tweets from mysql DB
#-------------------------------
solr_instance = sunburnt.SolrInterface(solr_url)

urls = []
fs = open("origURLs.txt","r")
for line in fs:
	line = line.strip()
	p = line.split(",")
	urls.append(p[0])
fs.close()

#Retrieve Long URLs
#-------------------------
print len(urls)
webpages=[]
#try:
rs=[grequests.get(u,timeout=10) for u in urls]

re= grequests.map(rs)
#except:
#	print sys.exc_info()[0]

#for url,_ in sorted_list:
print len(re)
for r in re:
	'''
	try:
		r = requests.get(url,timeout=10,verify=False)
	except:
		print sys.exc_info()[0]
		continue
	
	page = r.content or r.text
	'''
	page = r.content
	url = r.url
	#with closing(requests.get(url,timeout=10, stream=True)) as r:
	#	page = r.text or r.content
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
	#text = title + " " + text
	webpages.append((url,title, text))
print "URLs downloaded"
print len(webpages)
#Index retrieved webpages into SOLR
#----------------------------------------
for url,title, webpage in webpages:
	
	html_id = hashlib.md5(url).hexdigest()
	doc = {"id":html_id, "content":webpage, "title":title, "collection_id":archiveID, "url":url, "event":event, "event_type":event_type}
	
	# attempt to add it to the index, make sure to commit later
	#try:
	solr_instance.add(doc)
	#except Exception as inst:
	#	print "Error indexting file, with message" + str(inst)

try:
	solr_instance.commit()
except:
	print "Could not Commit Changes to Solr, check the log files."
else:
	print "Successfully committed changes"