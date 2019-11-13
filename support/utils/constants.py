#!/usr/bin/env python
#_*_ coding:utf-8 _*_

# 登录错误最大次数
LOGIN_ERROR_MAX_TIMES = 5

# 登录错误限制的时间， 单位：秒
LOGIN_ERROR_FORBID_TIME = 300

# 查询缓存时间, 单位：秒
AREA_INFO_REDIS_CACHE_EXPIRES = 7200

# 有效期保留时间，单位：秒
VALID_DATE_REDIS_CACHE_EXPIRES = 86400