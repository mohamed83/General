'''
Created on Sep 19, 2014

@author: dlrl
'''
#import sys
import pymysql
#from sunburnt import SolrInterface
'''
conn = pymysql.connect(host="spare05.dlib.vt.edu", user="ctrnet", passwd="tweetctr!!", db="twapperkeeper_2",charset='utf8')
cursor = conn.cursor()

#f = open(sys.argv[1],"r")
query = "select id,keyword,count from twapperkeeper_2.archives"
cursor.execute(query)
tweetArchives=[]
for row in cursor.fetchall():
    tweetArchives.append(row)
    print row
conn.close()
'''


#si = SolrInterface("http://jingluo.dlib.vt.edu:8080/solr")

webArchives=[]
'''
query = si.query().facet_by("event_type").paginate(rows=0)
results = query.execute().facet_counts.facet_fields
event_typesCounts = results['event_type']
eventTypes = []
for etc in event_typesCounts:
    eventTypes.append(etc[0])
    
query = si.query().facet_by("event").paginate(rows=0)
results = query.execute().facet_counts.facet_fields
eventCounts = results['event']
events = []
for et in eventCounts:
    events.append(et[0])
response =[]
for res in response:
    #arc =(res['collection_id'],res['collection_id'],res['collection_id'],res['collection_id'],res['collection_id'],res['collection_id'],res['collection_id'])
    arc =(res['event'],res['event_type'])
    webArchives.append(arc)

#tot = response.result.numFound
'''
#response = si.query().execute()
#tot = response.result.numFound
#print tot

#response = si.query().paginate(0,tot).execute()
'''
query = si.query().facet_by("event")
f = query.execute().facet_counts
results = f.facet_fields
eventCounts = results['event']
#events = []
#for et in eventCounts:
#    events.append(et[0])
i=0
f = open("webArchives.txt","w")

for res in eventCounts:
    #arc =(i,res['event'],'Web',res['event_type'],res['collection_id'],'',0)
    #arc =(res['event'],res['event_type'])
    #webArchives.append(arc)
    f.write(str(res) + "\n")
    i+=1
'''

#tweetArchives=[]

f = open("webArchives.txt","r")
for line in f:
    #line = line[1:-2]
    line = line.strip()
    parts = line.split(",")
    #archiveId,keyword,count,event,category = line.split(",")
    parts = [p.strip() for p in parts]
    webArchives.append(parts)

conn = pymysql.connect(host="nick.dlib.vt.edu", user="mohamed", passwd="moha1983mysql", db="ideal_pages",charset='utf8')
cursor = conn.cursor()

#f = open(sys.argv[1],"r")
i = 268
for arc in webArchives:
    #2379,'youngstown shooting',1724,6
    query = "insert into Events(id,event,archiveType,category,archiveID,keywords,count) values (" + str(i) + ","+arc[1]+","+"'Web',"+arc[3]+"," +arc[0]+ ","+arc[1] +","+arc[2]+")"
    print query
    cursor.execute(query)
    i=i+1
    #print row
conn.commit()
conn.close()

