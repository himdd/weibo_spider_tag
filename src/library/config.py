#!/usr/bin/python
#coding=utf-8
import os
import ConfigParser			# 读配置文件

# 配置文件统一放到conf目录下面
currDir = os.path.dirname(os.path.realpath(__file__))
configFile = currDir + os.sep + "../../conf/config.ini"
cf = ConfigParser.ConfigParser()
cf.readfp(open(configFile))

# 读取配置
def getSections():
	conf = {}
	secs = cf.sections()					# sections
	return secs

def getOptions(section):
	options = cf.options(section)			# options
	if 'host' not in options or  \
		'port' not in options or \
		'user' not in options or \
		'password' not in options or \
		'default_db' not in options:
		return {}
	return options

def getItems(section):
	items = cf.items(section)				# conf kv items
	return items

# 读取配置文件
def getDBConf(db='db'):
    secs = getSections()
    if db not in secs:
        print "config not inclue db conf"
        return {}
    opts = getOptions(db)
    if 0 == len(opts):
        print "lack options config"
        return {}

    conf = {}
    conf['host'] = cf.get(db, 'host')       #  values
    conf['port'] = cf.getint(db, 'port')
    conf['user'] = cf.get(db, 'user')
    conf['password'] = cf.get(db, 'password')
    conf['default_db'] = cf.get(db, 'default_db')
    return conf
