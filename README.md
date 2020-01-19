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
composer exec -it open_tech_pay_app /bin/bash
flask db init
flask db upgrade
python utils/seeding/seed_core.py
```

---

### Option 2: Using pipenv

**TODO Readme**

---

#### Running It

**Start the Flask server**

From the `open-pay` directory:
```
export FLASK_APP=$(pwd)/src/application.py
flask run
```
Note: You should use a proper application server like uWSGI in production, but this is good enough for demo purposes.

---

#### Unit tests
They're in the `/tests` folder. Create a config file in the `tests` directory. You should set up a seperate DB just for tests.
```
python -m unittest discover
```

---

#### Resources

##### PostgreSQL
[Installing on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04)  
[Usage with Flask](https://suhas.org/sqlalchemy-tutorial/)

##### Email
Transactional emails are sent with the [Mailjet](https://www.mailjet.com/) because it manages to avoid spam filters pretty well.
Alternatively, you can send emails directly - check out the `own-emails` branch to see how.

[SPF / DKIM setup](https://blog.codinghorror.com/so-youd-like-to-send-some-email-through-code/)  
[Using DKIM with the SMTP Docker image](https://github.com/namshi/docker-smtp/issues/22)