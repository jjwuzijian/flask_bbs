#endcoding: utf-8
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
import shortuuid
import enum

class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4

class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    #unique=True表示不容许出现相同的数据  nullable=False表示不容许出现空值
    telephone = db.Column(db.String(50),nullable=False,unique=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    #default表示默认值
    gender = db.Column(db.Enum(GenderEnum),default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,*args,**kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop("password")
        super(FrontUser,self).__init__(*args,**kwargs)

    @property
    #禁止访问属性
    def password(self):
        return self._password

    @password.setter
    #重写password属性，设置为加密模式
    def password(self,newpwd):
        self._password = generate_password_hash(newpwd)

    #加密验证
    def check_password(self,rawpwd):
        return check_password_hash(self._password,rawpwd)