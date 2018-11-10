#endcoding: utf-8
from flask import Blueprint,views,render_template,request,session,redirect,url_for,g,abort
from .forms import SingnupForm,SigninForm,AddPostForm,AddCommentForm
from utils import restful
from .models import FrontUser
from ..models import BannerModel,BoardsModel,PostModel,CommentModel,HighlightPostModel
from exts import db
from .decorators import login_required
from flask_paginate import Pagination,get_page_parameter
from sqlalchemy.sql import func
import config

bp = Blueprint("fromt",__name__)

@bp.route('/logout/')
@login_required
def logout():
    del session[config.FRONT_USER_ID]
    return redirect(url_for('fromt.front_index'))

@bp.route('/')
def front_index():
    board_id = request.args.get('bd',type=int,default=None)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardsModel.query.all()
    page = request.args.get(get_page_parameter(),type=int,default=1)
    sort = request.args.get("sort",type=int,default=1)
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE
    posts = None
    total = 0

    query_obj = None
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    if sort == 2:
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(HighlightPostModel.create_time.desc(),PostModel.create_time.desc())
    if sort == 3:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    if sort == 4:
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(func.count(CommentModel.id).desc(),PostModel.create_time.desc())


    if board_id:
        query_obj = query_obj.filter(PostModel.board_id==board_id)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start,end)
        total = query_obj.count()
    pagination = Pagination(bs_version=3,page=page,total=total,outer_window=0,inner_window=2)
    context = {
        'banners':banners,
        'boards':boards,
        'posts':posts,
        'pagination':pagination,
        'current_board':board_id,
        'current_sort':sort,
    }
    return render_template('front/front_index.html',**context)

@bp.route('/p/<post_id>')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    return render_template('front/front_pdetail.html',post=post)

@bp.route('/acomment/',methods=['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这个帖子！')
    else:
        return restful.params_error(form.get_error())

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