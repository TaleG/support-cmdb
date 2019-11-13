#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from flask import request, current_app, jsonify
from flask_restful import Resource
from support import db
from support.utils import RET
from support.models import Menu_Models, Paren_Model, Menu_Paren_Models


class Menu_Views(Resource):
    """子菜单"""
    def post(self):
        """
        添加子菜单信息
        :return:
        """
        req_data = request.get_json()

        try:
            MenuData = Menu_Models(
                menuName=req_data.get("menuName"),
            )
            db.session.add(MenuData)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")

        return jsonify(code=RET.OK, codemsg="Succeed.")

class Paren_Views(Resource):
    """主菜单"""
    def post(self):
        """
        添加主菜单
        :return:
        """
        req_data = request.get_json()

        try:
            MenuData = Paren_Model(
                paren_name=req_data.get("paren_name")
            )
            db.session.add(MenuData)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")

        return jsonify(code=RET.OK, codemsg="Succeed.")

class Paren_Menu_Views(Resource):
    """父菜单和子菜单关系"""
    def get(self):
        """
        菜单查找
        :return:
        """
        try:
            MenuParenData = Menu_Paren_Models.query.all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")

        MenuParenList = []
        for MenuParenInfo in MenuParenData:
            MenuParenList.append(MenuParenInfo.to_json())

        return jsonify(code=RET.OK, codemsg="Succeed", data=MenuParenList)