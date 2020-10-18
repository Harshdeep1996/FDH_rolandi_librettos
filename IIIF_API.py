import shutil
import requests
import pandas as pd
from PIL import Image
import io
import pytesseract
import os
import json


#ToDo: 1) read manifest.jsons 2) find jpg of first 5 pages 3) ocr pages 4) save as txt
'''
## Schema: http://ronallo.com/iiif-workshop-new/image-api/uri-parameters.html
url = 'http://dl.cini.it:8080/digilib/Scaler/IIIF/bd9aa8e401ba48d8cba45f31b7381953.jpg/full/,512/0/default.jpg'

response = requests.get(url, stream=True)

print(response.raw)

in_memory_file = io.BytesIO(response.content)
im = Image.open(in_memory_file)
im.show()


print(pytesseract.image_to_string(Image.open(in_memory_file), lang='ita'))
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



inPath = '/home/nulpe/Desktop/foundations_dh/fdh_manifests/'
outPath = '/home/nulpe/Desktop/foundations_dh/'
columns =['file_name', 'title', 'date', 'page_1', 'page_2', 'page_3', 'page_4', 'page_5']
df_librettos = pd.DataFrame(columns= columns)

for idx, filename in enumerate(os.listdir(inPath)):
    tempList = []

    if filename.endswith(".json"):
        tempList.append(filename)
        with open(inPath+filename) as jsonFile:
            jsonData = json.load(jsonFile)
            title, year = findYearTitle(jsonData)
            tempList.append(title)
            tempList.append(year)

            pagesData = jsonData['sequences'][0]['canvases']
            for el in pagesData[:5]:
                #get image from api
                imageApi = el['images'][0]['resource']['service']['@id']
                urlPage = imageApi+'/full/,512/0/default.jpg'

                #get text with teseract
                response = requests.get(urlPage, stream=True)
                in_memory_file = io.BytesIO(response.content)
                text = pytesseract.image_to_string(Image.open(in_memory_file), lang='ita')
                tempList.append(text)

            df_librettos.loc[len(df_librettos)] =tempList

            print('we are at ', idx + 1, 'of in total', len(os.listdir(inPath)), 'librettos')

            if (idx+1)  % 10 == 0:
                print(df_librettos)
                df_librettos.columns = ['file_name', 'title', 'date', 'page_1', 'page_2', 'page_3', 'page_4', 'page_5']
                df_librettos.to_pickle(outPath+'librettos.pkl')










