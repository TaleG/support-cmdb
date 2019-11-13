#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from support import db


class Paren_Model(db.Model):
    """父菜单"""
    __tablename__ = "support_paren"

    id = db.Column(db.Integer, primary_key=True)
    paren_name = db.Column(db.String(32), unique=True, nullable=False)
    Paren_List = db.relationship(
        "Menu_Paren_Models",
        backref="support_paren",
        lazy="dynamic")