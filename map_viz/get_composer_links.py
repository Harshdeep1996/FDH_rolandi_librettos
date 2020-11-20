import pandas as pd

x = pd.read_csv('../../data/librettos_1.csv')

y = x[x['composer'] != 'Not found']
y = y[x['city_name'] != '0']

YEAR_TICKS = list(range(1606, 1926, 22))

y['merged'] = y.apply(lambda row: {row['city_name']:[row['date'],row['title']]}, axis=1)

y3 = y[['merged', 'composer']].groupby('composer').agg(list)
y3 = y3[y3['merged'].apply(lambda x: True if len(x) > 1 else False)]

y3['cities'] = y3['merged'].apply(lambda x: set([[*i][0] for i in x]))
y3 = y3[y3['cities'].apply(lambda x: True if len(x) > 1 else False)]

def lower_bound_check(x):
    lower_bounds = []
    for i in x:
        for j, y in enumerate(YEAR_TICKS):
            if y > int(i):
                lower_bounds.append(YEAR_TICKS[j-1])
                break
    return lower_bounds

y3['lower_bounds'] = y3['merged'].apply(
    lambda x: set(lower_bound_check([list(i.values())[0][0] for i in x])))
y3.to_csv('data/composer_links.csv')
