# scraping_service
Vacancy scraping service with Django, BeautifulSoup and requests libraries

pip install --upgrade virtualenv

virtualenv env

cd env/

Scripts\activate

cd ..

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
