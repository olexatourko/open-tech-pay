SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/databasename'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SERVER_NAME = 'localhost:5000' # Used by url_for()

# Flask-Mail
MAIL_SERVER = 'smtp'
MAIL_PORT =  25
MAIL_USE_SSL = False
MAIL_USERNAME = ''
MAIL_PASSWORD = ''

# Used on the frontend for this particular deployment
DEPLOYMENT_NAME = 'OpenPay'
REGION_NAME = 'Region'