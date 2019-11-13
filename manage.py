#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from support import Create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS

# 以什么模式启动
app = Create_app("develop")

# 通过CORS验证
CORS(app)

manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
