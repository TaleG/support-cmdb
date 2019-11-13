#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from support import db

class Groups_Models(db.Model):
    """用户组"""
    __tablename__ = "support_groups"

    id = db.Column(db.Integer, primary_key=True)
    groupName = db.Column(db.String(32), unique=True, nullable=False)
    groupDesc = db.Column(db.String(128))
    groupList = db.relationship("Users_Groups_Models", backref="support_groups", lazy="dynamic")

    def to_json(self):
        json_data = {
            "id": self.id,
            "groupName": self.groupName,
            "groupDesc": self.groupDesc
        }
        return json_data
