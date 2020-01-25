## Open Pay
A web application for sharing local tech industry compensation. It aims to freely provide compensation data to students, employees, and employers in the local tech industry
 so they can make informed career and hiring decisions.

Here is an active implementation: http://londontechpay.ca

---

### Option 1: Running With Docker 

You can use [Docker](https://www.docker.com) and docker-compose to create a container which will grab all of the dependencies for you.
First, create a `.env` file in your root directory. Set where the DB container will store its data using the `HOST_SQL_STORAGE_PATH=` variable.
  ```
docker-compose build
docker-compose up
```

You'll need to run the database migrations and seed the database if you haven't:
```
docker exec -it open_tech_pay_app /bin/bash
flask db init
flask db upgrade
python utils/seeding/seed_core.py
```

---

### Option 2: Using pipenv for local development without Docker

**TODO Readme**

---

#### Unit tests
They're in the `/tests` folder. Create a config file in the `tests` directory. You should set up a seperate DB just for tests.
```
python -m unittest discover
```