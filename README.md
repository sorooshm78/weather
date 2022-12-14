# weather

### Usage
I am using python "3.10.6" version 

first step clone my project
```
git clone https://github.com/sorooshm78/weather/
```
[OpenWeatherMap](https://openweathermap.org) API used to access the live weather details.

go to [OpenWeatherMap](https://openweathermap.org) website and create account and get your API Key 

so rename sample_secret.json to secret.json and copy your API Key into file 
```
{
    "Key": "Your API KEY"
}
```

and then install requirements  
```
pip install -r requirements.txt
```

This will create all the migrations file (database migrations) required to run this App.
```
python manage.py makemigrations
```

Now, to apply this migrations run the following command
```
python manage.py migrate
```

### Setup Redis Cache 
Install Redis on Linux 
```
sudo apt-get update
sudo apt-get install redis
```
Run the Redis server from a new terminal window.
```
redis-server
```
and you can change redis configurations in core/settings.py
```
# Cash setting
CACHE_TTL = 60 * 15
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}
```

by default cached for 15 minutes and you change timeout cache
```
CACHE_TTL = 60 * 15 # second
```


### Running the code 
Just go into the code directory and type 
```
python manage.py runserver
```
"weather" app will start on 127.0.0.1:8000 (Local Address).
 
enjoy it!