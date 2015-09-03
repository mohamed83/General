'''
Created on Aug 29, 2015

@author: mmagdy
'''
import eventUtils
from dateutil.parser import *
from datetime import datetime
from _collections import defaultdict
from geopy.geocoders import Nominatim
import sys


def parseLoc(locTxt):
    addr=""
    loc = geolocator.geocode(locTxt,language='en')
    if loc:
        addr = loc.address
    return addr

def normalizeLocs(locsDic):
    parsedLocs = defaultdict(int)
    for k,v in locsDic.iteritems():
        try:
            parsedLoc = parseLoc(k)
            if parsedLoc:
                print "parsed: ", k, "to: ", parsedLoc
                parsedLocs[parsedLoc] += v
            else:
                print "No address returned for: ", k
        except:
            print k, " ", sys.exc_info()
    return parsedLocs

def normalizeDates(datesDic):
    #sortedFreqLocs = eventUtils.getSorted(freqLocs.iteritems(),1)
    #sortedFreqDates = eventUtils.getSorted(freqDates.iteritems(),1)
    #d = datetime.now()
    DEFAULT_DATE1 = datetime(1000,1,1)
    defaultDate2 = datetime(1100,2,2)
    parsedDates = defaultdict(int)
    #for k,v in freqLocs.iteritems():#sortedFreqLocs:
        #print k,",",v
    #print "--------------------------------"
    for k,v in datesDic.iteritems():#sortedFreqDates:
        #print k, ",", v
        try:
            parsedDate = parse(k,default=DEFAULT_DATE1)
            parsedDate2 = parse(k,default=defaultDate2)
            if parsedDate == parsedDate2:
            #print parsedDate
                print "parsed: ", k, ",", v
                parsedDates[parsedDate]+=v
            else:
                print "Didn't parse in complete"
        except ValueError as e:
            print e
            #pass
    return parsedDates


def extractDatesLocs(urls):
    webpagesTxt = eventUtils.getWebpageText_NoURLs(urls)
    txts = [webpageTxt['text'] for webpageTxt in webpagesTxt if 'text' in webpageTxt]
    webpageEnts = eventUtils.getEntities(txts)
    #webpageEnts = eventUtils.getEntities(webpageTxt[0]['text'])
    #print webpageEnts[0]['LOCATION']
    #print webpageEnts[0]['DATE']
    
    locs = []
    dates = []
    
    for wbE in webpageEnts:
        #print wbE['LOCATION']
        #print wbE['DATE']
        #print '-----------------------'
        if 'LOCATION' in wbE:
            locs.extend(wbE['LOCATION'])
        if 'DATE' in wbE:
            dates.extend(wbE['DATE'])
    
    freqLocs = eventUtils.getFreq(locs)
    freqDates = eventUtils.getFreq(dates)
   
    '''
    freqDates_norm = normalizeDates(freqDates)
    sortedDates = eventUtils.getSorted(freqDates_norm.iteritems(),1)
    print sortedDates
    print "Most Frequent Date (i.e. most probably event's date) is: ", sortedDates[0]
    print '________________________________'
    #print freqDates_norm
    '''
    freqLocs_norm = normalizeLocs(freqLocs)
    sortedLocs = eventUtils.getSorted(freqLocs_norm.iteritems(),1)
    print sortedLocs
    print "Most Frequent Location (i.e. most probably event's location) is: ", sortedLocs[0]
    #print freqLocs_norm
    return

if __name__ == "__main__":
    geolocator = Nominatim()
    '''
    http://www.reuters.com/article/2015/03/24/us-france-crash-airbus-lufthansa-idUSKBN0MK0ZP20150324
    http://www.independent.co.uk/news/world/europe/germanwings-crash-shocked-passengers-stared-silently-at-the-empty-arrivals-gate-10131339.html
    http://www.telegraph.co.uk/news/worldnews/europe/france/11493269/Germanwings-crash-Radio-silence-then-a-plunge-to-certain-death-in-the-Alps.html
    http://www.nbcnews.com/storyline/german-plane-crash/what-might-have-happened-plane-alps-crash-n329101
    http://www.cbsnews.com/news/germanwings-flight-9525-the-unusual-nature-of-the-crash/
    http://www.euronews.com/2015/03/24/airbus-crashes-in-southern-france-with-142-passengers-on-board-authorities/
    http://www.wsj.com/articles/germanwings-a320-plane-crashes-in-southern-france-1427195298
    http://www.marketwatch.com/story/germanwings-crash-2-babies-schoolkids-on-board-2015-03-24
    http://www.buzzfeed.com/stephaniemcneal/victims-of-deadly-germanwings-crash-include-16-german-high-s
    http://www.zerohedge.com/news/2015-03-24/first-images-germanwings-crash-debris-emerge-white-house-says-no-indication-terroris
    '''
    '''
    http://www.ibtimes.com/tunisia-hotel-attack-prime-minister-vows-close-80-mosques-spreading-venom-country-1986673
http://pamelageller.com/2015/06/tunisia-to-close-80-mosques-for-inciting-violence-after-hotel-attack-cbldf.html/
http://www.buzzfeed.com/maryanngeorgantopoulos/gunmen-reportedly-killed-at-least-7-tourists-at-tunisia-hote
http://www.euronews.com/2015/06/27/tunisia-to-beef-up-security-measures-in-wake-of-deadly-hotel-attack/
http://english.alarabiya.net/en/News/africa/2015/06/26/At-least-seven-killed-in-attack-on-two-Tunisian-beach-hotels.html
http://www.jpost.com/Breaking-News/Tunisia-government-says-to-close-80-mosques-for-inciting-violence-after-hotel-attack-407290
http://www.dailystar.co.uk/news/latest-news/450352/Tunisia-tourist-attack-Gunshots-fire-hotel-Sousse-resort
https://www.pressandjournal.co.uk/fp/news/world/621531/tunisia-terror-attack-tourist-hotel-targeted/
http://www.jihadwatch.org/2015/06/tunisia-plans-to-close-80-mosques-for-inciting-violence-after-hotel-jihad-attack
http://www.thetruthaboutguns.com/2015/06/robert-farago/breaking-terrorist-gunmen-kill-dozens-in-tunisia-hotel-attack/
    '''
    urlsT ='''
    http://www.breitbart.com/big-government/2015/06/26/supreme-court-says-same-sex-marriage-is-a-constitutional-right/
http://www.wsj.com/articles/publics-shift-on-same-sex-marriage-was-swift-broad-1435359461
http://thehill.com/video/in-the-news/246257-se-cupp-gets-emotional-over-same-sex-marriage-decision
http://www.tmz.com/2015/06/26/gay-marriage-supreme-court-same-sex-legal-constitutional-right/
http://www.poynter.org/news/mediawire/353539/front-pages-from-all-50-states-on-the-same-sex-marriage-ruling/
http://www.chicagotribune.com/news/opinion/zorn/ct-supreme-court-john-roberts-gay-marriage--perspec-0628-20150626-column.html
http://www.buzzfeed.com/kyleblaine/heres-every-2016-gop-candidates-response-to-the-same-sex-mar
http://news.sbts.edu/2015/06/26/mohler-responds-supreme-courts-same-sex-marriage-decision/
http://www.vanityfair.com/hollywood/2015/06/watch-stephen-colbert-shut-down-same-sex-marriage-haters
http://www.theonion.com/article/supreme-court-on-gay-marriage-sure-who-cares-31812
    '''
    urls = urlsT.split()
    #urls = ['http://theconservativetreehouse.com/2015/06/17/breaking-reports-mass-shooting-in-n-charleston-south-carolina/','http://pix11.com/2015/06/17/police-respond-to-shooting-at-charleston-south-carolina-church/','http://www.jpost.com/Breaking-News/Shooting-erupts-at-church-in-Charleston-South-Carolina-406415','http://fox2now.com/2015/06/17/shooting-reported-at-emanuel-african-methodist-episcopal-church-in-downtown-charleston/','http://fox59.com/2015/06/17/multiple-people-injured-following-shooting-at-church-in-charleston/','http://www.slate.com/blogs/the_slatest/2015/06/17/shooting_at_historic_black_church_in_charleston_south_carolina.html','http://www.ibtimes.com/south-carolina-church-shooting-downtown-charleston-shooting-leaves-least-8-dead-1972376','http://www.cbsnews.com/news/police-multiple-victims-in-south-carolina-church-shooting/','http://twitchy.com/2015/06/17/reports-multiple-people-shot-near-emanuel-ame-church-in-charleston-8-dead/','http://q13fox.com/2015/06/17/report-multiple-fatalities-in-shooting-at-charleston-south-carolina-church/']
    extractDatesLocs(urls)

