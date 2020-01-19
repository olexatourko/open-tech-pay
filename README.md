## Open Pay
A web application for sharing local tech industry compensation. It aims to freely provide compensation data to students, employees, and employers in the local tech industry
 so they can make informed career and hiring decisions.

### Key Project Features

- Capture data beyond only salary:
 employee benefits, specific tools used in a job, years with current employer, total number of employers during career, etc...
- Anonymous and verified submissions: using any email, or using a "verified" email based on whitelisted domains. Specific emails addresses will never be shared.
- Segmented data by year - allow multiple submissions from the same sources every year in order to keep the data up to date.
- (TODO) A side tool for valuing non-salary benefits using [NPV](https://www.investopedia.com/terms/n/npv.asp) calculations.

![Preview](https://github.com/olestourko/open-pay/raw/master/preview.png)

---

### Option 1: Running With Docker 

You can use [Docker](https://www.docker.com) to create a container which will grab all of the dependencies for you.
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