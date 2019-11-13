#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from flask import current_app, jsonify, request
from flask_restful import Resource
from support import db
from support.models import Users_Groups_Models

class Group_User_Views(Resource):
    """用户和组关系"""
    def get(self):
        """
        用户信息查找
        :return:
        """