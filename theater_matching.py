import spacy
import pandas as pd
import numpy as np
nlp = spacy.load("it_core_news_sm")

from nltk.cluster import KMeansClusterer
import nltk

locations = pd.read_csv('data/librettos_2.csv')
locations = locations.fillna('NaN')
locations['location_vec'] = [np.mean(np.array([token.vector for token in nlp(loc)]), axis=0) for loc in locations.location_full]

NUM_CLUSTERS=150

kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=100, avoid_empty_clusters=True)
assigned_clusters = kclusterer.cluster(locations['location_vec'], assign_clusters=True)
locations['predicted_cluster'] = kclusterer.cluster(locations['location_vec'], assign_clusters = True)
locations['centroid'] = locations['predicted_cluster'].apply(lambda x: obj.means()[x])

locations.to_csv('data/librettos_2.csv')