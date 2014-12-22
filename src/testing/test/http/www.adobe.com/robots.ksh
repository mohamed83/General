#
# This file is used to allow crawlers to index our site. 
#
# List of all web robots: http://www.robotstxt.org/wc/active/html/index.html
#
# Check robots.txt at:
# http://www.searchengineworld.com/cgi-bin/robotcheck.cgi
#

# Details about Googlebot available at: http://www.google.com/bot.html
# The Google search engine can see everything
User-agent: Googlebot 
Disallow: /licensing/distribution/strategies/
Disallow: /events/ciocouncil/

# All other robots will be restricted from accessing the Google-specific index pages
User-agent: *
Disallow: /google_indexing/
Disallow: /licensing/distribution/strategies/
Disallow: /events/ciocouncil/

Sitemap: http://www.adobe.com/sitemap.xml