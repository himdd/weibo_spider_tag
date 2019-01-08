#!/usr/bin/python
#coding=utf-8

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
            processGetUrlAndUpdataData(data)
        else:
            queueLock.release()

def processGetUrlAndUpdataData(data):
    id = data['id']
    origin_page_url = data['origin_page_url']
    source = data['site']
    source_id = id
    query = urlparse.urlparse(origin_page_url).query
    kvDict = dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])
    # print kvDict
    if "object_id" not in kvDict:
        return

    # print html
    json_data_url = "https://m.weibo.cn/s/video/object?object_id=%s" % (kvDict['object_id'])
    # print json_data_url

    json_data = getHtmlBYHeader(json_data_url)
    #print json_data
    json_dict = json.loads(json_data)
    stream_dict = json_dict["data"]['object']['stream']
    image_dict = json_dict["data"]['object']['image']
    origin_video_url = stream_dict['url']
    duration = stream_dict['duration']
    width = stream_dict['width']
    height = stream_dict['height']
    format = stream_dict['format']
    mime = 'video/'+format

    origin_image_url = image_dict['url']

    #print origin_video_url
    #print origin_image_url
    hash_id = get_md5_value(origin_page_url)

    # 下载视频
    if 0 == len(origin_video_url):
        # af_video_url = origin_video_url
        return
    # af_video_url="http://tbapi.ixiaochuan.cn/urlresolver/tbvideo/vid/ce55-bc11-11e7-92c0-00163e02acff?pid=34770329&imgid=170654362&cb=zyvd%2F66%2Fb6%2Fce55-bc11-11e7-92c0-00163e02acff"

    try:
        f = urllib2.urlopen(origin_video_url, timeout=1000)
        videoContent = f.read()
        #print origin_video_url
        video_size = len(videoContent)
        #print video_size
        key = get_md5_value(origin_video_url)

        # 上传视频
        requrl = ""
        request = urllib2.Request(requrl, videoContent)
        request.add_header('Content-Length', '%d' % len(videoContent))
        request.add_header('Content-Type', 'application/octet-stream')
        res_data = urllib2.urlopen(request)
        res = res_data.read()
        if 0 == len(res):
            logger.info('upload video fail' + origin_video_url)
            return

        obj = json.loads(res)
        dqd_video_url = obj['data']

        if 0 == len(dqd_video_url):
            logger.info('upload video fail no url,' + origin_video_url)
            return

        # 上传图片
        if 0 == len(origin_image_url):
            # af_thumb_url = origin_thumb_url
            return
        requrl = ""
        req = urllib2.Request(requrl, origin_image_url)
        #print requrl
        res_data = urllib2.urlopen(req)
        ret = res_data.read()
        if 0 == len(ret):
            logger.info('upload image fail,' + origin_image_url)
        else:
            obj = json.loads(ret)
            dqd_image_url = obj['data']

        # 更新数据库
        now = time.time()
        x = time.localtime(now)
        updateAt = time.strftime('%Y-%m-%d %H:%M:%S', x)

        infoSql = "insert into recommend_new_videos (hash_id,url,duration,width,height,`size`,mime,image,source," \
                  "source_id,source_key) values ('%s','%s',%d,%d,%d,%d,'%s','%s','%s',%d,'%s') " \
                  "ON DUPLICATE KEY UPDATE hash_id=values(hash_id),url=values(url),duration=values(duration)," \
                  "width=values(width), height=values(height), `size`=values(`size`), mime=values(mime)," \
                  "image=values(image),source=values(source), source_id=values(source_id)," \
                  "source_key=values(source_key)" % (hash_id, dqd_video_url, duration, width, height, video_size,
                                                     mime, dqd_image_url, source, source_id, dqd_video_url)
        #print infoSql
        cur.execute(infoSql)

        pageSql = "update recommend_video_play_page set video_downloaded=%d,updated_at='%s' where id=%d" % (1, updateAt, id)
        #print pageSql
        cur.execute(pageSql)
        con.commit()
    except Exception as e:
        logger.info('download exception' + origin_page_url + " " + e.message)
        # logger.info(e)

logging.basicConfig(
    level    = logging.DEBUG,
    format   = 'LINE %(lineno)-4d  %(levelname)-8s %(message)s',
    datefmt  = '%m-%d %H:%M',
    filename = "/Users/himdd/logs/dongqiudi-spider-video/upload.log",
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

# 程序入口
def main():
    try:
        # 线程
        threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6", "Thread-7", "Thread-8",
            "Thread-9", "Thread-10", "Thread-11", "Thread-12", "Thread-13", "Thread-14", "Thread-15", "Thread-16"]
        #threadList = ["Thread-1"]
        threads = []
        threadId = 1
        # 创建新线程
        for tName in threadList:
            thread = myThread(threadId, tName, workQueue)
            thread.start()
            threads.append(thread)
            threadId += 1

        # 从mysql读数据填充队列
        sql = "select id,origin_page_url,site from recommend_video_play_page where video_downloaded=0 " \
              "and site='weibo' and created_at>%s "

        now = time.time() - 7200
        x = time.localtime(now)
        createdAt = time.strftime('%Y-%m-%d %H:%M:%S', x)
        queryData = (createdAt)
        cur.execute(sql, queryData)
        results = cur.fetchall()
        logger.info('results number:' + str(len(results)))

        queueLock.acquire()
        for res in results:
            tmp = {}
            tmp['id'] = res[0]
            tmp['origin_page_url'] = res[1]
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
