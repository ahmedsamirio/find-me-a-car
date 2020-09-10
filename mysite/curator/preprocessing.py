"""Contains the functions which preprocess the database when read using pandas"""

import re
import pickle

from sklearn.preprocessing import OneHotEncoder
from scipy.stats import percentileofscore

def load_features_index():
    file = open("pickles/features.pkl", "rb")
    return pickle.load(file)


def check_feature(x, feature):
    if x == ['']:
        return 0
    else:
        return int(feature in x)


def one_hot_encode_features(df, features_index):
    for feature_en, feature_ar in features_index.items():
        df[feature_en] = df.Features.apply(lambda x: check_feature(x, feature_ar))
    return df.iloc[:, 17:]


def load_one_hot_encoder(df, specs):
    df.dropna(how="any", subset=specs, inplace=True)
    encoder = OneHotEncoder(sparse=False)
    encoder.fit(df[specs])
    return encoder


def encode_kilometers(kilometers, index):
    return kilometers.apply(lambda x: index[x])


def make_ad_vector(df, features_index, specs_encoder, kilometers_index, specs):
    one_hot_features = one_hot_encode_features(df, features_index).values
    one_hot_specs = specs_encoder.transform(df[specs])
    encoded_kilometers = encode_kilometers(df.Kilometers, kilometers_index).values.reshape(-1, 1)
    one_hot_array = np.concatenate([one_hot_specs, one_hot_features], axis=1)
    indices = model_df.index.values
    price_percentiles = model_df.Price.apply(lambda x: percentileofscore(model_df.Price, x))
    return indices, price_percentiles, encoded_kilometers, one_hot_array


def drop_na_rows(df, specs):
    df = df.dropna(how="any", subset=specs).reset_index(drop=True)
    return df