import pandas as pd
import re
from geopy.geocoders import Nominatim
key = 'AIzaSyDO9Hf9LcmDIgXH_jB4pUlMcogZpYcr860'
geolocator = Nominatim(user_agent=key)

locations = pd.read_csv('./data/librettos.csv', delimiter='	')

expr = r'''dramma|drama|melodramma|melodrama|melo-dramma|componimento sacro|per musica|opera|tragedia|spettacolo fantastico|azione romantica|farsa|con l'occasione|commeddia|commedia|operetta|festa|cantata|intermezzo in musica|intermezzi|\. ''' 
locations['title_opera'] = [re.split(expr,s.lower())[0] if len(re.split(expr,s.lower())) > 0 else s for s in locations.title]

expr = r'''dramma per musica|dramma giocoso|farsa giocosa|tragedia lirica|pastorale eroica|dramma buffo|dramma|drama|melodramma|componimento sacro|per musica|opera|tragedia|spettacolo fantastico|azione romantica|farsa|con l'occasione|commeddia|commedia|operetta|festa|cantata|intermezzo in musica|intermezzi''' 
locations['genre_opera'] = [re.search(expr,s.lower()).group(0) if re.search(expr,s.lower()) else 'Not found' for s in locations.title]

place = r'teatro|chiesa|cappella|oratorio|theatre|casa|nozze|sala|carnevale|theatro' 
time = r"anno|l'anno|l'autunno|la primavera|l'estate|l'inverno|dell'anno|il novembre|l'auttuno|ne' mesi di|nel mese di|per la prima opera del|per la fiera|nel prossimo|nel|nella|nell'occasione|con l'occasione|nella stagione di|la stagione|nell'està|in occasione|per la|per il|nel presente|del \d+|carnovale|\d+|\,|il "
locations['location'] = [re.split(time, re.split(place,s.lower())[1])[0] if len(re.split(place,s.lower())) > 1 else 'Not found' for s in locations.title]

locations['location_type'] = [re.search(place,s.lower()).group(0) if re.search(place,s.lower()) else 'Not found' for s in locations.title]
locations['location_full'] = locations['location_type'] + locations['location']

composer = r'per musica di|maestro|posta in musica dal|musica del sig\.|musica del signor|musica è del sig\.|musica è del signor|musicata da'
locations['composer'] = [s[re.search(composer,s.lower()).span(0)[0] : re.search(composer,s.lower()).span(0)[1] + 20]  if re.search(composer,s.lower()) else 'Not found' for s in locations.title]

def get_latitude(x):
    try:
        return x.latitude
    except:
        return 'Not found'

def get_longitude(x):
    try:
        return x.longitude
    except:
        return 'Not found'

geolocate_column = locations['location_full'].apply(geolocator.geocode)
locations['location_latitude'] = geolocate_column.apply(get_latitude)
locations['location_longitude'] = geolocate_column.apply(get_longitude)

locations.to_csv('./data/librettos_1.csv')