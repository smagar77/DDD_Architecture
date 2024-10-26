# DEMO-BACKEND

Backend for DEMO

## Getting started

```
git clone https://github.com/atulingale-sdc/demo.git
cd demo
```

## Install Redis
```
sudo apt-get update
sudo apt install redis
redis-cli --version
sudo systemctl status redis
```

## Install Pipenv
```
sudo apt install python3-pip
python3 -m pip install --user pipenv
```


# Setup auth service
```
cd services/auth-service/ && pipenv install
rename .env_sample to .env
set SQLALCHEMY_URI absolute path
pipenv shell
export PYTHONPATH=.
alembic upgrade heads
python auth_service &
```

```
to access auth service please visit - http://localhost:8080 or http://127.0.0.1:8080
to access API documentation please visit http://localhost:8080/docs or http://127.0.0.1:8080/docs
```

# Setup weather service
```
rename .env_sample to .env
cd services/weather-service/ && pipenv install
pipenv shell
alembic upgrade heads
python weather_service &
```
```
to access weather service visit - http://127.0.0.1:7074/docs
```

```
to access weather service please visit - http://localhost:8081 or http://127.0.0.1:8081
to access API documentation please visit http://localhost:8081/docs or http://127.0.0.1:8081/docs
```


## login credentials
```
sachin@demo.com / admin@123
```