
import sys
#import pysolr
import sunburnt
import pymysql


conn = pymysql.connect(host="spare05.dlib.vt.edu", user="ctrnet", passwd="tweetctr!!", db="twapperkeeper_2",charset='utf8')
cursor = conn.cursor()

# create the connection to solr
solr_url = "http://jingluo.dlib.vt.edu:8080/solr/"
solr_instance = sunburnt.SolrInterface(solr_url)
#solr_instance = pysolr.Solr(solr_url)

# Processes the given directory for .warc files
def main(argv):
    #argv = ["","z_75","","Boston bombing","","Bombing"]
    #argv = ["","z_82","","Turkish car bombing","","Bombing"]
    #argv = ["","z_77","","Texas fertilizer explosion","","Accidents"]
    argv = ["","z_98","","Quebec train derailment","","Accidents"]
    archiveID = argv[1]
    #collection_id = argv[3]
    event = argv[3]
    event_type = argv[5]
    query = "select id,text,from_user, from_unixtime(time, '%Y-%m-%d') from twapperkeeper_2." + archiveID + " where iso_language_code like 'en'"
    print query
    cursor.execute(query)
    docs=[]
    #error = False
    indexed = []
    for row in cursor.fetchall():
        #print type(row[1])
        #print row[1]
        doc = {"id":row[0], "content":row[1], "title":row[2],"last_modified":row[3],"category":"tweets", "collection_id":archiveID, "event":event, "event_type":event_type}
        docs.append(doc)
        
        #try:
    solr_instance.add(docs)
        #print row[1]
        #solr_instance.add(doc)
    #indexed.append(1)
        #except Exception as inst:
        #    print "Error indexting file, with message" + str(inst)

    #if len(indexed):
    print "Storing and Indexing finished"
            
    try:
        solr_instance.commit()
    except:
        print "Could not Commit Changes to Solr, check the log files."
    else:
        print "Successfully committed changes"

if __name__ == "__main__":
    main(sys.argv[1:])
