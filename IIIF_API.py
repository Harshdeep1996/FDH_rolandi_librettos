import shutil
import requests
import pandas as pd
from PIL import Image
import io
import pytesseract
import os
import json
import geopy
import geonamescache
import unicodedata as ud

latin_letters= {}

def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
         return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

def only_roman_chars(unistr):
    return all(is_latin(uchr)
           for uchr in unistr
           if uchr.isalpha())
def notAllUpper(string):
    for el in string:
        if el.isupper():
            pass
        else: return True

#ToDo: 1) read manifest.jsons 2) find jpg of first 5 pages 3) ocr pages 4) save as txt
'''

in_memory_file = io.BytesIO(response.content)
im = Image.open(in_memory_file)
im.show()
'''


def findYearTitle(jsonData):
    metaData = jsonData['metadata']
    for el in metaData:
        if el['label'] == 'title':
            title = el['value']
        else: title = 'no_title'
        if el['label'] == 'date_year_start':
            year = el['value']
        else: year = 'no_year'

    return title, year


def cityDic():
    city = geonamescache.GeonamesCache().get_cities()
    cities = {}
    cityList = []
    n=0
    for key in city:
        if city[key]['countrycode'] == 'IT':
            if len(city[key]['alternatenames'][0]) != 0:
                validCityNames = [city[key]['name']] +  [name for name in city[key]['alternatenames']  if only_roman_chars(name) and notAllUpper(name) and len(name)>3]
                cityList += validCityNames

                cities[city[key]['name'].lower()] = [validCityNames, city[key]['countrycode'].lower()]
            else:
                cityList+=[city[key]['name']]
                cities[city[key]['name'].lower()] = [[city[key]['name']], city[key]['countrycode'].lower()]
            n+=1

    print(n)
    return cities, cityList




inPath = '/home/nulpe/Desktop/foundations_dh/fdh_manifests/'
outPath = '/home/nulpe/Desktop/foundations_dh/'
columns =['file_name', 'title', 'date', 'front_page','pot_city_name']
df_librettos = pd.DataFrame(columns= columns)


italianCities, italianCitiesList = cityDic()
print(italianCitiesList)




for idx, filename in enumerate(os.listdir(inPath)):
    tempList = []

    if filename.endswith(".json"):
        tempList.append(filename)
        with open(inPath+filename) as jsonFile:
            jsonData = json.load(jsonFile)
            title, year = findYearTitle(jsonData)
            tempList.append(title)
            tempList.append(year)
            front_page = []
            pot_city_name = []

            pagesData = jsonData['sequences'][0]['canvases']
            page = 0

            for el in pagesData[:5]:
                #get image from api
                imageApi = el['images'][0]['resource']['service']['@id']
                urlPage = imageApi+'/full/,512/0/default.jpg'

                #get text with teseract
                response = requests.get(urlPage, stream=True)
                in_memory_file = io.BytesIO(response.content)
                text = pytesseract.image_to_string(Image.open(in_memory_file), lang='ita')
                textSplit = text.split()

                if len(textSplit) > 50:
                    break

                for word in textSplit:
                    for city in italianCitiesList:
                        if city.lower() == word.lower():
                            pot_city_name.append(city.lower())

                #if cityName:
                 #   print(textSplit)



                front_page += textSplit

            tempList.append(front_page)
            tempList.append(pot_city_name)
            df_librettos.loc[len(df_librettos)] =tempList

            print('we are at ', idx + 1, 'of in total', len(os.listdir(inPath)), 'librettos')

            if (idx+1)  % 10 == 0:
                print(df_librettos)
                df_librettos.columns = ['file_name', 'title', 'date', 'title_page', 'pot_city_name']
                df_librettos.to_pickle(outPath+'librettos.pkl')
                df_librettos.to_csv(outPath+'librettos.csv', index=False, sep='\t', header=True)










