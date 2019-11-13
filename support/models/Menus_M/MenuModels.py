#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from support import db

class Menu_Models(db.Model):
    """菜单栏"""
    __tablename__ = "support_menu"
    id = db.Column(db.Integer, primary_key=True)
    menuParentId = db.Column(db.Integer)
    menuName = db.Column(db.String(32), unique=True, nullable=False)
    Menu_List = db.relationship("Menu_Paren_Models", backref="support_menu", lazy="dynamic")


