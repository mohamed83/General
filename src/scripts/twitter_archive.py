# Script that will automate crawling of seed urls from ytk db
#
# Nikhil Plassmann (nikhilgp@vt.edu)

import seed_crawl
import url_producer 

def main():
	url_producer.produce_url()
	seed_crawl.seed_crawl()

if __name__ == "__main__":
	main()
