import mysql.connector

cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='test')

# Get  buffered cursor
curA = cnx.cursor(buffered=True)
curB = cnx.cursor(buffered=True)

# Query to get employees who joined in a period defined by two dates
query = ("SELECT MONTH,DAY, FAJR,SUNRISE,DUHR,ASR,MAGHREB,ISHAA FROM PrayerTimes "
  "WHERE MONTH >= '3' AND MONTH < '11'"

# UPDATE statement 3/9  --> 10/31
update_athan_time = ("UPDATE PrayerTimes SET FAJR = %s,SUNRISE= %s,DUHR= %s,ASR= %s,MAGHREB= %s, ISHAA= %s ")

curA.execute(query)

# Iterate through the result of curA
for (month,day fajr, sunrise, duhr, asr, maghreb, ishaa) in curA:
	if month >= 3:
		if day >= 9:
			ptimes = [fajr,sunrise,duhr,asr,maghreb,ishaa]
			for p in ptimes:
				h = p.split(":")
				p = int(h[0]) - 1 + ":" + h[1]
			curB.execute(update_athan_time, (fajr, sunrise, duhr, asr, maghreb, ishaa))

  # Commit the changes
cnx.commit()





cnx.close()