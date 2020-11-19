import pandas as pd

inPath = '/home/nulpe/Desktop/foundations_dh/data/'


df_librettos = pd.read_pickle(inPath+'librettos_2.pkl')




print(df_librettos.columns)