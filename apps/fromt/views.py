from flask import Blueprint,views,render_template

bp = Blueprint("fromt",__name__)

@bp.route('/')
def index():
    return "fromt index"

class SignupView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')

    def post(self) :

bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))