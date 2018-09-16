import os

SECRET_KEY = os.urandom(24)
DEBUG = True

DB_URI = 'mysql+pymysql://root:1234@localhost:3306/bbs?charset=utf8'
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = '12321'