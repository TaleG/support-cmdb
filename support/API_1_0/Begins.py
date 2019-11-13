#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from flask import jsonify
from flask_restful import Resource
from support.utils import RET
from support.models import *

class Begins_Views(Resource):
    def get(self):
        """
        Test Page
        :return:
        """
        return jsonify(code=RET.OK, codemsg="Welcome to Begin Page.")