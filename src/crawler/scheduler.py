#!/usr/bin/python
#coding=utf-8

import json
from lxml import etree        # 导入xpath
#import MySQLdb as mdb
import pymysql as mdb
import re
import sys
sys.path.append("..")
import time
import logging

# 自定义包
from library.config import *
from library.util import *

reload(sys)
sys.setdefaultencoding('utf8')

def safeTrim(str):
    newStr = str.replace('赞[', '')
    newStr = newStr.replace('评论[', '')
    newStr = newStr.replace('转发[', '')
    newStr = newStr.replace('收藏', '')
    newStr = newStr.replace(']', '')
    return newStr

def modifyPub(publishAt):
    publishTime = publishAt.replace('weibo.com', '')
    arr = publishTime.split('来自')
    pt = arr[0]

    if "分钟前" in pt:
        pt = pt.replace('分钟前', '')
        now = time.time()
        try :
            pt = int(now) - int(pt) * 60
        finally :
            pt = int(now) - 20* 60
            x = time.localtime(pt)
            pt = time.strftime('%Y-%m-%d %H:%M:%S', x)

    if "今天" in pt:
        now = time.time()
        x = time.localtime(now)
        pt = pt.replace('今天', '')
        today = time.strftime('%Y-%m-%d', x)
        pt = today + " " + pt

    if "昨天" in pt:
        now = time.time() - 86400
        x = time.localtime(now)
        pt = pt.replace('昨天', '')
        today = time.strftime('%Y-%m-%d', x)
        pt = today + " " + pt
    pt = pt.replace('年', '-')
    pt = pt.replace('月', '-')
    pt = pt.replace('日', '')
    return pt

# 解析结构化信息
def getItems(url):
    items = {}
    html = getHtmlBYHeader(url)
    #print html
    selector = etree.HTML(html, parser=None, base_url=None)
    videoInfo = {}

    i = 1
    while i < 11:
        tmp = {}
        textList=selector.xpath('/html/body/div[@class="c"][' + str(i) + ']/div/span/a/text()')
        #print i,textList
        j = 1
        for text in textList:
            #print text
            flag = "视频"
            if flag in text:
                videoUrl=selector.xpath('//div[@class="c"]['+str(i)+']/div/span/a[' + str(j) + ']/@href')
                tmp['videoUrl'] = videoUrl[0]
                break
            j = j + 1
        if j > len(textList):
            i = i + 1
            continue
        up = selector.xpath('/html/body/div[@class="c"][' + str(i) + ']/div/a[1]/text()')
        share = selector.xpath('/html/body/div[@class="c"][' + str(i) + ']/div/a[2]/text()')
        comment = selector.xpath('/html/body/div[@class="c"][' + str(i) + ']/div/a[3]/text()')
        if 0 == len(up):
            upCount = 0
        else:
            upCount = safeTrim(up[0])
            if 0 == len(upCount):
                upCount = 0

        if 0 == len(share):
            shareCount = 0
        else:
            shareCount = safeTrim(share[0])
            if 0 == len(shareCount):
                shareCount = 0

        if 0 == len(comment):
            commentCount = 0
        else:
            commentCount = safeTrim(comment[0])
            if 0 == len(commentCount):
                commentCount = 0

        tmp['up'] = upCount
        tmp['share'] = shareCount
        tmp['comment'] = commentCount

        article=selector.xpath('/html/body/div[@class="c"][' + str(i) + ']/div/span[@class="ctt"]//text()')
        short = ""
        content = short.join(article)
        tmp['content'] = content
        publishAt=selector.xpath('/html/body/div[@class="c"][' + str(i) + ']/div/span[@class="ct"]/text()')
        if 0 == len(publishAt):
            pt = ""
        else:
            pt = modifyPub(publishAt[0])

        tmp['publish_time'] = pt
        tmp['view_count'] = 0
        items[i] = tmp
        i = i + 1
    return items

# 程序入口
def main():
    logging.basicConfig(
        level    = logging.DEBUG,
        format   = 'LINE %(lineno)-4d  %(levelname)-8s %(message)s',
        datefmt  = '%m/%d/%Y %I:%M:%S %p',
        filename = "/Users/himdd/logs/dongqiudi-spider-video/scheduler.log",
        filemode = 'w');
    logger = logging.getLogger(__name__)
    logger.info('Start Scheduler')

    while 1:
        now = time.time()
        x = time.localtime(now)
        updateAt = time.strftime('%Y-%m-%d %H:%M:%S', x)
        logger.info('loop at ' + str(updateAt))

        con = None
        try:
            conf = getDBConf()
            if 0 == len(conf):
                logger.info('get db conf fail')
                continue
            con = mdb.connect(host=conf['host'], port=conf['port'], user=conf['user'], passwd=conf['password'], db=conf['default_db'], charset="utf8");
            cur = con.cursor()

            sql = "select id, nick, user_id, hub_url, last_fetch_time, frequency from recommend_video_seed where site='weibo'"
            cur.execute(sql)
            results = cur.fetchall()
            if 0 == len(results):
                logger.info('get weibo seed empty')
                continue
            for res in results:
                seed_id = res[0]
                nick = res[1]
                user_id = res[2]
                hub_url = res[3]
                # 判断抓取历史和频率
                last_fetch_time = res[4]
                frequency = res[5]
                if last_fetch_time + frequency > now:
                    logger.info('skip:' + nick + " " + str(now) + " " + str(last_fetch_time) + " " + str(frequency))
                    continue
                # 抓取并解析
                #hub_url = "https://weibo.cn/1744957737/profile?filter=1&page=1"
                #hub_url = "https://weibo.cn/1744957737/profile?filter=1&page=1&display=0&retcode=6102"
                items = getItems(hub_url)
                for idx in items:
                    itm = items[idx]
                    videoSql = "insert into recommend_video_play_page (origin_page_url,site,seed_id,publish_time,author,content,view_count,up_count,share_count,comment_count) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE updated_at=%s"
                    data = (itm['videoUrl'], 'weibo', seed_id, itm['publish_time'], nick, itm['content'], itm['view_count'], itm['up'], itm['share'], itm['comment'], updateAt)
                    cur.execute(videoSql, data)
                    con.commit()
                # 更新抓取历史
                upSql = "update recommend_video_seed set last_fetch_time=%s where id=%s"
                upData = (now, seed_id)
                cur.execute(upSql, upData)
                con.commit()
        finally:
            if con:
                con.close()            # 无论如何，连接记得关闭
        time.sleep(300)

if __name__ == "__main__":
    main()
