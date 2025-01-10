This repository is dedicated to the health tourism website developed under the ADAPHA company.

* health-tourism-website

    - backend
    - frontend
 
for API documentation go to http://127.0.0.1:8000/docs/

backend set up

* Python 3.10.16
* PostgreSQL

Before starting up the server,

* Install required packages
```
>> /health-tourism-website/backend$
pip install -r requirements.txt
```

* Run migrations 
```
>> /health-tourism-website/backend/web_backend$
django manage.py makemigrations
django manage.py migrate
```

* Then some automatic database uploading must be done
```
>> /health-tourism-website/backend/web_backend$
django manage.py cities-light 
python manage.py import_specialities
python manage.py import_procedure
python manage.py import_health_institutions
```

* Finally you can run the server
```
>> /health-tourism-website/backend/web_backend$
django manage.py runserver
```
