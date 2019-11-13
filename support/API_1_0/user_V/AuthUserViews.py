#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from flask import current_app, request, jsonify, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from support.models import Users_Models
from support.utils import RET, LOGIN_ERROR_MAX_TIMES, LOGIN_ERROR_FORBID_TIME
from support import redis_store

class Auth_Users_Views(Resource):
    """用户登录认证"""
    def post(self):
        """
        用户认证
        :return:
        """

        # 获取前端传参
        req_data = request.get_json()
        username = req_data.get("username")
        password = req_data.get("password")

        # 判断数据是否为空
        if not all([username, password]):
            return jsonify(code=RET.NODATA, codemsg="Username or Passowrd is None.")

        try:
            # 按用户查找数据是否存在
            User_Data = Users_Models.query.filter_by(username=username).first()
            token = Users_Models.generate_auth_token(User_Data)
        except (IntegrityError, AttributeError) as e:
            current_app.logger.error(e)
            return jsonify(code=RET.NODATA, codemsg="User Data No Exist.")

        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")

        try:
            # 从redis获取用户错误次数
            Access_Nums = redis_store.get("access_login_error_number_%s" % username)
        except Exception as e:
            current_app.logger.error(e)
        else:
            # 判断redis访问错误是否为空或是否大于限制。
            if Access_Nums is not None and int(Access_Nums) >= LOGIN_ERROR_MAX_TIMES:
                return jsonify(code=RET.REQERR, codemsg="Login errors are excessive.")

        # 判断用户是否存在或密码是否正确。
        if User_Data is None or not User_Data.check_password(password):
            try:
                # 如果检测失败则保存信息到redis中，expire设置错误信息有效期
                redis_store.incr("access_login_error_number_%s" % username)
                redis_store.expire("access_login_error_number_%s" % username, LOGIN_ERROR_FORBID_TIME)
            except Exception as e:
                current_app.logger.error(e)
            return jsonify(code=RET.DATAERR, codemsg="User or Password Auth Error.")

        return jsonify(code=RET.OK, codemsg="Succeed.", token=token)

    def delete(self):
        """
        退出系统
        :return:
        """
        session.clear()
        return jsonify(code=RET.OK, codemsg="Succeed.")
