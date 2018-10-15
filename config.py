# _*_ coding: utf-8 _*_
import os

SECRET_KEY = os.urandom(24)
DEBUG = True

#数据库配置
DB_URI = 'mysql+pymysql://root:1234@localhost:3306/bbs?charset=utf8'
# DB_URI = 'mysql+pymysql://root:123456@localhost:3306/bbs?charset=utf8'
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = '12321'
FRONT_USER_ID = '122131'

#set_mail_config
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
# MAIL_USE_SSL
MAIL_USERNAME = '2662147461@qq.com'
MAIL_PASSWORD = 'ilhxkotdnsnuebfi'
MAIL_DEFAULT_SENDER = '2662147461@qq.com'

#短信验证配置
ALIDAYU_APP_KEY = '23709557'
ALIDAYU_APP_SECRET = 'd9e430e0a96e21c92adacb522a905c4b'
ALIDAYU_SIGN_NAME = u'小饭桌应用'
ALIDAYU_TEMPLATE_CODE = 'SMS_68465012'

#图片配置
image_path = 'static/image/'
