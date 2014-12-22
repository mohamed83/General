import sys
import sunburnt
#import solr



solr_url = "http://jingluo.dlib.vt.edu:8080/solr/"
#solr_instance = solr.Solr(solr_url)
solr_instance = sunburnt.SolrInterface(solr_url)

f = open("vts_news.csv")
for line in f:
	line = line.strip()
	parts = line.split(",")
	
	id = parts[0]
	title = parts[1]
	content = parts[2]
	url = parts[3]
	event_type="Community"
	event="Blacksburg_Events"
	popularity=parts[4] #views === popularity
	last_modified=parts[5]
	
	doc = {"id":id, "content":content, "title":title, "url":url, "event":event,"event_type":event_type,"popularity":popularity,"last_modified":last_modified }    
    # attempt to add it to the index, make sure to commit later
	i = 0
	e = 0
	try:
		solr_instance.add(doc)
		i+=1
	except Exception as inst:
		print "Error indexting file, with message" + str(inst)
		e+=1
try:
    solr_instance.commit()
except:
    print "Could not Commit Changes to Solr, check the log files."
else:
    print "Successfully committed changes"

print "Success:" +str(i)
print "Error:" + str(e)