#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from support import db

class Permission_Models(db.Model):
    """权限模版"""

    __tablename__ = "support_permission"
    id = db.Column(db.Integer, primary_key=True)
    perName = db.Column(db.String(32), unique=True, nullable=False)
    perDesc = db.Column(db.String(128))

    def to_json(self):
        json_data = {
            "id": self.id,
            "perName": self.perName,
            "perDesc": self.perDesc
        }
        return json_data