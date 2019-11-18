#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from flask import current_app, jsonify, request
from flask_restful import Resource
from support import db
from support.models import Users_Groups_Models, Users_Models
from support.utils import RET, SupResourceViews

class Group_User_List_Views(Resource):
    """用户和组关系"""
    def __init__(self):
        self.GroupUserDatabase = SupResourceViews(Users_Groups_Models)
        self.UserDatabase = SupResourceViews(Users_Models)

    def get(self, id):
        """
        用户信息查找
        :return:
        """
        # AllData = self.GroupUserDatabase.GetByIdData(id)
        # GroupUserData = self.GroupUserDatabase.ListData(AllData)

        LinkList = []
        try:
            LinkData = db.session.query(Users_Groups_Models).filter_by(groupId=id).all()
        except Exception as e:
            current_app.logger.error(e)
            return

        for UserInfo in LinkData:
            LinkList.append(UserInfo.to_json()['key'])

        try:
            UserData = db.session.query(Users_Models).all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")

        UserDataInfo = self.UserDatabase.ListLinkData(UserData)

        return jsonify(code=RET.OK, codemsg="Success.", LinkData=LinkList, UserData=UserDataInfo)

    def post(self):
        """

        :return:
        """
        resp = request.get_json()
        print(resp.get('linkData'))