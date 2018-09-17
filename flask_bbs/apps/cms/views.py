#endcoding: utf-8
from flask import Blueprint,views,render_template,request,session,redirect,url_for,g,jsonify
from .forms import LoginFrom,ResetpwdForm
from .models import CMSUser
from .decorators import login_required
from exts import db,mail
from flask_mail import Message
from utils import restful
import string,random
import config

bp = Blueprint("cms",__name__,url_prefix="/cms")

@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))

@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')

@bp.route('/email_captcha/')
def email_chptcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请传递邮箱参数！')

    source = list(string.ascii_letters)
    source.extend(map(lambda x:str(x),range(0,10)))

    chptcha = ''.join(random.sample(source,6))
    message = Message('CMS论坛邮箱验证码', recipients=[email], body='您的验证码是:{0}'.format(chptcha))
    try:
        mail.send(message)
    except:
        return restful.server_error()
    return restful.success()

class IndexView(views.MethodView):
    @login_required
    def get(self):
        return render_template('cms/cms_index.html')

class LoginView(views.MethodView):

    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)

    def post(self):
        form = LoginFrom(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    #如果设置session.permanent = True，那么过期时间为31天
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message=u'邮箱或者密码错误')
        else:
            message = unicode(form.get_error(),'utf-8')
            return self.get(message=message)

class RsetPwdView(views.MethodView):
    @login_required
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error('旧密码错误')
        else:
            message = unicode(form.get_error(),'utf-8')
            return restful.params_error(message)

class RsetEmailView(views.MethodView):
    @login_required
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        pass

bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/',view_func=IndexView.as_view('index'))
bp.add_url_rule('/resetpwd/',view_func=RsetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=RsetEmailView.as_view('resetemail'))
