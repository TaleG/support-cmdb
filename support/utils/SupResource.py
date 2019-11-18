#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from flask import jsonify, current_app
from sqlalchemy.exc import InterfaceError
from support import db
from support.utils import RET

class SupSqlalchemyTools(object):
    """数据库操作"""
    def __init__(self, Database):
        self.Database = Database

    def CountData(self):
        """
        计算数据总数量
        :return:
        """
        try:
            Count = db.session.query(self.Database).count()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")
        return Count

    def GetByIdData(self, id):
        """
        按Id操作查（单条）数据库
        :param id:
        :return:
        """
        try:
            Data = db.session.query(self.Database).filter_by(id=id).first()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")
        return Data

    def GetTotalData(self, id):
        """
        按Id操作查（所有）关系数据
        :param id:
        :return:
        """
        try:
            Data = db.session.query(self.Database).filter_by(id=id).all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")
        return Data

    def GetAllData(self):
        """
        查看数据库所有数据
        :return:
        """
        try:
            Data = db.session.query(self.Database).all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")
        return Data

    def GetPageData(self, pageSize, currentPage):
        """

        :param pageSize:
        :param currentPage:
        :return:
        """
        try:
            Data = db.session.query(self.Database).limit(pageSize).offset((currentPage - 1) * pageSize)

        except Exception as e:
            current_app.logger.error(e)
            return
        return Data


class SupResourceViews(SupSqlalchemyTools):
    """把Resource封装到一个统一类中"""
    def __init__(self, Database):
        super(SupResourceViews, self).__init__(Database)
        self.Database = Database
        self.DataList = []

    def ListData(self, SupData):
        """
        初始化数据把数据放到列表中
        :param SupData:
        :return:
        """
        for DataInfo in SupData:
            self.DataList.append(DataInfo.to_json())
        return self.DataList

    def ListLinkData(self, SupData):
        """
        初始化数据把数据放到列表中
        :param SupData:
        :return:
        """
        for DataInfo in SupData:
            self.DataList.append(DataInfo.to_link_json())
        return self.DataList

    def SupGetById(self, id):
        """
        查找数据库单条数据
        :param id:
        :return:
        """
        try:
            Data = db.session.query(self.Database).filter_by(id=id).first()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")
        try:
            DataInfo = Data.to_json()
        except AttributeError as e:
            current_app.logger.error(e)
            return jsonify(code=RET.NODATA, codemsg="Data No Exist.")

        return jsonify(code=RET.OK, codemsg="Succeed.", data=DataInfo)

    def SupGetTotal(self, id):
        """
        查找关系对应的数据
        :param id:
        :return:
        """
        try:
            Data = db.session.query(self.Database).filter_by(id=id).all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")

        for DataInfo in Data:
            self.DataList.append(DataInfo.to_json())
        return jsonify(code=RET.OK, codemsg="Succeed.", data=self.DataList)

    def SupAddData(self, SupData):
        """
        添加数据，做数据添加和修改操作。
        :param SupData:
        :return:
        """
        try:
            db.session.add(SupData)
            db.session.commit()
        except InterfaceError as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DATAEXIST, codemsg="Data Exist.")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")
        return jsonify(code=RET.OK, codemsg="Succeed.")

    def SupDeleteData(self, id):
        """
        做数据删除，需要传入数据ID
        :param id:
        :return:
        """
        try:
            GroupsData = db.session.query(self.Database).filter_by(id=id).first()

            db.session.delete(GroupsData)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, codemsg="Database Error.")
        return jsonify(code=RET.OK, codemsg="Succeed.")