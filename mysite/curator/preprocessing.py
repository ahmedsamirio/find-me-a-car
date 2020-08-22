"""Contains the functions which preprocess the database when read using pandas"""

import re
import pickle

from sklearn.preprocessing import OneHotEncoder

def replace_arabic(text):
    arabic_numbers  = u'١٢٣٤٥٦٧٨٩٠'
    english_numbers = u'1234567890'

    arabic_regexp = u"(%s)" % u"|".join(arabic_numbers)

    def _sub(match_object, digits):
        return english_numbers[digits.find(match_object.group(0))]

    def _sub_arabic(match_object):
        return _sub(match_object, arabic_numbers)

    return re.sub(arabic_regexp, _sub_arabic, text)


def save_features_index():
    features_index = {'ABS': 'نظام فرامل ABS',
                     'AC': 'تكييف',
                     'Air_bags': 'وسائد هوائية',
                     'Radio': 'راديو اف ام',
                     'AUX': 'مدخل aux اوديو',
                     'EBD': 'EBD',
                     'Fog_lights': 'فوانيس شبورة',
                     'Electric_mirrors': 'مرايا كهربائية',
                     'Electric_seats': 'مقاعد كهربائية',
                     'Electric_windows': 'زجاج كهربائي',
                     'Touch_screen': 'شاشة تعمل باللمس',
                     'USB': 'شاحن يو اس بي',
                     'Anti_theft': 'تنبيه / نظام مضاد للسرقة',
                     'Bluetooth': 'بلوتوث',
                     'Cruise_control': 'مثبت سرعة',
                     'Start/stop': 'زر تشغيل / إيقاف المحرك',
                     'GPS': 'نظام ملاحة',
                     'Off_road_wheels': 'عجلات للطرق الوعرة',
                     'Parking_sensors': 'حساسات ركن',
                     'Center_lock': 'سنتر لوك',
                     'Power_steering': 'باور ستيرنج',
                     'Rear_cam': 'كاميرا خلفية',
                     'Custom_wheels': 'إطارات خاصة',
                     'Sunroof': 'فتحة سقف',
                     'Leather_seats': 'مقاعد جلد',
                     'Roof_holder': 'حامل السقف'}
    with open("features_index.pkl", 'wb') as f:
        pickle.dump(features_index, f)


def load_features_index():
    file = open("pickles/feautres_index.pkl", 'rb')
    features_index = pickle.load(file)
    return features_index


def save_specs():
    specs = ["transmission", "cc"]
    file = open("pickles/specs.pkl", 'wb')
    pickle.dump(specs, file)


def load_specs():
    file = open("pickles/specs.pkl", 'rb')
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


def save_specs_encoder(df, specs):
    df.dropna(how="any", subset=specs, inplace=True)
    encoder = OneHotEncoder(sparse=False)
    encoder.fit(df[specs])
    file = open("pickles/specs_encoder.pkl", 'wb')
    pickle.dump(encoder, file)


def load_specs_encoder():
    file = open("pickles/specs_encoder.pkl", 'rb')
    return pickle.load(file)


def save_kilometers_index(df):
    model_df.kilometers = model_df.kilometers.apply(lambda x: replace_arabic(x))
    kilometers = model_df.Kilometers.unique()
    sorted_kilometers = sorted(kilometers, key=lambda x: int(x.split()[-1]))
    file = open("pickles/kilometers_index.pkl", "wb")
    pickle.dump(sorted_kilometers, file)


def load_kilometers_index():
    file = open("pickles/kilometers_index.pkl", "wb")
    return pickle.load(file)


def encode_kilometers(kilometers, index):
    return kilometers.apply(lambda x: index[x])


def make_ad_vector(df, features_index, specs_encoder, kilometers_index, specs):
    one_hot_features = one_hot_encode_features(df, features_index).values
    one_hot_specs = specs_encoder.transform(df[specs])
    encoded_kilometers = encode_kilometers(df.Kilometers, kilometers_index).values.reshape(-1, 1)
    one_hot_array = np.concatenate([encoded_kilometers, one_hot_specs, one_hot_features], axis=1)
    return one_hot_array



def drop_na_rows(df, specs):
    df = df.dropna(how="any", subset=specs).reset_index(drop=True)
    return df



