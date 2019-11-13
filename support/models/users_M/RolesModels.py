#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from support import db

class Roles_Models(db.Model):
    """权限表"""
    __tablename__ = "support_roles"
    id = db.Column(db.Integer, primary_key=True)
    roleName = db.Column(db.String(32), unique=True, nullable=False)
    roleDesc = db.Column(db.String(128))

    def to_json(self):
        json_data = {
            "id": self.id,
            "roleName": self.roleName,
            "roleDesc": self.roleDesc
        }
        return json_data