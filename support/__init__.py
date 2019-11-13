#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import redis
import logging
import time
from flask import Flask
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy

from config import Config_Map

####### 错误日志 #########
# logging.error("")   # 错误级别
# logging.warning("") #告警级别
# logging.info("")    #消息提示级别
# logging.debug("")   #调试级别

# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG) #调用debug级

# 设置日志时间：setTime获取时间格式：time.struct_time(tm_year=2016, tm_mon=4, tm_mday=7, tm_hour=10, tm_min=28, tm_sec=49, tm_wday=3, tm_yday=98, tm_isdst=0)
setTime = time.localtime(time.time())
filename = "Support_Server_%s_%s_%s.log" % (setTime.tm_year, setTime.tm_mon, setTime.tm_mday)
# 创建日志记录器，指明日志保存路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/%s" % filename, maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式、日志等级、输入日志信息的文件名行数、日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_log_handler)


# 创始redis连接对象
redis_store = None

# Mysql数据库
db = SQLAlchemy()


def Create_app(Config_name):
    """
    创建Flask的应用对像
    :param Config_name: str 配置模式的名字 {"develop", "product", "test"}
    :return:
    """
    app = Flask(__name__)


    # 根据配置模式的名字获取配置参数的类
    config_class = Config_Map.get(Config_name)
    app.config.from_object(config_class)


    # 初始化redis工具
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT,
                                    password=config_class.REDIS_PASS)

    # 使用app初始化DB
    db.init_app(app)

    # 注册蓝图
    from support import API_1_0
    app.register_blueprint(API_1_0.api_bp, url_prefix="/api/v1.0")

    return app
