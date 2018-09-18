# _*_ coding: utf-8 _*_
from .views import bp
from flask import session,g
from .models import CMSUser
import config

@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user