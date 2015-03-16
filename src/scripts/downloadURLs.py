from eventUtils import getWebpageText
f = open('seedsURLs_z_543-noTweets.txt','r')
urls = f.readlines()
f.close()
urls = [u.strip() for u in urls]
texts = getWebpageText(urls)
i = 0
for p in texts:
    
    if p.has_key('text'):
        ftext = open("webpages/"+str(i) + ".txt", "w")
        ftext.write(p['text'].encode("utf-8"))
        ftext.close()
    i+=1
