from sunburnt import SolrInterface
import sys

si = SolrInterface("http://nick.dlib.vt.edu:8080/solr")

eventQuery = sys.argv[1]

response = si.query( event=eventQuery).execute()
tot = response.result.numFound
response = si.query(event=eventQuery).field_limit(["content"]).paginate(0,tot).execute()
docs = {}
print response.result.numFound
i = 1
for res in response:
    f = open(str(i) + ".txt","w")
    f.write(res['content'].encode("utf-8"))
    f.close()
    i+=1
si.commit()
