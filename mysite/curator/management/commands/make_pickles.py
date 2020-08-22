from django.core.management.base import BaseCommand
from django.db import connection
from curator.models import Ad

from sklearn.preprocessing import OneHotEncoder

import pickle
import os
import re

import pandas as pd

pickles_dir = os.path.abspath(os.path.join(os.getcwd(), 'curator', 'pickles'))

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

    path = os.path.join(pickles_dir, 'features_index.pkl')
    with open(path, 'wb') as f:
        pickle.dump(features_index, f)



def save_specs():
    specs = ['transmission', 'cc']
    path = os.path.join(pickles_dir, 'specs.pkl')
    file = open(path, 'wb')
    pickle.dump(specs, file)
    return specs


def save_specs_encoder(df, specs):
    df.dropna(how='any', subset=specs, inplace=True)
    encoder = OneHotEncoder(sparse=False)
    encoder.fit(df[specs])
    path = os.path.join(pickles_dir, 'specs_encoder.pkl')
    file = open(path, 'wb')
    pickle.dump(encoder, file)


def save_kilometers_index(df):
    df.kilos = df.kilos.apply(lambda x: replace_arabic(x))
    kilometers = df.kilos.unique()
    sorted_kilometers = sorted(kilometers, key=lambda x: int(x.split()[-1]))
    path = os.path.join(pickles_dir, 'kilometers_index.pkl')
    file = open(path, 'wb')
    pickle.dump(sorted_kilometers, file)


def replace_arabic(text):
    arabic_numbers  = u'١٢٣٤٥٦٧٨٩٠'
    english_numbers = u'1234567890'

    arabic_regexp = u"(%s)" % u"|".join(arabic_numbers)

    def _sub(match_object, digits):
        return english_numbers[digits.find(match_object.group(0))]

    def _sub_arabic(match_object):
        return _sub(match_object, arabic_numbers)

    return re.sub(arabic_regexp, _sub_arabic, text)


class Command(BaseCommand):
    help = 'save database pickles for further data manipulation when finding the best ads for a car model'

    def handle(self, *args, **options):
        query = str(Ad.objects.all().query)
        df = pd.read_sql_query(query, connection)

        specs = save_specs()
        save_features_index()
        save_kilometers_index(df)
        save_specs_encoder(df, specs)

        self.stdout.write('Saved pickles')


