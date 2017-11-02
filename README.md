# Online Shop

# Installation
* clone the repo
* create virtualenv
* `pip install -r requirements.txt` there


# Настройки БД
```
DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'django_db', 
        'USER': 'pasha', 
        'PASSWORD': '***', 
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    } 
} 
```
