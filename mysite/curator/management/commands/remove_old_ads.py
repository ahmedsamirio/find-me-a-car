from curator.models import Ad

import requests, threading

from .config import *
from django.core.management.base import BaseCommand



removed_ads_ids = []
threads = []

def fetch_ad_status(ad): 
    global removed_ads_ids 

    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=20)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    ad_status = session.get(ad.url, headers=headers).status_code
    if ad_status != 200: 
        removed_ads_ids.append(ad.id) 

class Command(BaseCommand):
    help = "remove old ads"

    def handle(self, *args, **options):

        for ad in Ad.objects.all():
            print('Checking', ad)
            thread = threading.Thread(target=fetch_ad_status, args=[ad])
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
            print('Finished', thread)

        Ad.objects.filter(id__in=removed_ads_ids).delete()

        # print(removed_ads_ids)