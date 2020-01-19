#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import redis


class Config(object):
    """Flask配置信息"""
    SECRET_KEY = "6difejo#)+bg6ccmt%%_qmt_(go8+v1u*zoz(1u53qgia^t=%y"

    # 连接数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/support_server"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 数据库慢查询记录阀值
    SLOW_DB_QUERY_TIME = 10000
    # 开启自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 记录查询
    SQLALCHEMY_RECORD_QUERIES = True

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_PASS = '123456'

    # flask-session配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS)
    SESSION_USE_SIGNER = True  # 对cookie中的session进行隐藏
    PERMANENT_SESSION_LIFETIME = 1  # 设置session数据有效期，单位是秒


class DevelopmentConfig(Config):
    """开发者模式配置信息"""
    DEBUG = True

class ProductionConfig(Config):
    """生产模式配置信息"""
    pass

class TestingConfig(Config):
    """测试模式配置信息"""
    TESTING = True

Config_Map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig,
    "test": TestingConfig,
}
