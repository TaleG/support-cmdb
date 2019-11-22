#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import join
import uuid
from flask import current_app, request, jsonify, g
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from support import db
from support.utils import RET, login_required
from support.models import Users_Models
from support.utils import SupResourceViews

class Users_Views(Resource):
    """用户视图"""
    @login_required
    def get(self):
        """
        查询用户信息
        :return:
        """
        id = g.data["id"]
        try:
            userData = Users_Models.query.filter_by(id=id).first()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")
        try:
            User_Info = userData.to_json()

        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.NODATA, codemsg="Select is None.")
        return jsonify(code=RET.OK, codemsg="Succeed.", data=User_Info)

    def post(self):
        """
        添加用户
        :return:
        """
        # 获取前端返回的数据
        req_data = request.get_json()
        username = req_data.get("username")
        password = req_data.get("password")

        suid = str(uuid.uuid4())

        try:
            # 把数据和数据库字段组起来。
            User_Data = Users_Models(
                username=username,
                userPhone=req_data.get("userPhone"),
                userEmail=req_data.get("userEmail"),
                userRole=req_data.get("userRole"),
                uuid=''.join(suid.split("-")),
                userLoginIp=request.remote_addr,    # 获取登录IP
                userDesc=req_data.get("userDesc")
            )
            # 在用户model中配置了用户是否填有名字，如果没有系统会随机创建一个。
            User_Data.name_info = req_data.get("name")
            # 在用户model中创建了hash加密，所有创建的密码都会做成加密。
            User_Data.password_hash = password
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DATAERR, codemsg="Data Error.")
        try:
            # 把数据提添加到数据库
            db.session.add(User_Data)
            # 把添加的数据库提交到数据库
            db.session.commit()
        except IntegrityError as e:
            # 提交数据库如果有问题操作回退
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DATAEXIST, codemsg="Data Exist.")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")

        return jsonify(code=RET.OK, codemsg="Succeed.")

    def put(self, id):
        """
        修改用户信息
        :param id:
        :return:
        """
        req_data = request.get_json()
        try:
            UserData = Users_Models.query.filter_by(id=id).first()

            UserData.name = req_data.get("name", UserData.name)
            UserData.username = req_data.get("username", UserData.username)
            UserData.userRole = req_data.get("userRole", UserData.userRole)
            UserData.userEmail = req_data.get("userEmail", UserData.userEmail)
            UserData.userPhone = req_data.get("userPhone", UserData.userPhone)
            UserData.userDesc = req_data.get("userDesc", UserData.userDesc)

            # 在用户model中创建了hash加密，所有创建的密码都会做成加密。
            UserData.password_hash = req_data.get("password", UserData.password)

            db.session.add(UserData)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")

        return jsonify(code=RET.OK, codemsg="Succeed.")

    def delete(self, id):
        """
        删除数据
        :param id:
        :return:
        """
        try:
            UserData = Users_Models.query.filter_by(id=id).first()

            db.session.delete(UserData)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error")

        return jsonify(code=RET.OK, codemsg="Succeed.")

class Users_List_Views(Resource):
    """用户视图"""

    def get(self, id):
        """
        查询用户信息
        :return:
        """
        try:
            userData = Users_Models.query.filter_by(id=id).first()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")
        try:
            User_Info = userData.to_json()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.NODATA, codemsg="Select is None.")
        return jsonify(code=RET.OK, codemsg="Succeed.", data=User_Info)

    def post(self):
        """
        备件查询
        :return:
        """
        req_data = request.get_json()
        page_size = req_data.get("pageSize")
        currentPage = req_data.get("currentPage")
        username = req_data.get("searchMap")

        userList = []

        if username:

            # UserData = Users_Models.query.filter_by(username=searchMap).all()
            # 模糊查询username数据
            UserData = db.session.query(Users_Models).filter(or_(Users_Models.username.like(username + "%"))).all()
            for UserInfo in UserData:
                userList.append(UserInfo.to_json())

            return jsonify(code=RET.OK, codemsg="Succeed.", data=userList, total=len(userList))
        else:
            try:
                userCount = Users_Models.query.count()
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(code=RET.DBERR, codemsg="Database Error.")
            try:
                userData = Users_Models.query.limit(page_size).offset((currentPage - 1) * page_size)
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(code=RET.DBERR, codemsg="Database Error.")

            for userInfo in userData:
                userList.append(userInfo.to_json())

            return jsonify(code=RET.OK, codemsg="Succeed.", data=userList, total=userCount)

class ResetPassword(Resource):
    """修改密码"""
    def __init__(self):
        self.UserData = SupResourceViews(Users_Models)

    def put(self):
        """
        修改密码
        :return:
        """
        pass
