#endcoding: utf-8
from flask import Blueprint,views,render_template,request,session,redirect,url_for,g,jsonify
from .forms import LoginFrom,ResetpwdForm,ResetEmailForm,AddBannerForm,UpdateBannerForm
from .models import CMSUser,CMSPersmission
from ..models import BannerModel
from .decorators import login_required,permission_required
from exts import db,mail
from flask_mail import Message
from utils import restful,zlcache
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
    zlcache.set(email,chptcha)
    return restful.success()

@bp.route('/boards/')
@login_required
@permission_required(CMSPersmission.BOARDER)
def boards():
    return render_template('cms/cms_boards.html')

@bp.route('/comments/')
@login_required
@permission_required(CMSPersmission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')

@bp.route('/croles/')
@login_required
@permission_required(CMSPersmission.ADMINER)
def croles():
    return render_template('cms/cms_croles.html')

@bp.route('/cusers/')
@login_required
@permission_required(CMSPersmission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')

@bp.route('/fusers/')
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')

@bp.route('/posts/')
@login_required
@permission_required(CMSPersmission.POSTER)
def posts():
    return render_template('cms/cms_posts.html')

@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.all()
    return render_template('cms/cms_banners.html',banners = banners)

@bp.route('/abanner/',methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())

@bp.route('/ubanner/',methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图')
    else:
        return restful.params_error(message=form.get_error())

@bp.route('/dbanner/',methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图ID')

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图')

    db.session.delete(banner)
    db.session.commit()
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
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())

bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/',view_func=IndexView.as_view('index'))
bp.add_url_rule('/resetpwd/',view_func=RsetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=RsetEmailView.as_view('resetemail'))
