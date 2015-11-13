
# reference: https://docs.python.org/2.7/library/xml.etree.elementtree.html
# data source: http://www.dbis.informatik.uni-goettingen.de/Mondial

from xml.etree import ElementTree as ET

document_tree = ET.parse( './data/mondial_database_less.xml' )

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


# 10 cities with the largest population


# 10 ethnic groups with the largest overall populations (sum of best/latest estimates over all countries)
# name and country of a) longest river, b) largest lake and c) airport at highest elevation



document = ET.parse( './data/mondial_database.xml' )