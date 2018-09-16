#endcoding: utf-8
from flask import Blueprint,views,render_template,request,session,redirect,url_for
from .forms import LoginFrom
from .models import CMSUser
from .decorators import login_required
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

class IndexView(views.MethodView):
    @login_required
    def get(self):
        return render_template('cms/cms_index.html')

    def post(self):
        pass

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
                return self.get(message='邮箱或者密码错误')

        else:
            message = unicode(form.errors.popitem()[1][0],'utf-8')
            return self.get(message=message)

class RsetPwdView(views.MethodView):
    @login_required
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        pass



bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/',view_func=IndexView.as_view('index'))
bp.add_url_rule('/resetpwd/',view_func=RsetPwdView.as_view('resetpwd'))
