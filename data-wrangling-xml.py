
# reference: https://docs.python.org/2.7/library/xml.etree.elementtree.html
# data source: http://www.dbis.informatik.uni-goettingen.de/Mondial

from xml.etree import ElementTree as ET
import operator

# document_tree = ET.parse( './data/mondial_database_less.xml' )

# print names of all countries
for child in document_tree.getroot():
    print child.find('name').text

# print names of all countries and their cities
for element in document_tree.iterfind('country'):
    print '* ' + element.find('name').text + ':',
    capitals_string = ''
    for subelement in element.getiterator('city'):
        capitals_string += subelement.find('name').text + ', '
    print capitals_string[:-2]

# Using data in 'data/mondial_database.xml', the examples above, 
# and refering to https://docs.python.org/2.7/library/xml.etree.elementtree.html, find


# 10 countries with the lowest infant mortality rates
# DONE!
for country in document.iterfind('country'):
	if country.find('infant_mortality') is None:
		pass
	else:
		name = country.find('name').text
		im = country.find('infant_mortality').text
		d[name] = float(im)

sorted_dict = sorted(d.items(), key=operator.itemgetter(1))

print sorted_dict[:10]

# ANSWER:
# [('Monaco', 1.81), ('Japan', 2.13), ('Bermuda', 2.48), ('Norway', 2.48), ('Singapore', 2.53), 
# ('Sweden', 2.6), ('Czech Republic', 2.63), ('Hong Kong', 2.73), ('Macao', 3.13), ('Iceland', 3.15)]

# 10 cities with the largest population
# DONE! 
for country in document.iterfind('country'):
	if country.find("population[@year='2000']") is None:
		pass
	else:
		name = country.find('name').text
		pop = country.find("population[@year='2000']").text
		d[name] = int(pop)

sorted_dict = sorted(d.items(), key=operator.itemgetter(1), reverse=True)

print sorted_dict[:10]

# ANSWER (2000):
# [('China', 1242612226), ('United States', 281414181), ('Indonesia', 205132458), ('Brazil', 169799170), 
# ('Russia', 146762881), ('Pakistan', 143832014), ('Japan', 125714674), ('Mexico', 97483412), 
# ('Philippines', 76506928), ('Turkey', 67808719)]

# 10 ethnic groups with the largest overall populations (sum of best/latest estimates over all countries)
document = ET.parse( './data/mondial_database.xml' )
d = {}
for country in document.iterfind('country'):
    # print country.find('./population[last()]').get('year')
    # print country.find('./population[last()]').text
    
    #lastpop = country.find('./population[last()]')
    if country.find('./ethnicgroup[1][@percentage]') is None:
        pass
    else:
        lastpop = int(country.find('./population[last()]').text)
        ethnic = country.find('./ethnicgroup[1]')
        ethnicname = ethnic.text
        ethicperc = float(ethnic.get('percentage'))/100
        print country.find('name').text, ethnicname
        print lastpop * ethicperc
        d[country.find('name').text, ethnicname] = lastpop * ethicperc
  
sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)[:10]
# (('China', 'Han Chinese'), 1245058800.0),
#  (('India', 'Dravidian'), 302713744.25),
#  (('United States', 'European'), 254958101.97759998),
#  (('Nigeria', 'African'), 162651570.84),
#  (('Bangladesh', 'Bengali'), 146776916.72),
#  (('Japan', 'Japanese'), 126534212.00000001),
#  (('Russia', 'Russian'), 114646210.938),
#  (('Indonesia', 'Javanese'), 113456006.10000001),
#  (('Brazil', 'European'), 108886717.794),
#  (('Vietnam', 'Viet/Kinh'), 76078375.3)]  
    
# name and country of a) longest river
d = {}
for river in document.iterfind('river'):
    name = river.get('id')
    print name
    country = river.get('country')
    print country
    length = river.find('./length')
    if length is None:
        pass
    else:
        print float(length.text)
        d[name, country]=float(length.text)
    
sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)[:1]
sorted_d
# [(('river-Amazonas', 'CO BR PE'), 6448.0)]

# name and country of b) largest lake
d = {}
for lake in document.iterfind('lake'):
    name = lake.get('id')
    print name
    country = lake.get('country')
    print country
    area = lake.find('./area')
    if area is None:
        pass
    else:
        print float(area.text)
        d[name, country]=float(area.text)

sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)[:1]
sorted_d

# Caspian Sea
#[(('lake-KaspischesMeer', 'R AZ KAZ IR TM'), 386400.0)]

# name and country of c) airport at highest elevation
d = {}
for airport in document.iterfind('airport'):
    name = airport.get('iatacode')
    print name
    country = airport.get('country')
    print country
    elevation = airport.findtext('./elevation')
    print type(elevation)
    if elevation is None:
        pass
    elif elevation=='':
        pass
    else:
        print float(elevation)
        d[name, country]=float(elevation)

sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)[:1]
sorted_d      
# El Alto Intl, Bolivia
# [(('LPB', 'BOL'), 4063.0)]