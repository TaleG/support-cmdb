#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from flask import Blueprint
from flask_restful import Api


from . import Begins, user_V, menu_V

api_bp = Blueprint("api_1_0", __name__)
api = Api(api_bp)

# 测试
api.add_resource(Begins.Begins_Views, '/begin', endpoint='begin')

# 用户验证
api.add_resource(user_V.Auth_Users_Views, '/userauth', endpoint='userauth')

# 用户
api.add_resource(user_V.Users_List_Views, '/user_list', '/user_list/<int:id>', endpoint="user_list")
api.add_resource(user_V.Users_Views, '/users', '/users/<int:id>', endpoint='users')

# 组
api.add_resource(user_V.Groups_List_Views, '/group_list', '/group_list/<int:id>', endpoint='group_list')
api.add_resource(user_V.Groups_Views, "/groups", "/groups/<int:id>", endpoint="groups")

# 菜单
api.add_resource(menu_V.Menu_Views, '/menu', endpoint='menu')
api.add_resource(menu_V.Paren_Views, '/paren', endpoint='paren')
api.add_resource(menu_V.Paren_Menu_Views, '/parenmenu', endpoint='parenmenu')