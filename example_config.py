SQLALCHEMY_DATABASE_URI = 'mysql://root:root@db/open_tech_pay'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SERVER_NAME = 'hostname' # Used by url_for()

#Mailjet
MAILJET_API_KEY = None
MAILJET_API_SECRET = None

# Used on the frontend for this particular deployment
DEPLOYMENT_NAME = ''
REGION_NAME = ''

# A List of string messages
MESSAGES = []

# Other settings
MARKET_DATA_MIN_DISPLAY = 4
RANDOMIZE_MARKET_DATA = False