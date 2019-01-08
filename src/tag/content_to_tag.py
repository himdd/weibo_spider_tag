#!/usr/bin/python
#  encoding: utf-8
from __future__ import unicode_literals

import jieba
import jieba.posseg
import jieba.analyse
import datetime
import re



import pymysql as mdb
import Queue
import sys
sys.path.append("..")
import threading
import time
import urllib2
import hashlib
import json
import logging
import urlparse

# 自定义包
from library.config import *
from library.util import *

exitFlag = 0
queueLock = threading.Lock()
workQueue = Queue.Queue(2000)

def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

class myThread (threading.Thread):
    def __init__(self, threadId, name, q):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.q = q

    def run(self):
        logger.info('starting thread' + self.name)
        processor(self.name, self.q)
        logger.info('exiting thread' + self.name)

def processor(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            logger.info('queue size:' + str(workQueue.qsize()))
            data = q.get()
            queueLock.release()
            processData(data)
        else:
            queueLock.release()

def processData(data):
    # print data
    video_id = data['id']
    page_id = data['source_id']
    source = data['site']

    try:
        sql = "SELECT content,author FROM `recommend_video_play_page` WHERE id=%s"
        queryData = (page_id)
        cur.execute(sql, queryData)
        content_results = cur.fetchall()
        logger.info('deal id: %s' % video_id)

        if len(content_results) == 0:
            return

        # user tag
        author = content_results[0][1]
        if len(author) != 0:
            sql = "SELECT id,`name` FROM `recommend_tags` " \
                  "WHERE `name` = '%s'" % author.decode('utf-8')
            cur.execute(sql)
            results_tag = cur.fetchall()
            # print results_tag
            if len(results_tag) == 0:
                sql = "insert into `recommend_tags`  (`name`) VALUES ('%s')" \
                      " ON DUPLICATE KEY UPDATE `name` = values(`name`)" % author.decode('utf-8')
                cur.execute(sql)
                tag_id = con.insert_id()
                sql = "insert into `recommend_categorys_tags`  (`category_id`,`tag_id`) VALUES (%d,%d)" \
                      " ON DUPLICATE KEY UPDATE category_id = values(category_id), tag_id=values(tag_id)"\
                      % (user_category_id, tag_id)
                cur.execute(sql)
                con.commit()

        content = content_results[0][0]
        content = content.decode('utf-8')
        reg = re.compile('<[^>]*>')
        content = reg.sub('', content).strip()
        if len(content) != 0:
            extract_results_origin = jieba.analyse.extract_tags(content, withWeight=True)
            extract_results = []
            for tag, weight in extract_results_origin:
                extract_results.append((tag.encode('utf-8'), weight))

            tags = ["'" + k.decode('utf-8') + "'" for k, v in extract_results]
            tag_str = ",".join(tags)
            sql = "SELECT id,`name` FROM `recommend_tags` " \
                "WHERE `name` in (" + tag_str + ")"
            cur.execute(sql)
            results_tags = cur.fetchall()
            # for rowt in results_tags:
            #    print rowt[0], rowt[1]

            tag_dict = {}
            for tag_id, name in results_tags:
                # print name
                tag_dict[name] = tag_id

            # insert into recommend_videos_tags
            sql_values = []
            for tag, weight in extract_results:
                if tag in tag_dict:
                    sql_values.append(" (%s,%s,%s) " % (video_id, tag_dict[tag], weight))
            if len(sql_values) > 0:
                sql = "insert into `recommend_videos_tags`  (`video_id`,`tag_id`,`weight`) VALUES " \
                      + ",".join(sql_values) + " ON DUPLICATE KEY UPDATE " \
                      + " video_id = values(video_id), tag_id=values(tag_id), weight = values(weight) "
                cur.execute(sql)
                con.commit()

        # 更新数据库
        now = time.time()
        x = time.localtime(now)
        updateAt = time.strftime('%Y-%m-%d %H:%M:%S', x)
        pageSql = "update recommend_new_videos set is_tag=%d,updated_at='%s' where id=%d" % (1, updateAt, video_id)
        cur.execute(pageSql)
        con.commit()
    except Exception as e:
        logger.info('exception:' + " " + e.message)
        # logger.info(e)

logging.basicConfig(
    level    = logging.DEBUG,
    format   = 'LINE %(lineno)-4d  %(levelname)-8s %(message)s',
    datefmt  = '%m-%d %H:%M',
    filename = "/Users/himdd/logs/dongqiudi-spider-video/content_to_tag.log",
    filemode = 'a');
logger = logging.getLogger(__name__)
logger.info('Start Main')

con = None
try:
    conf = getDBConf()
    if 0 == len(conf):
        logger.info('get conf error')
        sys.exit(1)
    con = mdb.connect(host=conf['host'], port=conf['port'], user=conf['user'], passwd=conf['password'], db=conf['default_db']);
    cur = con.cursor()
finally:
    logger.info('start main function')

SITE = "weibo"
user_category_id = 11

# 程序入口
def main():

    try:
        # 线程
        #threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6", "Thread-7", "Thread-8",
        #    "Thread-9", "Thread-10", "Thread-11", "Thread-12", "Thread-13", "Thread-14", "Thread-15", "Thread-16"]
        threadList = ["Thread-1"]
        threads = []
        threadId = 1
        # 创建新线程
        for tName in threadList:
            thread = myThread(threadId, tName, workQueue)
            thread.start()
            threads.append(thread)
            threadId += 1

        # 从mysql读数据填充队列
        sql = "SELECT id,source_id,source FROM `recommend_new_videos` WHERE is_tag=0 and source=%s and created_at>%s "

        now = time.time() - 7200
        x = time.localtime(now)
        created_at = time.strftime('%Y-%m-%d %H:%M:%S', x)
        queryData = (SITE, created_at)
        cur.execute(sql, queryData)
        results = cur.fetchall()
        logger.info('results number:' + str(len(results)))

        queueLock.acquire()
        for res in results:
            tmp = {}
            tmp['id'] = res[0]
            tmp['source_id'] = res[1]
            tmp['site'] = res[2]

            if not workQueue.full():
                workQueue.put(tmp)
        queueLock.release()

        # 等待队列清空
        while not workQueue.empty():
            pass

        # 通知线程是时候退出
        global exitFlag
        exitFlag = 1
        # 等待所有线程完成
        for t in threads:
            t.join()
        logger.info('exit main thread')
    finally:
        if con:
            con.close()            # 无论如何，连接记得关闭

if __name__ == "__main__":
    main()
