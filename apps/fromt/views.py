from flask import Blueprint,views,render_template,make_response
from io import BytesIO
from utils.captcha.xtcaptcha import Captcha

bp = Blueprint("fromt",__name__)

@bp.route('/')
def index():
    return "fromt index"

@bp.route('/captcha/')
def graph_captcha():
    text,image = Captcha.gene_code()
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return  resp

class SignupView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')

bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))