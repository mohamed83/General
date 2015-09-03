import json

f = open('twitter_cache_1_July_2014_through_27_Feb_2015.json','r')
keys = []
for l in f:
	s = json.loads(l.strip())
	
	#keys.extend(s.keys())
	keys.append(len(s))
#keysSet = set(keys)
#print keysSet
print keys
f.close()

'''
['category', 'content', 'fb_comments_count', 'fb_link', 'title', 'text', 'author', 'fb_id', 'longitude', 'twitter_id', 'fb_type', 'source', 'published_at', 'fb_likes_count', 'image_url', 'cached_on', 'latitude', 'link', 'twitter_retweet_count', 'geo', 'id']
'''