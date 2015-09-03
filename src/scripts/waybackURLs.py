host = 'http://localhost:8080/wayback/*/'

urls = []
seedsFile = 'seeds.txt'

f = open(seedsFile)
urls = f.readlines()
f.close()

#waybackURLs = []
htmlURLs = []
for u in urls:
	wu = host + u
	#waybackURLs.append(wu)
	ah = "<a href='" + wu + "' > u </a> <br>"
	htmlURLs.append(ah)
	
htmlString = "<html><head><title>Wayback URLa</title></head><body>"+  "".join(htmlURLs)+"</body></html>"

 
fw = open("waybackURLs.txt","w")
fw.write(htmlString)
fw.close()