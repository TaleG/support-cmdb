#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from flask import request, jsonify, current_app
from flask_restful import Resource
from support import db
from support.models import Groups_Models
from support.utils import RET
from support.utils import SupResourceViews

class Groups_Views(Resource):
    """组视图"""
    def __init__(self):
        # 初始化数据库类，把Group库绑到SupResourceViews中。
        self.GroupDatabase = SupResourceViews(Groups_Models)


    # def get(self, id):
    #     """
    #     条件查询当前组有哪些用户
    #     :return:
    #     """
    #     try:
    #         UserGroupData = Users_Groups_Models.query.filter_by(id=id).all()
    #     except Exception as e:
    #         current_app.logger.error(e)
    #         return jsonify(code=RET.DBERR, codemsg="Database Error.")
    #     UserGroupList = []
    #     for UserGroupInfo in UserGroupData:
    #         UserGroupList.append(UserGroupInfo.to_json())
    #     return jsonify(code=RET.OK, codemsg="Succeed.", data=UserGroupList)


    def post(self):
        """
        添加数据
        :return:
        """
        req_data = request.get_json()
        try:
            Groups = Groups_Models(
                groupName=req_data.get("groupName"),
                groupDesc=req_data.get("groupDesc")
            )
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DATAERR, codemsg="Data Error.")
        # 调用utils.SupResource.SupAddData方法把数据添加到Mysql数据库中。
        self.GroupDatabase.SupAddData(Groups)

        return jsonify(code=RET.OK, codemsg="Succeed.")

    def put(self, id):
        """
        更新数据
        :param id:
        :return:
        """
        req_data = request.get_json()
        try:
            GroupsData = self.GroupDatabase.GetByIdData(id)

            GroupsData.groupName = req_data.get("groupName", GroupsData.groupName)
            GroupsData.groupDesc = req_data.get("groupDesc", GroupsData.groupDesc)

        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")

        # 调用utils.SupResource.SupAddData方法把数据添加到Mysql数据库中。
        self.GroupDatabase.SupAddData(GroupsData)

        return jsonify(code=RET.OK, codemsg="Succeed.")

    def delete(self, id):
        """
        删除数据
        :param id:
        :return:
        """
        # 调用utils.SupResource.SupDeleteData方法删除数据。
        return self.GroupDatabase.SupDeleteData(id)


class Groups_List_Views(Resource):
    """组视图"""
    def __init__(self):
        # 初始化数据库类，把Group库绑到SupResourceViews中。
        self.GroupDatabase = SupResourceViews(Groups_Models)

    def get(self, id):
        """
        单个详情信息查询
        :param id:
        :return:
        """
        # 调用utils.SupResource.SupGetById，按Id查找数据库数据
        return self.GroupDatabase.SupGetById(id)


    def post(self):
        """
        条件查询数据
        :return:
        """
        # 获取前端信息
        req_data = request.get_json()
        # 获取分页信息
        page_size = req_data.get("pageSize")
        currentPage = req_data.get("currentPage")
        # 获取条件查询数据
        groupName = req_data.get("groupName")

        # 判断groupName是否为空，不为空的话开始查询相应数据
        if groupName:

            # 条件查询数据，page_size为查询数据，page_index为查询条数
            GroupData = db.session.query(Groups_Models).filter(
                Groups_Models.groupName.like(groupName + "%")).all()

            # 调用utils.SupResource.PageData()方法进行,GroupData需要把查出来的数据传入
            PageData = self.GroupDatabase.ListData(GroupData)

            return jsonify(code=RET.OK, codemsg="Succeed.", data=PageData, total=len(PageData))

        else:
            # superTest = SupResourceViews(Groups_Models)
            # 传入页码和条数参数查出对应页的数据
            GroupData = self.GroupDatabase.GetPageData(page_size, currentPage)
            # 把数据放到ListData中格式化
            PageData = self.GroupDatabase.ListData(GroupData)
            # 统计数据库所有数据
            DataCount = self.GroupDatabase.CountData()
            return jsonify(code=RET.OK, codemsg="Success.", data=PageData, total=DataCount)

