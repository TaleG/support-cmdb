#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from support import db
from .MenuModels import Menu_Models
from .ParenModels import Paren_Model

class Menu_Paren_Models(db.Model):
    """父和子菜单关系"""
    __tablename__ = "support_Menu_Paren"

    id = db.Column(db.Integer, primary_key=True)
    ParenId = db.Column(db.ForeignKey(Paren_Model.id))
    MenuId = db.Column(db.ForeignKey(Menu_Models.id))

    def Menu_Info(self):
        """
        判断是否为空
        :return:
        """
        try:
            menuName = self.support_menu.menuName
        except Exception:
            menuName = None
        return menuName

    def to_json(self):
        json_data = {
            "id": self.id,
            "ParenName": self.support_paren.paren_name,
            "MenuName": self.Menu_Info()
        }
        return json_data