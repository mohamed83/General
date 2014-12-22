import os

from sunburnt import SolrInterface

si = SolrInterface("http://jingluo.dlib.vt.edu:8080/solr")

# This is where you put the event name 

# eventQuery = "Typhoon Haiyan"
eventQuery = "Connecticut School Shooting"

# This is where you put the downloaded files
root = 'D:\Test\EventCollections\SmallCollections'

#response = si.query(event="Connecticut").query(event="School").query(event="shooting").execute()
response = si.query(text="west africa").execute()

#response = si.query(event=eventQuery).execute()

tot = response.result.numFound
print tot
#response = si.query(event=eventQuery).field_limit(["content"]).paginate(0,tot).execute()

response = si.query(event=eventQuery).paginate(0,tot).execute()

docs = {}

print response.result.numFound

i = 1

directory = root + "\\" + eventQuery

if not os.path.exists(directory):
    os.makedirs(directory)

for res in response:
    f = open(directory + "\\" + str(i) + ".txt","w")

    content = res['content'][0]

    f.write(content.encode("utf-8"))

    f.close()

    i+=1