#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from flask import current_app, jsonify, request
from flask_restful import Resource
from sqlalchemy import and_
from sqlalchemy.orm.exc import UnmappedInstanceError
from support import db
from support.models import Users_Groups_Models, Users_Models
from support.utils import RET, SupResourceViews

class Group_User_List_Views(Resource):
    """用户和组关系"""
    def __init__(self):
        # 初始化user和group关系库
        self.GroupUserDatabase = SupResourceViews(Users_Groups_Models)
        # 初始化User库，为穿梭窗功能使用
        self.UserDatabase = SupResourceViews(Users_Models)
        # 把查询数据做列表初始化。
        self.ListLink = []

    def get(self, id):
        """
        用户信息查找
        :return:
        """
        try:
            # 按groupId查询User_Groups_Models库数据，因为Groupid为固定参数，所以不能继承自定义库类。
            LinkData = db.session.query(Users_Groups_Models).filter_by(groupId=id).all()
        except Exception as e:
            # 查询出来的时候出现异常不需要做什么返回
            current_app.logger.error(e)
            return False

        for UserInfo in LinkData:
            # 此处只为了遍历查询出来的数据，LinkData中以字典返回。
            # 只要他的key字段数据就行，此处key为userId，是为了查出组内的所有用户信息。
            # 放到穿梭窗已选位。
            self.ListLink.append(UserInfo.to_json()['key'])

        try:
            # 查出所有用户信息
            # 此处只为了拉取所有用户信息，只放到穿梭窗左边待选位。
            UserData = db.session.query(Users_Models).all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")

        # 用片定义的初始化继承，调用ListLinkData()方法把查询数据初始化。
        ListDataInfo = self.UserDatabase.ListLinkData(UserData)

        return jsonify(code=RET.OK, codemsg="Success.", LinkData=self.ListLink, UserData=ListDataInfo)

    def post(self, id):
        """
        穿梭框添加（左向右移）
        :return:
        """
        req_data = request.get_json()
        # 前端返回偏移选中数据，此处为添加组中的所属用户。
        movedKeys = req_data.get('movedKeys')

        for i in movedKeys:
            try:
                # 按groupId和userId条件查询数据数据。
                # 此处为了判断数据是否存在。
                UserGroupData = db.session.query(Users_Groups_Models).filter(and_(
                    Users_Groups_Models.groupId == id,
                    Users_Groups_Models.userId == i)).all()
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(code=RET.DBERR, codemsg="Database Error.")
            # 遍历条件查询数据（此处不确定因素）
            for UserGroupInfo in UserGroupData:
                UserGroupInfo.to_json()

            # 把遍历查询出来的数据放到库中
            UserLinkData = Users_Groups_Models(
                groupId=id,
                userId=i
            )
            # 此处调用自定义数据库方法继承，把放到数据库中的数据提交到数据库。
            self.GroupUserDatabase.SupAddData(UserLinkData)

        return jsonify(code=RET.OK, codemsg="Succeed.")

    def delete(self, id):
        """
        穿梭框删除（右向左移）
        :param id:
        :return:
        """
        req_data = request.get_json()
        # 接收前端传来数据
        movedKeys = req_data.get('movedKeys')
        for i in movedKeys:
            try:
                # 条件查询数据
                GroupData = db.session.query(Users_Groups_Models).filter(and_(
                    Users_Groups_Models.groupId == id,
                    Users_Groups_Models.userId == i)).first()
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(code=RET.DBERR, codemsg="Database Error.")
            # 操作删除方法把查出来的数据删除。
            try:
                db.session.delete(GroupData)
                db.session.commit()
            except UnmappedInstanceError:
                # 此处为偏移操作，UnmappedInstanceError为是否存在。此处不做返回处理
                pass

        return jsonify(code=RET.OK, codemsg="Succeed.")
