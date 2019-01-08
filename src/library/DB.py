# coding=utf-8

import pymysql


class DB:
    db = None
    #DB_HOST = "10.19.117.230"
    #DB_PORT = "3306"
    #DB_USERNAME = "dongqiudi"
    #DB_PASSWORD = "wfnF6fuUNHjj3w"
    #DB_DATABASE = "dqd_dedecms"

    def __init__(self, *args, **kwargs):
        self.connect(*args, **kwargs)

    def connect(self, *args, **kwargs):
        # 打开数据库连接
        if self.db is None:
            try:

                self.db = pymysql.connect(*args, **kwargs)
            except Exception as e:
                print('connect error', e)

        return self.db

    def update(self, sql):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            return True
        except Exception as e:
            # Rollback in case there is any error
            print('update error:', sql, e)
            self.db.rollback()
            return False

    def query(self, sql):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            return results
        except Exception as e:
            print('query error:', e)
            return False

    def close(self):
        if self.db is not None:
            self.db.close()

    def __del__(self):
        self.close()
