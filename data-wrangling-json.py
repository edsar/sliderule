import pandas as pd
import json
from pandas.io.json import json_normalize

# Using data in file 'data/world_bank_projects.json' and the techniques demonstrated above,

df = pd.read_json('data/world_bank_projects.json')

# 1. Find the 10 countries with most projects

df[["countryname"]].stack().value_counts()[:10]
# People's Republic of China         19
# Republic of Indonesia              19
# Socialist Republic of Vietnam      17
# Republic of India                  16
# Republic of Yemen                  13
# Kingdom of Morocco                 12
# People's Republic of Bangladesh    12
# Nepal                              12
# Republic of Mozambique             11
# Africa                             11

# 2. Find the top 10 major project themes (using column 'mjtheme_namecode')

df[["mjtheme"]].stack().value_counts()[:10]
# [Human development]                                                                             25
# [Environment and natural resources management]                                                  22
# [Public sector governance]                                                                      18
# [Rural development]                                                                             14
# [Environment and natural resources management, Environment and natural resources management]    12
# [Financial and private sector development]                                                      11
# [Social protection and risk management]                                                         10
# [Social dev/gender/inclusion]                                                                    8
# [Human development, Human development]                                                           8
# [Financial and private sector development, Financial and private sector development]             6

import simplejson as json
    
json.dumps(df.mjtheme_namecode[0])
themes_json = df.mjtheme_namecode.map(lambda x: json.dumps(x))
themes_json.to_json('data/themes.json', orient='records')
themes = pd.read_json('data/themes.json', orient='records')

d = {}
#d2 = {}
df = pd.DataFrame(d)
#x = 0
for row in themes.iterrows():
    for row_item in row[1]:
        # print row_item
        json_list = json.loads(row_item)
        for item in json_list:
            # x = x + 1 #1500 total
            #d['code'] = item['code']
            #d['name'] = item['name']
            #d.update(item)
            #df.append(item, ignore_index=True)
            # print json_normalize(item, meta=["code","name"])
            if item["name"] is None or item["name"]=="":
                pass
            else:
                d[item["code"]] = item["name"]
                # if d2[d[item["code"],d[item["name"]] is None:
                #     pass
                # else:
                #     d2[d[item["code"],d[item["name"]] = count
            # print item["name"]
            # print k, v
            # if [item["code"], item["name"]] in dict:
            #     count = 
            #     d[item["code"], item["name"]] = count+1
d
#ANSWER
# {u'1': u'Economic management',
#  u'10': u'Rural development',
#  u'11': u'Environment and natural resources management',
#  u'2': u'Public sector governance',
#  u'3': u'Rule of law',
#  u'4': u'Financial and private sector development',
#  u'5': u'Trade and integration',
#  u'6': u'Social protection and risk management',
#  u'7': u'Social dev/gender/inclusion',
#  u'8': u'Human development',
#  u'9': u'Urban development'}

df.mjtheme_namecode[0]
x = json_normalize(df.mjtheme_namecode[0], meta=['code','name'])
y = df.mjtheme_namecode.map(lambda json_val: json_normalize(json_val[0], meta=['code', 'name']))
json_normalize(df, 'mjtheme_namecode', ['mjtheme', 'shortname', ['info', 'governor']])

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[str(name[:-1])] = str(x)

    flatten(y)
    return out
    
project_themes = df.mjtheme_namecode.map(lambda json_val: flatten_json(json_val))

# create a {code,name: count} dict
# read each df row pulling out the mjtheme_namecode array
# for each item in the mjtheme_namecode array, look for an entry in the {code,name: count} dict
# if the entry exists, increment the count
# else add the entry to the {code,name: count} dict

    themerows = ptheme

# 3. In 2. above you will notice that some entries have only the code and the name is missing. 
# Create a dataframe with the missing names filled in.


