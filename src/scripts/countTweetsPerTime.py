#!/usr/bin/python
import utils
import pymysql

'''
import sys
import re
from subprocess import call
from email.utils import parsedate
import time
import codecs
'''
#CONST_TABLE  = "z_" + sys.argv[1]
CONST_TABLE  = "z_403"
CONST_ADDITIONAL = 'no'

host='lancelot.dlib.vt.edu'
username='mmagdy'
password='pw4mmagdy'
dbase='twitter'

#def csv_unireader(f, encoding="utf-8"):
#    for row in csv.reader(codecs.iterencode(codecs.iterdecode(f, encoding), "utf-8")):
#        yield [e.decode("utf-8") for e in row]

#call("rm tweet_text.csv", shell=True)
#call("rm tweet_text_date.csv", shell=True)
#call("rm tweet_date.csv", shell=True)
#call("rm tweet_arff.csv", shell=True)

#file0 = open(CONST_TABLE + '/10_original.csv','w')
f1 = open(CONST_TABLE + '.txt','w')
#file5 = open(CONST_TABLE + '/15_lat_long.csv','w')
#f7 = open(CONST_TABLE + '/17_from_user.csv','w')

#if CONST_ADDITIONAL == 'yes':
#    file2 = open(CONST_TABLE + '/12_cleaned_text_date.csv','w')
#    file3 = open(CONST_TABLE + '/13_date.csv','w')
#    file4 = open(CONST_TABLE + '/14_arff.csv','w')
#    file6 = open(CONST_TABLE + '/16_state.csv','w')

# connect
#conn = pymysql.connect(host="spare05.dlib.vt.edu", user="ctrnet", passwd="tweetctr!!", db="twapperkeeper_2")
conn = pymysql.connect(host=host, user=username, passwd=password, db=dbase)
cursor = conn.cursor()

# execute SQL select statement
# water main break 7
#cursor.execute("select id, text, created_at, time from z_1 where text not like 'RT%'")
# with date constraint

# extract organization
#cursor.execute("SELECT text, time FROM twapperkeeper_2." + CONST_TABLE_DB + " WHERE from_unixtime(time, '%Y-%m-%d') >= DATE('2013-04-01') AND from_unixtime(time, '%Y-%m-%d') <= DATE('2013-4-30') AND text not like 'RT%'")
month = "08"
#cursor.execute("SELECT text, time FROM twapperkeeper_2." + CONST_TABLE_DB + " WHERE from_unixtime(time, '%Y-%m-%d') >= DATE('2014-" + month+ "-01') AND from_unixtime(time, '%Y-%m-%d') <= DATE('2014-"+ month+"-31')")

#query = "SELECT time FROM twapperkeeper_2." + CONST_TABLE_DB + " WHERE from_unixtime(time, '%Y-%m') = '2014-" + month+"'"



#query = "select count(*), from_unixtime(time, '%Y-%m') as fullDate from twitter." + CONST_TABLE +" where text not like 'RT%' "+ " group by fullDate"

query = "select from_user as user_name, from_unixtime(time, '%Y-%m') as fullDate, count(*) from twitter." + CONST_TABLE +" where text not like 'RT%' "+ " group by user_name, fullDate"

#print query
cursor.execute(query)

# Condition: Has lat and long, Until < 2014-3-1
##cursor.execute("SELECT id, text, created_at, time, geo_coordinates_0, geo_coordinates_1, from_user FROM twitter." + CONST_TABLE_DB + " WHERE geo_coordinates_0 <> 0 AND geo_coordinates_1 <> 0 AND time <= 1393632000 ")

##cursor.execute("SELECT id, text, created_at, time, geo_coordinates_0, geo_coordinates_1 FROM twitter.CONST_TABLE WHERE geo_coordinates_0 <> 0 AND geo_coordinates_1 <> 0 AND text not like '%Airport Blvd%' AND text not like '%Rio de Janeiro%' AND text not like '%#Orleans?!?%' AND text not like '%Episcopal Road area of Berlin%' ")

# hurricane 51
##cursor.execute("select id, text, created_at, time from z_51 where text not like 'RT%' and text like '%isaac%'")

# get the number of rows in the resultset
#numrows = int(cursor.rowcount)

#print "Total no of Tweets in Month %s is %s" % (month, numrows)
for row in cursor.fetchall():
	f1.write("%s,%s,%s\n" % (row[0],row[1],row[2]))
	#f1.write("%s,%s,%s\n" % (row[1],row[0]))
'''    
num = 1
for numrows in cursor.fetchall() :

    # 00. Original
    #file0.write('%s\n' % numrows[1])
    #orig = numrows[1].replace('\n', '')
    #file0.write('%s\n' % orig)

    # remove url
    text = re.sub("(?P<url>https?://[^\s]+)", "", numrows[0])
    #text = re.sub("(?P<url>http://[^\s]+)", "", numrows[1])
    # remove #, @
    text = text.replace('#', '')
    #text = text.replace('@', '')
    text = text.replace('|', '')
    text = text.replace('!', '')
    text = text.replace('?', '')
    text = text.replace('/', '')
    text = text.replace(')', '')
    text = text.replace('(', '')
    text = text.replace('=', '')
    text = text.replace('_', '')
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    text = text.replace('\newline', '')
    text = text.replace(':', '')
    text = text.replace(',', '')
    text = text.replace('.', '')
    text = text.replace('"', '')
    text = text.replace('  ', ' ')
    # For remove "water main break" case insensitive
    #wmb = re.compile(re.escape('water main break'), re.IGNORECASE)
    #text = wmb.sub('', text)

    # Cleaned Text
    f1.write('%s\n' % text)
    
    # Lat, long
#    lat = numrows[4]
#    long = numrows[5]
#    file5.write('%s, %s\n' % (lat, long))

    # from_user
#    f7.write('%s, %s\n' % (numrows[6], text ))

#    if CONST_ADDITIONAL == 'yes':
#        id = numrows[0]
#        timeString = numrows[3]
#        #a = parsedate('Fri, 15 May 2009 17:58:28 +0000')
#        create_date = parsedate( numrows[2] )
#        year = str(create_date[0])
#        month = str(create_date[1])
#        day = str(create_date[2])
#        
#        file2.write('%s, %s, %s, %s, %s, %s, %s, %s\n' % ( id, text, timeString, create_date[0], create_date[1], create_date[2], create_date[3], create_date[4]))
#        file3.write('%s, %s%s%s\n' % (id, year.zfill(4), month.zfill(2), day.zfill(2)))
#        file4.write('%s, "%s"\n' % (id, text))
#        
#        # State using reverse geocoder
#        geolocator = GoogleV3()
#        address, (latitude, longitude) = geolocator.reverse('%s, %s' % (lat, long), exactly_one=True)
#        state = '';
#        if address.endswith('USA'):
#            address_element = re.split(r',\s*', address)
#            state = address_element[2][0:2]
#        file6.write('%s\n' % state)

    num = num + 1
    #time.sleep(0.5)

print "Total number of tweets: " + str(num)
'''
#file0.close()
f1.close()
#file5.close()
#f7.close()
#if CONST_ADDITIONAL == 'yes':
#    file2.close()
#    file3.close()
#    file4.close()
#    file6.close()