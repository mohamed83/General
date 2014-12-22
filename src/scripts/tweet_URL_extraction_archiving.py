import re
import sys
from operator import itemgetter # to sort dictionaries by the values in (key, value) pairs
import requests
from bs4 import BeautifulSoup,Comment

#file containing tweets is passed as first argument to the script
#e.g python tweet_URL_extraction.py tweetsFile.txt
#where tweetsFile.txt is a text file containing one tweet per line.

tweets = open(sys.argv[1], "r")
shortURLsList = []
for tweet in tweets:
	
	regExp = "(?P<url>https?://[a-zA-Z0-9\./-]+)"
	url_li = re.findall(regExp, tweet)  # find all short urls in a single tweet
	while (len(url_li) > 0): 
		shortURLsList.append(url_li.pop())
		

expanded_url_dict = {}
# Once we collect short urls, next step is to expand each url to its original form

for url in shortURLsList:
	url = url.strip()
	try:
		#ori_url = requests.get(url, timeout=0.01).url
		ori_url = requests.get(url).url
		if ori_url != "":
			# add the expanded original urls to a python dictionary with their count
			if ori_url in expanded_url_dict:
				expanded_url_dict[ori_url] = expanded_url_dict[ori_url] + 1
			else:
				expanded_url_dict[ori_url] = 1
				
	except:  # ignore the exceptions/HTTP errors, and simply process the next tweet
		pass
		
		
# sort expanded_url_dict in descending order of the url count
sorted_list = sorted(expanded_url_dict.iteritems(), key=itemgetter(1), reverse=True)
print "sorted"

webpages = []
for expanded_url, count in sorted_list:
	print expanded_url + "," + str(count)

for url,_ in sorted_list: 
	try:
		response = requests.get(url)
		page = response.text || response.content
	except :
		print sys.exc_info()[0]
		pass
	soup = BeautifulSoup(page)
	title = ""
	text = ""
	if soup.title:
		title = soup.title

	comments = soup.findAll(text=lambda text:isinstance(text,Comment))
	[comment.extract() for comment in comments]
	text_nodes = self.soup.findAll(text=True)

	visible_text = filter(visible, text_nodes)
	text = ''.join(visible_text)
	text = title + " " + text
	webpages.append((url,text))
	

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head']:
        return False
    return True