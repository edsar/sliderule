
# reference: https://docs.python.org/2.7/library/xml.etree.elementtree.html
# data source: http://www.dbis.informatik.uni-goettingen.de/Mondial

from xml.etree import ElementTree as ET
import pandas as pd
import operator

# document_tree = ET.parse( './data/mondial_database_less.xml' )

# # print names of all countries
# for child in document_tree.getroot():
#     print child.find('name').text

# # print names of all countries and their cities
# for element in document_tree.iterfind('country'):
#     print '* ' + element.find('name').text + ':',
#     capitals_string = ''
#     for subelement in element.getiterator('city'):
#         capitals_string += subelement.find('name').text + ', '
#     print capitals_string[:-2]

# Using data in 'data/mondial_database.xml', the examples above, 
# and refering to https://docs.python.org/2.7/library/xml.etree.elementtree.html, find


document = ET.parse( './data/mondial_database.xml' )
root = document.getroot()
d = {}

# 10 countries with the lowest infant mortality rates

# DONE!
# for country in document.iterfind('country'):
# 	if country.find('infant_mortality') is None:
# 		pass
# 	else:
# 		name = country.find('name').text
# 		im = country.find('infant_mortality').text
# 		d[name] = float(im)

# sorted_dict = sorted(d.items(), key=operator.itemgetter(1))

# print sorted_dict[:10]

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



# name and country of a) longest river, 



# name and country b) largest lake and 




# name and country c) airport at highest elevation


