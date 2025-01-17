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
python manage.py import_destinations
```

* Finally you can run the server
```
>> /health-tourism-website/backend/web_backend$
django manage.py runserver
```


you can find some example data in deneme-info.txt for api test 
```
/home/gokce/Masaüstü/Projects/Adapha/health-tourism-website/backend/web_backend/deneme-info.txt
```