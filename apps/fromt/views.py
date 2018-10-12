#endcoding: utf-8
from flask import Blueprint,views,render_template,request,session,redirect,url_for
from .forms import SingnupForm,SigninForm
from utils import restful
from .models import FrontUser
from exts import db
import config

bp = Blueprint("fromt",__name__)

@bp.route('/')
def front_index():
    return render_template('front/front_index.html')

class SignupView(views.MethodView):
    def get(self):
        #获取原URL
        return_to = request.referrer
        if return_to and return_to != request.url:
            return render_template('front/front_signup.html',return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self) :
        form = SingnupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            # model提交数据
            user = FrontUser(telephone=telephone,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())

class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url:
            return render_template('front/front_signin.html', return_to=return_to)
        else:
            return render_template('front/front_signin.html')

    def post(self):
        form = SigninForm(request.form)
        #form表单验证
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    # 如果设置session.permanent = True，那么过期时间为31天
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message=u'账号或者密码错误!')
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/',view_func=SigninView.as_view('signin'))