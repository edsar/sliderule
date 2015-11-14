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

df.mjtheme_namecode[0]
json_normalize(df.mjtheme_namecode[1], meta=['code','name'])
df2 = df.mjtheme_namecode.map(lambda json_val: json_normalize(json_val, meta=['code', 'name']))
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
    
df3= df.mjtheme_namecode.map(lambda json_val: json_normalize(flatten_json(json_val)))



# 3. In 2. above you will notice that some entries have only the code and the name is missing. Create a dataframe with the missing names filled in.

 # create a {code,name: count} dict
# read each df row pulling out the mjtheme_namecode array
# for each item in the mjtheme_namecode array, look for an entry in the {code,name: count} dict
# if the entry exists, increment the count
# else add the entry to the {code,name: count} dict  