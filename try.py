import pandas as pd

def makeListOutOfCsvString(csv_strings):
    list_of_strings = []
    for li in city_names:
        temp = ''.join([i for i in li if i.isalpha() or i == ','])
        temp = temp.split(',')
        list_of_strings.append(temp)
    return list_of_strings

inPath = '/home/nulpe/Desktop/foundations_dh/data/'


df_librettos = pd.read_csv(inPath+'librettos_1.csv')
city_names = df_librettos.pot_city_name.tolist()

Pot_city_name_fuzzy = makeListOutOfCsvString(city_names)




print(Pot_city_name_fuzzy)