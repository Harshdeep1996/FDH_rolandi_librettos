import pandas as pd
import re

#locations = pd.read_csv('./data/librettos.csv', delimiter='	')
locations = pd.read_pickle('./data/librettos.pkl')
expr = r'''dramma|drama|melodramma|melodrama|melo-dramma|componimento sacro|per musica|opera|tragedia|spettacolo fantastico|azione romantica|farsa|con l'occasione|commeddia|commedia|operetta|festa|cantata|intermezzo in musica|intermezzi|\. ''' 
locations['title_opera'] = [re.split(expr,s.lower())[0] if len(re.split(expr,s.lower())) > 0 else s for s in locations.title]

expr = r'''dramma per musica|dramma giocoso|farsa giocosa|tragedia lirica|pastorale eroica|dramma buffo|dramma|drama|melodramma|componimento sacro|per musica|opera|tragedia|spettacolo fantastico|azione romantica|farsa|con l'occasione|commeddia|commedia|operetta|festa|cantata|intermezzo in musica|intermezzi''' 
locations['genre_opera'] = [re.search(expr,s.lower()).group(0) if re.search(expr,s.lower()) else 'Not found' for s in locations.title]

place = r'teatro|chiesa|cappella|oratorio|theatre|casa|nozze|sala|carnevale|theatro' 
time = r"l'anno|dell'anno|del \d+|\d+|\,"
locations['location'] = [re.split(time, re.split(place,s.lower())[1])[0] if len(re.split(place,s.lower())) > 1 else 'Not found' for s in locations.title]

locations['location_type'] = [re.search(place,s.lower()).group(0) if re.search(place,s.lower()) else 'Not found' for s in locations.title]

composer = r'per musica di|maestro|posta in musica dal|musica del sig\.|musica del signor|musica è del sig\.|musica è del signor|musicata da'
locations['composer'] = [s[re.search(composer,s.lower()).span(0)[0] : re.search(composer,s.lower()).span(0)[1] + 20]  if re.search(composer,s.lower()) else 'Not found' for s in locations.title]

locations.to_csv('./data/librettos_1.csv')
locations.to_pickle('/home/nulpe/Desktop/foundations_dh/data/librettos_1.pkl')

print(locations.pot_city_name.tolist())

for potCity in locations.pot_city_name.tolist():
    print(type(potCity))