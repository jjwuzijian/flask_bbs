#endcoding: utf-8
from wtforms import StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from ..forms import BaseForm
from utils import zlcache
from flask import g

class LoginFrom(BaseForm):
    email = StringField(validators=[Email(message=u'请输入正确的邮箱信息'),InputRequired(message=u'请输入邮箱')])
    password = StringField(validators=[Length(6,20,message=u'请输入正确的密码')])
    remember = IntegerField()

class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message=u'请输入正确的旧密码')])
    newpwd = StringField(validators=[Length(6, 20, message=u'请输入正确的新密码')])
    newpwd2 = StringField(validators=[EqualTo('newpwd',message=u'两次密码不相同')])

class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message=u'请输入正确格式的邮箱信息')])
    captcha = StringField(validators=[Length(min=6,max=6,message=u'请输入正确长度的验证码')])

    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_cache = zlcache.cache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValueError(u'请输入正确的验证码！')

    def validate_email(self,field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValueError(u'该邮箱地址已经注册过了！')