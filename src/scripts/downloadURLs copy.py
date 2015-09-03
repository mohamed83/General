import eventUtils
f = open('seedURLs_z_543-noTweets.txt','r')
urls = f.readlines()
f.close()
urls = [u.strip() for u in urls]
