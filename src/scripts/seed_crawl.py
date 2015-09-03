import hapy
import subprocess
import sys
import time

# @param h
# @param job_name
def wait_job_end(h, job_name):
	print 'waiting for job to finish'
	key = 'Finished: FINISHED'
	check = ''
	while key not in check:
		info = h.get_job_info(job_name)
		check = info['job']['statusDescription']
		time.sleep(1)
			
# @param h
# @param job_name
# @param func_name
# @author function from Hapy Heritrix Python wrapper README
def wait_for(h, job_name, func_name):
	print 'waiting for', func_name
	info = h.get_job_info(job_name)
	while func_name not in info['job']['availableActions']['value']:
		time.sleep(1)
		info = h.get_job_info(job_name)

# This function crawls the seed urls
def seed_crawl():
	crawlerFile = 'crawler-beans.cxml'                              # crawler_beans
	t = time.gmtime()
	job_name = "%s%s%s%s%s%s" %(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
	seedsFile = '$HERITRIX_HOME/jobs/%s/seeds.txt' %(job_name)      # seed file
	job_dir = '$HERITRIX_HOME/jobs/%s/2*/warcs/*' %(job_name)       # warc files
	warc_dir = '/home/cloudera/ideal_auto/warcs'                    # warc repo
	mv_com = 'mv %s %s' %(job_dir, warc_dir)                        # move files
	heritrix_host = 'https://preston.dlib.vt.edu:8443/'             # need to have heritrix running here
	user = 'admin'
	pw = 'ideal2014'
	mv_seed = 'mv %s %s' %('seeds.txt', seedsFile)

	'''
	file = open(seedsFile, 'r+')
	seed_list = file.read()
	file.close()
	'''

	file = open(crawlerFile, 'r+')
	line_string = ''
	cxml_string = ''

	'''	
	while '# URLS HERE' not in line_string:
		line_string = file.readline()
		cxml_string = cxml_string + line_string
	line_string = file.readline()
	cxml_string = cxml_string + seed_list
	'''
	
	line_string = file.read()
	cxml_string = cxml_string + line_string
	file.close()

	h = hapy.Hapy(heritrix_host, username=user, password=pw)
	h.create_job(job_name)

	time.sleep(1)
	subprocess.call([mv_seed], shell=True)

	h.submit_configuration(job_name, cxml_string)
	wait_for(h, job_name, 'build')
	h.build_job(job_name)
	wait_for(h, job_name, 'launch')
	h.launch_job(job_name)
	wait_for(h, job_name, 'unpause')
	h.unpause_job(job_name)
	
	wait_job_end(h, job_name)
	
	print 'crawl finished: moving warc files'
	
	subprocess.call([mv_com], shell=True)
