import pandas as pd
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

inPath = '/home/nulpe/Desktop/foundations_dh/data/'


df_librettos = pd.read_pickle(inPath+'librettos.pkl')

filter_pot_city = ['casale', 'vittoria', 'desio', 'nola', 'bali', 'mira', 'sora', 'sora',
                   'genzano', 'faro']

print(df_librettos.columns)

city_names = df_librettos.pot_city_name.tolist()

print(len(city_names))

city_names_dic = {}
for cityLst in city_names:
    for city in cityLst:
        if city in city_names_dic:
            city_names_dic[city]+=1
        else: city_names_dic[city] = 1

popular_cities = []
for key in city_names_dic:
    if city_names_dic[key] >10:
        popular_cities.append(key)


city_matching_sec = []

pot_cities = df_librettos.pot_city_name.tolist()
n=0

k=0
for lst in pot_cities:
    if len(lst)>0: k+=1
print(k)

for ind, cop in enumerate(df_librettos.coperta.tolist()):
    tempAddPotCity = []
    for word in cop:
        word = word.lower()
        for city in popular_cities:
            if city != word and similar(city, word) > 0.85:
                #print(word)
                #print(city)
                #print('\n')
                tempAddPotCity.append(city)
                n+=1
    city_matching_sec.append(pot_cities[ind]+tempAddPotCity)


print('we have ',n ,'new cities of in total ', len(df_librettos.coperta.tolist()))



k=0
for lst in city_matching_sec:
    if len(lst)>0: k+=1
print(k)