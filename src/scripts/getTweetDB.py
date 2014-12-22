'''
Created on Oct 9, 2014

@author: Heritrix
'''
import pymysql

conn = pymysql.connect(host="spare05.dlib.vt.edu", user="mmagdy", passwd="pw4mmagdy", db="twitter",charset='utf8')
cursor = conn.cursor()

#f = open(sys.argv[1],"r")
query = "select id from twitter.archives"
print query
cursor.execute(query)
archives=[]
for row in cursor.fetchall():
    #print row[0]
    archives.append(row[0])

for arc in archives:
    query = "select * from twitter.z_" + str(arc)
    print query
    cursor.execute(query)
    f = open(str(arc) +".csv")
    for r in cursor.fetchall():
        print r
#print "tweets read from DB"