'''
Created on Oct 5, 2014

@author: dlrl
'''
#shortURLs = 192000

no_files = 10


urls = []
fr = open("shortURLs.txt")
for line in fr:
    #line = line.strip()
    p = line.split(",")
    url = p[0]
    while url.endswith("."):
        url = url[:-1]
    urls.append(url)
    
shortURLs_file = len(urls)/no_files
for i in range(10):
    f = open(str(i)+".txt", "w")
    
    u = urls[i*shortURLs_file:(i+1)*shortURLs_file]
    s = "\n".join(u)
    f.write(s)
    #for su in u:
    #    f.write(su+"\n")
    f.close()

fr.close()