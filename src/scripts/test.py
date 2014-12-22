def getDomain(url):
	#stat = {}
	#url = ""
	domain = ""
	#for elem in data:
	#url = elem[0]
	#url = elem
	#ind = url.find("http")
	ind = url.find("//")
	if ind != -1 :
	#url2 = url[ind:]
	#ind = url2.find("//")
		domain = url[ind+2:]
		ind = domain.find("/")
		domain = domain[:ind]
	return domain

f = open("origURLs.txt")
urls = []
for line in f:
	line = line.strip()
	p = line.split(",")
	
	url = p[0]
	ind = url.find("twitter.com")
	if ind == -1:
		urls.append(url)
		
f.close()

f = open("origURLsCleaned.txt","w")
s = "\n".join(urls)
f.write(s)
f.close()

f = open("origURLsCleaned.txt")
urls = []
for line in f:
	line = line.strip()
	urls.append(line)
		
f.close()

import hapy
import time

def wait_for(h, job_name, func_name):
	print 'waiting for', func_name
	info = h.get_job_info(job_name)
	while func_name not in info['job']['availableActions']['value']:
		time.sleep(1)
		info = h.get_job_info(job_name)


h = hapy.Hapy('https://localhost:8443', username='admin', password='admin')
name = "9/11_Anniversary"
h.create_job(name)
#h.submit_configuration(name, config)
h.submit_configuration(name)
wait_for(h, name, 'build')
h.build_job(name)
wait_for(h, name, 'launch')
h.launch_job(name)
wait_for(h, name, 'unpause')
h.unpause_job(name)
	