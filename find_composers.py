import pandas as pd
from difflib import SequenceMatcher
import plac
import spacy
import shutil
import requests
import pandas as pd
from PIL import Image
import io
import pytesseract
import os
import json

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


@plac.annotations(
    model=("Model to load (needs parser and NER)", "positional", None, str)
)
def main(texts, model="it_core_news_sm"):

    nlp = spacy.load(model)
    #print("Processing %d texts" % len(texts))


    for text in [texts]:
        #print(text)
        doc = nlp(text)
        person = extract_currency_relations(doc)

        return person

def extract_currency_relations(doc):
    # Merge entities and noun chunks into one token
    spans = list(doc.ents) + list(doc.noun_chunks)

    spans = spacy.util.filter_spans(spans)
    relations = []
    #print(doc)
    truth_val = False

    entity_tree = []

    for ent in doc.ents:

        entity_tree_extracted = ent.text, ent.label_, [str(i).lower() for i in ent.subtree]
        entity_tree.append(entity_tree_extracted)

    people = []
    for el in entity_tree:
        if el[1] == 'PER':
            people.append(el[0])

    if len(people)>=1:
        return people[0]
    else: return -1


inPath = '/home/nulpe/Desktop/foundations_dh/data/'


#join Aurel & Ludovica df's
df_librettos = pd.read_pickle(inPath+'librettos_ver_best.pkl')
df_lib_2 = pd.read_csv(inPath+'librettos_2.csv').drop(['Unnamed: 0'], axis=1)

join_columns = [col for col in df_lib_2.columns if col not in df_librettos.columns]

print(df_librettos.columns)
df_librettos.to_csv('/home/nulpe/Desktop/try_librettos.csv', index=False)
print(join_columns)


#searching for composers
hit_words = ['musica di','maestro', 'posta in musica dal', 'musica del sig', 'musica del signor','musica è del sig', 'musicata da', 'musica']
hit_words = ['maestro', 'musica', 'signore', 'sig.']

n=0

titles = df_librettos.title.tolist()

meastroList = []




for idx, cop in  enumerate(df_librettos.coperta.tolist()):
    tempDirector = []

    cop = [c.lower() for c in cop]

    for indx, word in enumerate(cop):
        if word == 'musica':

            for i in range(3):
                if cop[indx+i] in ['del', 'dal', 'd', 'di', 'da', 'det', 'd1']:
                    cop_str = ' '.join(cop[indx:indx + 7])

                    person = main(cop_str)
                    if person !=-1:
                        tempDirector.append(person)
                        print(len(meastroList))

        if word == 'maestro':
            cop_str = ' '.join(cop[indx:indx + 7])

            person = main(cop_str)
            if person != -1:
                tempDirector.append(person)
                print(person)


        for comp in ['compositore', 'composta']:
            if comp in word:
                cop_str = ' '.join(cop[indx-5:indx + 5])

                person = main(cop_str)
                if person != -1:
                    tempDirector.append(person)
                    print(person)

    title = titles[idx]

    for indx, word in enumerate(title.split()):

        if 'musica' in word:

            for i in range(len(title.split()[indx:]) ):
                if title.split()[indx+i] in ['del', 'dal', 'd', 'di', 'da', 'det', 'd1']:
                    cop_str = ' '.join(title.split()[indx:indx + 5])

                    person = main(cop_str)
                    if person !=-1:
                        tempDirector.append(person)
                        print(person)


        if 'maestro' in word:
            cop_str = ' '.join(title.split()[indx:indx + 5])

            person = main(cop_str)
            if person != -1:
                tempDirector.append(person)
                print(person)


    if len(tempDirector)> 0:
        meastroList.append(tempDirector[-1])
        n+=1
        print('Number of matches', n)
        print('position ', len(meastroList))


    else: meastroList.append('')


print(len(meastroList))


df_librettos['composers'] = meastroList


df_librettos.to_csv(inPath+'librettos_with_composers.csv', index=False, header=True)
