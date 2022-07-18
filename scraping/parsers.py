import requests
import codecs
from bs4 import BeautifulSoup
from random import randint


headers = [ # fake information for trick the server
    {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/533+ (KHTML, like Gecko)'}
    ]


__all__ = ('work','hh_rabota','dou')


def work(url,city = None,language = None):
    
    domain = 'https://www.work.ua'
    jobs = []
    errors = []
    if url:
        resp = requests.get(url=url,headers=headers[randint(0,2)])
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content,'html.parser')
            main_div = soup.find('div',id='pjax-job-list')
            if main_div:
                div_lst = main_div.find_all('div',attrs={'class':'job-link'})
                for div in div_lst:
                    title = div.find('h2')
                    comp_div = div.find('div',attrs = {'class':'add-top-xs'}).span
                    company = comp_div.text
                    if not company:
                        company = 'No name'
                    href = title.a['href']
                    description = div.p.text
                    jobs.append({
                        'title':title.text,
                        'description':description,
                        'company':company,
                        'url':domain + href,
                        'city_id':city,
                        'language_id':language,
                    })
            else:
                errors.append({
                    'url':url,
                    'title':'Div does not exists.'
                })
        else:
            errors.append({
                'url':url,
                'title':'Page do not response.'
            })

    return jobs,errors


def hh_rabota(url,city = None,language = None):

    jobs = []
    errors = []
    if url:
        resp = requests.get(url=url,headers=headers[randint(0,2)])
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content,'html.parser')
            main_div = soup.find('div',id = 'a11y-main-content')
            if main_div:
                div_lst = main_div.find_all('div',attrs={'class':'vacancy-serp-item__layout'})
                for div in div_lst:
                    title = div.find('h3')
                    href = title.a['href']
                    company = div.find('div',attrs = {'class':'vacancy-serp-item__meta-info-company'}).text
                    if not company:
                        company = 'No name'
                    description = div.find('div', attrs = {'class':'g-user-content'}).text
                    jobs.append({
                        'title':title.text,
                        'url':href,
                        'company':company,
                        'description':description,
                        'city_id':city,
                        'language_id':language,
                    })
            else:
                errors.append({
                    'url':url,
                    'title':'Div does not exists.'
                })
        else:
            errors.append({
                'url':url,
                'title':'Page do not response.',

            })

    return jobs,errors


def dou(url,city = None,language = None):

    jobs = []
    errors = []
    if url:
        resp = requests.get(url=url,headers=headers[randint(0,2)])
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content,'html.parser')
            main_div = soup.find('div',id='vacancyListId')
            if main_div:
                li_lst = main_div.find_all('li',attrs={'class':'l-vacancy'})
                for li in li_lst:
                    title = li.find('div',attrs = {'class':'title'})
                    href = title.a['href']
                    description = li.find('div',attrs = {'class':'sh-info'})
                    company = 'No name'
                    a = title.find('a', attrs = {'class':'company'})
                    if a:
                        company = a.text
                    jobs.append({
                        'title':title.a.text,
                        'description':description.text,
                        'company':company,
                        'url': href,
                        'city_id':city,
                        'language_id':language,
                    })
            else:
                errors.append({
                    'url':url,
                    'title':'Div does not exists.'
                })
        else:
            errors.append({
                'url':url,
                'title':'Page do not response.'
            })

    return jobs,errors


##########################################
# for testing scraping functions

# if __name__ == '__main__':
#     url = ''
#     jobs,errors = work(url)
#     h = codecs.open('work.txt','w','utf-8')
#     h.write((str(jobs)))
#     h.close()

