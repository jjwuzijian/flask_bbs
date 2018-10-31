# _*_ coding: utf-8 _*_
from ..forms import BaseForm
from wtforms import StringField,IntegerField
from wtforms.validators import Regexp,EqualTo,InputRequired
from utils import zlcache

class SingnupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}",message=u'请输入正确的手机号码！')])
    sms_captcha = StringField(validators=[Regexp(r"\w{4}",message=u'请输入正确的短信验证码！')])
    username = StringField(validators=[Regexp(r'.{2,20}',message=u'请输入正确的用户名！')])
    password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z\.]{6,20}",message=u'请输入正确格式的密码！')])
    password2 = StringField(validators=[EqualTo("password1",message=u'两次输入密码不一致！')])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}",message=u"请输入正确的图形验证码！")])

    #定义新的form规则格式为 validate_*(*为前面定义的表单名称)
    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        telephone = self.telephone.data
        if sms_captcha != '1111':
            sms_captcha_mem = zlcache.get(telephone)
            if not sms_captcha_mem or sms_captcha_mem.lower() != sms_captcha.lower():
                raise ValueError(message=u'短信验证码错误！')

    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        if graph_captcha != '1111':
            # print graph_captcha.lower()
            graph_captcha_mem = zlcache.get(graph_captcha.lower())
            if not graph_captcha_mem:
                raise ValueError(message=u'图形验证码错误！')

class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message=u'请输入正确的手机号码！')])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z\.]{6,20}", message=u'请输入正确格式的密码！')])
    remember = StringField()

class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message=u'请输入标题！')])
    content = StringField(validators=[InputRequired(message=u'请输入内容！')])
    board_id = IntegerField(validators=[InputRequired(message=u"请输入板块ID")])

class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message=u'请输入评论内容！')])
    post_id = IntegerField(validators=[InputRequired(message=u"请输入帖子ID")])