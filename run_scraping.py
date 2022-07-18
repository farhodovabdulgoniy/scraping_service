import codecs
import os,sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django
django.setup()

from django.db import DatabaseError
from scraping.models import Url, Vacancy,City,Language,Error
from scraping.parsers import *
from django.contrib.auth import get_user_model

User = get_user_model()

parsers = (
    (work,'work'),
    (hh_rabota,'hh_rabota'),
    (dou,'dou'),
)


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            url_data = url_dict.get(pair)
            if url_data:
                tmp['url_data'] = url_dict.get(pair)
                urls.append(tmp)
    return urls


settings = get_settings()
url_list = get_urls(settings)


jobs,errors = [],[]

for data in url_list:

    for func,key in parsers:
        url = data['url_data'][key]
        j, e = func(url,city = data['city'],language = data['language'])
        jobs += j
        errors += e    


for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass        
if errors:
    er = Error(data=errors).save()

    
# h = codecs.open('work.txt','w','utf-8')
# h.write((str(jobs)))
# h.close()
