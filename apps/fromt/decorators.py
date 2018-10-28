# _*_ coding: utf-8 _*_
from flask import session,redirect,url_for,g
from functools import wraps
import config

def login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if config.FRONT_USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('fromt.signin'))
    return inner