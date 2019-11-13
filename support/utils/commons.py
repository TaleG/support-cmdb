#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from functools import wraps
from flask import jsonify, g, request, current_app
from .response_code import RET

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

def login_required(view_func):
    """
    用户登录检测装饰器
    :param view_func:
    :return:
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        try:
            tokens = request.headers["X-CSRFToken"]
        except Exception:
            return jsonify(code=RET.SESSIONERR, codemsg="Http RespError")
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            g.data = s.loads(tokens)
            return view_func(*args, **kwargs)

        except SignatureExpired:
            return jsonify(code=RET.SESSIONERR, codemsg="Session Signature Error")
        except BadSignature:
            return jsonify(code=RET.SESSIONERR, codemsg="Session BadSignatury Error.")
    return wrapper