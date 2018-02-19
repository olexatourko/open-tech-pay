## Open Pay
A web application for sharing local tech industry compensation.

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
They're in the `/tests` folder. Similair to running the application, set an env variable with the config file location. You should set up a seperate DB just for tests.
```
export CONFIG_FILEPATH=$(pwd)/tests/config.py
python -m unittest discover
```

---

#### PostgreSQL resources

[Installing on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04)  
[Usage with Flask](https://suhas.org/sqlalchemy-tutorial/)