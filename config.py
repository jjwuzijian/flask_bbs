import os

SECRET_KEY = os.urandom(24)
DEBUG = True

# DB_URI = 'mysql+pymysql://root:1234@localhost:3306/bbs?charset=utf8'
DB_URI = 'mysql+pymysql://root:123456@localhost:3306/bbs?charset=utf8'
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = '12321'

#set_mail_config
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
# MAIL_USE_SSL
MAIL_USERNAME = '2662147461@qq.com'
MAIL_PASSWORD = 'ilhxkotdnsnuebfi'
MAIL_DEFAULT_SENDER = '2662147461@qq.com'
