#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from support import db
from .UserModels import Users_Models
from .GroupsModels import Groups_Models

class Users_Groups_Models(db.Model):
    __tablename__ = "users_groups"

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.ForeignKey(Users_Models.id))
    groupId = db.Column(db.ForeignKey(Groups_Models.id))

    def to_json(self):
        json_data = {
            "id": self.id,
            "key": self.userId,
            "label": self.support_users.name,
            "disabled": False,
            "groupId": self.groupId,
        }
        return json_data
