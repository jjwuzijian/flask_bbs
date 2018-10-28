#endcoding: utf-8
from flask import Blueprint,views,render_template,request,session,redirect,url_for,g
from .forms import SingnupForm,SigninForm,AddPostForm
from utils import restful
from .models import FrontUser
from ..models import BannerModel,BoardsModel,PostModel
from exts import db
from decorators import login_required
import config

bp = Blueprint("fromt",__name__)

@bp.route('/')
def front_index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardsModel.query.all()
    posts = PostModel.query.all()
    context = {
        'banners':banners,
        'boards':boards,
        'posts':posts,
    }
    return render_template('front/front_index.html',**context)

@bp.route('/apost/',methods=['GET','POST'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardsModel.query.all()
        return render_template('front/front_apost.html',boards=boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardsModel.query.get(board_id)
            if not board:
                return restful.params_error(message='没有这个板块！')
            post = PostModel(title=title,content=content)
            post.board = board
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())



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