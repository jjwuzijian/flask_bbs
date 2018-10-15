# _*_ coding: utf-8 _*_
from flask import Blueprint,request,make_response
from utils import restful,zlcache
from exts import alidayu
from utils.captcha import xtcaptcha
from .forms import SMSCaptchaForm
from io import BytesIO
from utils.captcha.xtcaptcha import Captcha

bp = Blueprint("common",__name__,url_prefix="/c")

# @bp.route('/sms_captcha/')
# def sms_acptcha():
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(message='请输入手机号码！')
#     captcha = xtcaptcha.Captcha.gene_code()
#     if alidayu.send_sms(telephone,code=captcha):
#         return restful.success()
#     else:
#         # return restful.params_error(message='短信验证码发送失败！')
#         return restful.success()

@bp.route('/sms_captcha/',methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = xtcaptcha.Captcha.gene_text()
        print(u'短信验证码是：',captcha)
        if alidayu.send_sms(telephone,code=captcha):
            zlcache.set(telephone,captcha)
            return restful.success()
        else:
            zlcache.set(telephone, captcha)
            return restful.success()
    else:
        return restful.params_error(message=u'参数错误！')

@bp.route('/captcha/')
def graph_captcha():
    text,image = Captcha.gene_code()
    zlcache.set(text.lower(),text.lower())
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return  resp

