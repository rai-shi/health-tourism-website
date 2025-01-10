This repository is dedicated to the health tourism website developed under the ADAPHA company.

* health-tourism-website

    - backend
    - frontend
 
for API documentation go to http://127.0.0.1:8000/docs/

backend set up

* Python 3.10.16
* PostgreSQL

Don't forget to run migrations when starting up the server for the first time.
```
>> /health-tourism-website/backend$
pip install -r requirements.txt

>> /health-tourism-website/backend/web_backend$
django manage.py makemigrations
django manage.py migrate
django manage.py cities-light 
python manage.py import_specialities
python manage.py import_procedure
python manage.py import_health_institutions

django manage.py runserver
```
