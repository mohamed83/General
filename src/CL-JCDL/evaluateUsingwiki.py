# -*- coding: utf-8 -*
from scripts.eventUtils import getTokens, getIntersection
ldas= []
with open('ldas.txt','r') as f:
    for l in f:
        p = l.strip().split(",")
        ldas.append(p)
        #print p
ners= []
with open('ners.txt','r') as f:
    for l in f:
        p = l.strip().split(",")
        ners.append(p)
        #print p
events = ['ebola','pakistan_flood','virginia_earthquake','brazil_fire','sandy','tucson_shooting']
wiki = {}
wiki['pakistan_flood'] = ''' The floods in Pakistan began in late July 2010, resulting from heavy monsoon rains in the Khyber Pakhtunkhwa, Sindh, Punjab and Balochistan regions of Pakistan, which affected the Indus River basin. Approximately one-fifth of Pakistan's total land area was underwater, approximately 796,095 square kilometres (307,374 sq mi).[3][4][5] According to Pakistani government data, the floods directly affected about 20 million people, mostly by destruction of property, livelihood and infrastructure, with a death toll of close to 2,000.[1]

UN Secretary-General Ban Ki-moon had initially asked for US$460 million (€420 million) for emergency relief, noting that the flood was the worst disaster he had ever seen. Only 20% of the relief funds requested had been received on 15 August 2010.[6] The U.N. had been concerned that aid was not arriving fast enough, and the World Health Organization reported that ten million people were forced to drink unsafe water.[7] The Pakistani economy was harmed by extensive damage to infrastructure and crops.[8] Damage to structures was estimated to exceed US$4 billion (€2.5 billion), and wheat crop damages were estimated to be over US$500 million (€425 million).[9] Total economic impact may have been as much as US$43 billion (€35 billion)'''

wiki['ebola'] = '''
The most widespread epidemic of Ebola virus disease (commonly known as "Ebola") in history is currently ongoing in several West African countries.[11][12] It has caused significant mortality, with reported case fatality rates of up to 71%[13][14][15] and specifically 57-59% among hospitalized patients.[9] Ebola virus disease was first described in 1976 in two simultaneous outbreaks in sub-Saharan Africa; this is the 26th outbreak and the first to occur in West Africa. It began in Guinea in December 2013 and then spread to Liberia and Sierra Leone.[13] A small outbreak of twenty cases occurred in Nigeria and one case occurred in Senegal, both now declared disease-free.[16] Several cases were reported in Mali,[17] but this outbreak has also been declared over,[7] and an isolated case has been reported in the United Kingdom.[14] Imported cases in the United States and Spain have led to secondary infections of medical workers but have not spread further.[18][19] As of 25 January 2015, the World Health Organization (WHO) and respective governments have reported a total of 22,091 suspected cases and 8,810 deaths,[4] though the WHO believes that this substantially understates the magnitude of the outbreak.[1][20][21]

This is the first Ebola outbreak to reach epidemic proportions; past outbreaks were brought under control within a few weeks. Extreme poverty, a dysfunctional healthcare system, a mistrust of government officials after years of armed conflict, and the delay in responding to the outbreak for several months have all contributed to the failure to control the epidemic. Other factors include local burial customs that include washing of the body after death, the spread to densely populated cities, and international indifference.[22][23][24][25][26]

As the disease progressed, many hospitals, short on both staff and supplies, became overwhelmed and closed, leading some health experts to state that the inability to treat other medical needs may be causing "an additional death toll [that is] likely to exceed that of the outbreak itself".[27][28] Hospital workers, who work closely with the highly contagious body fluids of the diseased, have been especially vulnerable to catching the disease. In August 2014, the WHO reported that ten percent of the dead have been healthcare workers.[29] In September, the WHO estimated that the countries' capacity for treating Ebola patients was insufficient by the equivalent of 2,122 beds. In December, they reported that at a national level there were now a sufficient number of beds to treat and isolate all reported Ebola cases, although the uneven distribution of cases was resulting in serious shortfalls in some areas. In other words, a patient may be required to travel a long distance to reach a treatment facility, which may not be very realistic in many instances. [30]

The World Health Organization has been criticised for its delay in taking action to address the epidemic. By September 2014, Médecins Sans Frontières/Doctors Without Borders (MSF), the non-governmental organization (NGO) with the largest working presence in the affected countries, had grown increasingly critical of the international response. Speaking on 3 September, the president of MSF spoke out concerning the lack of assistance from the United Nations member countries saying, "Six months into the worst Ebola epidemic in history, the world is losing the battle to contain it."[31] On 3 September, the United Nations' senior leadership said it could be possible to stop the Ebola outbreak in 6 to 9 months, but only if a "massive" global response is implemented.[32] The Director-General of the WHO, Margaret Chan, called the outbreak "the largest, most complex and most severe we've ever seen" and said that it is "racing ahead of control efforts".[32] In a 26 September statement, the WHO said, "The Ebola epidemic ravaging parts of West Africa is the most severe acute public health emergency seen in modern times.'''

wiki['virginia_earthquake']= '''
The 2011 Virginia Earthquake occurred on August 23 at 1:51:04 p.m. local time in the Piedmont region of the US state of Virginia. The epicenter, in Louisa County, was 61 km (38 mi) northwest of Richmond and 8 km (5 mi) south-southwest of the town of Mineral. It was an intraplate earthquake with a magnitude of 5.8 and a maximum perceived intensity of VII (very strong) on the Mercalli intensity scale. Several aftershocks, ranging up to 4.5 Mw in magnitude, occurred after the main tremor.

The earthquake, along with a magnitude–5.8 quake on the New York–Ontario border during 1944, is the largest to have occurred in the U.S. east of the Rocky Mountains since an earthquake centered in Giles County in western Virginia occurred during 1897,[3] with an estimated magnitude of 5.8.[4]

The quake was felt across more than a dozen U.S. states and in several Canadian provinces, and was felt by more people than any other quake in U.S. history.[5] No deaths and only minor injuries were reported. Minor damage to buildings was widespread and was estimated by one risk-modeling company at $200 million to $300 million, of which about $100 million was insured.[6][7]

The earthquake prompted research that revealed that the farthest landslide from the epicenter was 150 miles (240 km), by far the greatest landslide distance recorded from any other earthquake of similar magnitude. Previous studies of worldwide earthquakes indicated that landslides occurred no farther than 36 miles (58 km) from the epicenter of a magnitude 5.8 earthquake. The Virginia earthquake study suggested that the added information about East Coast earthquakes may prompt a revision of equations that predict ground shaking.'''

wiki['brazil_fire']= '''
The Kiss nightclub fire started between 2:00 and 2:30 (BRST)[1] on 27 January 2013 in Santa Maria, Rio Grande do Sul, Brazil, killing at least 242 people[2] and injuring at least 168 others.[3][4][5][6][7] It is considered the second most-devastating fire disaster in the history of Brazil—surpassed only by the Great North American Circus fire of December 1961, which killed 503 people in Niterói, and the deadliest nightclub fire since the December 2000 fire that killed 309 people in Luoyang, China. It is also the third-deadliest nightclub fire in history, behind the Luoyang Christmas fire and the Cocoanut Grove fire in 1942.

Because it was a high-casualty fire caused by illegal indoor usage of outdoor pyrotechnics, the disaster bore similarities to the 2003 Station nightclub fire[8] in West Warwick, Rhode Island in the United States; the 2004 República Cromañón nightclub fire in Buenos Aires, Argentina; the 2008 Wuwang Club fire in Shenzen, China; the 2009 Santika Club fire in Watthana, Bangkok, Thailand (cause is disputed); and the 2009 Lame Horse fire in Perm, Russia.'''

wiki['sandy']='''Hurricane Sandy (also unofficially known as "Superstorm Sandy") was the deadliest and most destructive hurricane of the 2012 Atlantic hurricane season, as well as the second-costliest hurricane in United States history. Classified as the eighteenth named storm, tenth hurricane and second major hurricane of the year, Sandy was a Category 3 storm at its peak intensity when it made landfall in Cuba.[1] While it was a Category 2 storm off the coast of the Northeastern United States, the storm became the largest Atlantic hurricane on record (as measured by diameter, with winds spanning 1,100 miles (1,800 km)).[3][4] Estimates as of March 2014 assess damage to have been over $68 billion (2013 USD), a total surpassed only by Hurricane Katrina.[5] At least 233 people were killed along the path of the storm in eight countries.[6][2]

Sandy developed from a tropical wave in the western Caribbean Sea on October 22, quickly strengthened, and was upgraded to Tropical Storm Sandy six hours later. Sandy moved slowly northward toward the Greater Antilles and gradually intensified. On October 24, Sandy became a hurricane, made landfall near Kingston, Jamaica, re-emerged a few hours later into the Caribbean Sea and strengthened into a Category 2 hurricane. On October 25, Sandy hit Cuba as a Category 3 hurricane, then weakened to a Category 1 hurricane. Early on October 26, Sandy moved through the Bahamas.[7] On October 27, Sandy briefly weakened to a tropical storm and then restrengthened to a Category 1 hurricane. Early on October 29, Sandy curved north-northwest and then[8] moved ashore near Brigantine, New Jersey, just to the northeast of Atlantic City, as a post-tropical cyclone with hurricane-force winds.[1][9]

In Jamaica, winds left 70% of residents without electricity, blew roofs off buildings, killed one, and caused about $100 million (2012 USD) in damage. Sandy's outer bands brought flooding to Haiti, killing at least 54, causing food shortages, and leaving about 200,000 homeless; the hurricane also caused two deaths in the Dominican Republic. In Puerto Rico, one man was swept away by a swollen river. In Cuba, there was extensive coastal flooding and wind damage inland, destroying some 15,000 homes, killing 11, and causing $2 billion (2012 USD) in damage. Sandy caused two deaths and damage estimated at $700 million (2012 USD) in The Bahamas. In Canada, two were killed in Ontario and an estimated $100 million (2012 CAD) in damage was caused throughout Ontario and Quebec.[10]

In the United States, Hurricane Sandy affected 24 states, including the entire eastern seaboard from Florida to Maine and west across the Appalachian Mountains to Michigan and Wisconsin, with particularly severe damage in New Jersey and New York. Its storm surge hit New York City on October 29, flooding streets, tunnels and subway lines and cutting power in and around the city.[11][12] Damage in the United States amounted to $65 billion (2013 USD)'''
wiki['tucson_shooting']= '''
On January 8, 2011, U.S. Representative Gabrielle Giffords and eighteen others were shot during a constituent meeting held in a supermarket parking lot in Casas Adobes, Arizona, in the Tucson metropolitan area. Six people died, including federal District Court Chief Judge John Roll; Gabe Zimmerman, one of Rep. Giffords' staffers; and a nine-year-old girl, Christina-Taylor Green.[2][5][6][7][8] Giffords was holding the meeting, called "Congress on Your Corner" in the parking lot of a Safeway store when Jared Lee Loughner drew a pistol and shot her in the head before proceeding to fire on other people.[5][6] One additional person was injured in the immediate aftermath of the shooting.[3] News reports identified the target of the attack as Giffords, a Democrat representing Arizona's 8th congressional district.[5] She was shot through the head at point-blank range, and her medical condition was initially described as "critical".[5][6]

Loughner, a 22-year-old Tucson man who was fixated on Giffords, was arrested at the scene.[4] Federal prosecutors filed five charges against him, including the attempted assassination of a member of Congress and the assassination of a federal judge.[7][9][10] Loughner had been arrested (but not convicted) once on a minor drug charge[11] and had been suspended by his college for disruptive behavior. Court filings include notes handwritten by Loughner indicating he planned to assassinate Giffords.[9] The motive for the shooting remains unclear; Loughner did not cooperate with authorities, invoking his right to remain silent.[6] He was held without bail and indicted on 49 counts. In January 2012, Loughner was found by a federal judge to be incompetent to stand trial based on two medical evaluations, which diagnosed him with paranoid schizophrenia.[12] Judged still incompetent to stand trial on May 25, finally on August 7, Loughner had a hearing at which he was judged competent. He pleaded guilty to 19 counts, and in November 2012 was sentenced to life in prison.

Following the shooting, American and international politicians expressed grief and condemnations. Attention focused on the harsh political rhetoric in the United States. Some commentators blamed members of the political right wing for the shooting; in particular, Sarah Palin was implicated because of gun-related metaphors in her speeches and because of the website of her political action committee which "targeted" the districts of Giffords and others with pictures of crosshairs on an electoral map. Others defended Palin by noting that Loughner hated all politicians regardless of their affiliation.[13] Gun control advocates pushed for increased restrictions on the sale of firearms and ammunition, specifically high-capacity ammunition magazines.[14] President Barack Obama led a nationally televised memorial service on January 12, and other memorials took place'''

students = {}
methods = ['lda','ner','summary']

students['sandy'] = {}
students['sandy']['lda']=ldas[0]
students['sandy']['ner']=ners[0]
students['sandy']['summary']= ''' The storm, Hurricane Sandy, hits in New York on October 2012. The hurricane was a Category 1. Furthermore, the hurricane had a wind speed of 75 mph. hurricane Sandy formed in the Atlantic. Also, Hurricane Sandy had a size of 1000 miles wide. Hurricane Sandy caused 10 inches of rain. For more information. Search for hurricane sandy.'''

students['tucson_shooting'] = {}
students['tucson_shooting']['lda']=ldas[1]
students['tucson_shooting']['ner']=ners[1]
students['tucson_shooting']['summary']=''' On the night of Sunday, January 9, Jared lee opened fire in Tucson. The suspect fired 5 rounds out of his rifle. 6 people lost their lives. 32 of the people were hurt, and are being treated for their injuries. The victims were between the ages of 40 and 50'''

students['brazil_fire'] = {}
students['brazil_fire']['lda']=ldas[2]
students['brazil_fire']['ner']=ners[2]
students['brazil_fire']['summary']=''' In January 2013 there was a fire started by indoor fireworks in Santa Maria. This fire, fueled by ignited foam, grew to the size of the building, engulfed the club and ended up killing 309. Firefighters worked to douse a fire at the Kiss Club. One exit was made unavailable for a period of time. Compared to previous fires in the city it was a fast-moving fire.'''

students['virginia_earthquake'] = {}
students['virginia_earthquake']['lda']=ldas[3]
students['virginia_earthquake']['ner']= ners[3]
students['virginia_earthquake']['summary']=''' On 23 August, 2011 at 1:51, a 5.8 magnitude earthquake struck Virginia, The epicenter of the quake was located at Louisa. There were aftershocks that followed the earthquake and no tsunami was caused by the earthquake. There are no reports of landslides due of this earthquake. A total of 140 deaths occurred'''

students['ebola'] = {}
students['ebola']['lda']=ldas[4]
students['ebola']['ner']=ners[4]
students['ebola']['summary']=''' There has been an outbreak of Ebola reported in the following locations: Liberia, West Africa, Nigeria, Guinea, and Sierra Leone. 
In January 2014, there were between 425 and 3052 cases of Ebola in Liberia, with between 2296 and 2917 deaths. Additionally, In January 2014, there were between 425 and 4500 cases of Ebola in West Africa, with between 2296 and 2917 deaths. Also, In January 2014, there were between 425 and 3000 cases of Ebola in Nigeria, with between 2296 and 2917 deaths. Furthermore, In January 2014, there were between 425 and 3052 cases of Ebola in Guinea, with between 2296 and 2917 deaths. In addition, In January 2014, there were between 425 and 3052 cases of Ebola in Sierra Leone, with between 2296 and 2917 deaths. 
There were previous Ebola outbreaks in these areas. Ebola was found in 1989 in Liberia. As well, Ebola was found in 1989 in West Africa. Likewise, Ebola was found in 1989 in Nigeria. Additionally, Ebola was found in 1989 in Guinea. Also, Ebola was found in 1989 in Sierra Leone. 
Ebola virus disease (EVD; also Ebola hemorrhagic fever, or EHF), or simply Ebola, is a disease of humans and other primates caused by Ebola viruses. Signs and symptoms typically start between two days and three weeks after contracting the virus as a fever, sore throat, muscle pain, and headaches. Then, vomiting, diarrhea and rash usually follow, along with decreased function of the liver and kidneys. At this time some people begin to bleed both internally and externally. The disease has a high risk of death, killing between 25 percent and 90 percent of those infected with the virus, averaging out at 50 percent.[1] This is often due to low blood pressure from fluid loss, and typically follows six to sixteen days after symptoms appear.
'''

students['pakistan_flood'] = {}
students['pakistan_flood']['lda']=ldas[5]
students['pakistan_flood']['ner']=ners[5]
students['pakistan_flood']['summary']=''' In August 2010 a flood spanning 600 miles caused by heavy monsoon affected the Indus river in Pakistan, The total rainfall was 200 millimeters and the total cost of damage was 250 million dollars. The flood killed 3000 people, left 809 injured, and approximately 15 million people were affected. In addition 1300 people are still missing. The cities of Nasirabad Badheen and Irvine were affected most by flooding, in the province of Sindh Mandalay and Punjab, finally nearly all of the flood damage occurred in the state of Pakistan'''

wikiTokens = {}
for k in wiki:
    wikiTokens[k] = getTokens(wiki[k])

for k in students:
    students[k]['lda'] = getTokens(' '.join(students[k]['lda']))
    students[k]['ner'] = getTokens(' '.join(students[k]['ner']))
    students[k]['summary'] = getTokens(students[k]['summary'])
    #students[k]['summary'] = students[k]['lda'] + students[k]['ner'] + students[k]['summary']


evalResults = {}
for k in students:
    evalResults[k] = {}
    ws = set(wikiTokens[k])
    for d in students[k]:
        s = students[k][d]
        r = getIntersection(ws, set(s))
        #print r
        evalResults[k][d] = r
        print d, k, len(r), len(s)#len(ws)
        #print len(r)* 1.0/len(ws)
        if len(s):
            print len(r)* 1.0/len(s)
        else:
            print 0