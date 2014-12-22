import sys
import requests
import hashlib
from bs4 import BeautifulSoup,Comment

f = open(sys.argv[1],"r")
webpages=[]
for line in f:
	line = line.strip()
	parts = line.split(",")
	url = parts[0] 
	try:
		response = requests.get(url)
		page = response.text or response.content
	except :
		print sys.exc_info()[0]
		pass
	soup = BeautifulSoup(page)
	title = ""
	text = ""
	if soup.title:
		if soup.title.string:
			title = soup.title.string

	comments = soup.findAll(text=lambda text:isinstance(text,Comment))
	[comment.extract() for comment in comments]
	text_nodes = self.soup.findAll(text=True)

	visible_text = filter(visible, text_nodes)
	text = ''.join(visible_text)
	#text = title + " " + text
	webpages.append((url,title, text))
i = 1
for url,title, webpage in webpages:
	f = open(str(i) + ".txt","w")
    f.write(webpage.encode("utf-8"))
    f.close()
    i+=1
    
    event = "Ebola disease outbreak"
    event_type = "Disease Outbreak"
    
    html_id = hashlib.md5(url).hexdigest()
	
	# build the doc to index into solr
	# the fields here are the same as if an xml file were being used
	# so id is similar to an <id> tag and <content> as well, etc...
	doc = {"id":html_id, "content":webpage, "title":title, "collection_id":collection_id, "url":url, "event":event, "event_type":event_type}
	
	# attempt to add it to the index, make sure to commit later
	try:
		solr_instance.add(doc)
	except Exception as inst:
		print "Error indexting file, with message" + str(inst)

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head']:
        return False
    return True