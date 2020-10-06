"""Contains the functions which preprocess the database when read using pandas"""

import re
import pickle
import os
import numpy as np

from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import percentileofscore

def load_features_index():
    file = open("curator/pickles/features_index.pkl", "rb")
    return pickle.load(file)


def load_sorted_kilometers_dict():
    file = open("curator/pickles/kilometers_index.pkl", "rb")
    return pickle.load(file)


def load_specs():
    file = open("curator/pickles/specs.pkl", "rb")
    return pickle.load(file)


def check_feature(x, feature):
    if x:
        return int(feature in x)
    else:
        return 0


def one_hot_encode_features(df, features_index):
    for feature_en, feature_ar in features_index.items():
        df[feature_en] = df.features.apply(lambda x: check_feature(x, feature_ar))
    return df.iloc[:, 16:]


def load_one_hot_encoder(df, specs):
    df.dropna(how="any", subset=specs, inplace=True)
    encoder = OneHotEncoder(sparse=False)
    encoder.fit(df[specs])
    return encoder


def encode_kilometers(kilometers, index):
    return kilometers.apply(lambda x: index[x])


def make_ad_vectors(ads, features_index, specs_encoder, kilometers_index, specs):
    one_hot_features = one_hot_encode_features(ads, features_index).values
    one_hot_specs = specs_encoder.transform(ads[specs])
    encoded_kilometers = encode_kilometers(ads.kilos, kilometers_index).values.reshape(-1, 1)
    one_hot_array = np.concatenate([one_hot_specs, one_hot_features], axis=1)
    indices = ads.index.values
    price_percentiles = ads.price.apply(lambda x: percentileofscore(ads.price, x))
    return indices, price_percentiles, encoded_kilometers, one_hot_array


def drop_na_rows(df, specs):
    df = df.dropna(how="any", subset=specs).reset_index(drop=True)
    return df


def replace_arabic(text):
    arabic_numbers  = u'١٢٣٤٥٦٧٨٩٠'
    english_numbers = u'1234567890'

    arabic_regexp = u"(%s)" % u"|".join(arabic_numbers)

    def _sub(match_object, digits):
        return english_numbers[digits.find(match_object.group(0))]

    def _sub_arabic(match_object):
        return _sub(match_object, arabic_numbers)

    return re.sub(arabic_regexp, _sub_arabic, text)


def preprocess_queried_ads(ads):
    ads = ads.drop(columns=["imgs", "description"])  # drop these columns as they don't serve in similarity scores
    specs = load_specs()
    features_index = load_features_index()
    specs_encoder = load_one_hot_encoder(ads, specs)
    kilometers_index = load_sorted_kilometers_dict()
    ads.kilos = ads.kilos.apply(lambda x: replace_arabic(x))
    ads = drop_na_rows(ads, specs)
    indices, price_percentiles, ad_kilos, ad_vectors = make_ad_vectors(ads, features_index, specs_encoder, kilometers_index, specs)        
    return indices, price_percentiles, ad_kilos, ad_vectors


def calculate_weighted_average(x):
    if x.size != 0:
        weights = np.arange(1, len(x)+1)[::-1]
        average = (weights * x).sum() / weights.sum()
        return average
    else:
        return 0


def calculate_triangluar_similarity_matrix(vectors):
    n = len(vectors)
    dist = np.zeros((n, n))
    row, col = np.triu_indices(n, 1)
    dist[row, col] = cosine_similarity(vectors)[row, col]
    return dist


def score_queried_ads(ads):
    indices, price_percentiles, ad_kilometers, ad_vectors = preprocess_queried_ads(ads)

    dist = calculate_triangluar_similarity_matrix(ad_vectors)
    dist_f = np.fliplr(dist)  # flip the similarity matrix to give higher weights to higher prices ads in weighted average
    scores = np.zeros((dist_f.shape[0]))  
    for i, row in enumerate(dist_f):
        x = row[np.nonzero(row)]
        score = calculate_weighted_average(x)
        scores[i] = score

    scores += (ad_kilometers.ravel()/32)  # adds positive bias towards ads with lower kilometers
    scores -= (price_percentiles.ravel()/192)  # adds negative bias towards ads with higher prices

    sorted_indices = [idx for _, idx in sorted(zip(scores, indices), reverse=True)]

    return sorted_indices

