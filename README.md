## Open Pay
A web application for sharing local tech industry compensation. The key project goal is to close the pay information gap
by providing detailed data for a specific region.

 This project aims to freely provide compensation data to students, employees, and employers in the local tech industry
 so they can make informed career and hiring decisions.

### Key Project Features

- Capture data beyond only salary:
 employee benefits, specific tools used in a job, years with current employer, total number of employers during career, etc...
- Anonymous and verified submissions: using any email, or using a "verified" email based on whitelisted domains. Specific emails addresses will never be shared.
- Segmented data by year - allow multiple submissions from the same sources every year in order to keep the data up to date.
- A side tool for valuing non-salary benefits using [NPV](https://www.investopedia.com/terms/n/npv.asp) calculations.

![Preview](https://github.com/olestourko/open-pay/raw/master/preview.png)

---

#### Dependencies


**[Flask](http://flask.pocoo.org/docs/0.12/quickstart/)**: The web application framework.

```
pip install flask
```

**[SQLAlchemy](https://www.sqlalchemy.org/)**:  The ORM (+ some extensions).

```
pip install psycopg2-binary # using postgreSQL instead of MySQL
pip install sqlalchemy
pip install flask-sqlalchemy
pip install flask-migrate
pip install flask-mail
```

- [Flask Integration](http://flask.pocoo.org/docs/0.12/quickstart/)
- [Migrations Extension](https://flask-migrate.readthedocs.io/en/latest/)

**[Marshmallow](https://marshmallow.readthedocs.io/en/latest/)**:  Model mapper for SQLAlchemy model -> JSON.

```
pip install marshmallow
```

---

#### Running It

First get the dependencies above, then...

**Initial Migrations and Seeding**

First specify your database credentials in a file called `/config.py`. (check out /`example_config.py`)

```
flask db init
flask db migrate
flask db upgrade
```

Seed the db with clients and product ares:

```
python src/seed.py
```

**Start the Flask server**

From the `bc-sample` directory:
```
export FLASK_APP=$(pwd)/src/application.py
export CONFIG_FILEPATH=$(pwd)/config.py
flask run
```
Note: You should use a proper application server like uWSGI in production, but this is good enough for demo purposes.

---

#### Unit tests
They're in the `/tests` folder. Similar to running the application, set an env variable with the config file location. You should set up a seperate DB just for tests.
```
python -m unittest discover
```

---

#### PostgreSQL resources

[Installing on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04)  
[Usage with Flask](https://suhas.org/sqlalchemy-tutorial/)