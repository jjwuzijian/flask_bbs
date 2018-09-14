#endcoding: utf-8
from flask import Blueprint,views,render_template,request,session,redirect,url_for
from .forms import LoginFrom
from .models import CMSUser
from .decorators import login_required
import config

bp = Blueprint("cms",__name__,url_prefix="/cms")

@bp.route('/')
@login_required
def index():
    return "cms index"

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

bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
