import pymysql


class MySQLCommand(object):
    def __init__(self, host, port, user, passwd, db, charset):
        self.host = host
        self.port = port
        self.user = user
        self.password = passwd
        self.db = db
        self.charset = charset

    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host,
                                        port=self.port,
                                        user=self.user,
                                        passwd=self.password,
                                        db=self.db,
                                        charset=self.charset)
            self.cursor = self.conn.cursor()
        except Exception as e:
            self.conn = None
            self.cursor = None
            print('connect mysql error.', e)

    def queryMysql(self, sql):
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchall()
            return row
        except Exception as e:
            print(e)
            print(sql)

    def insertMysql(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.cursor.rollback()
            print(e)
            print(sql)

    def closeMysql(self):
        self.cursor.close()
        self.conn.close()
