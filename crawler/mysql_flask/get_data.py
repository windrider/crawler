import requests
from fake_useragent import UserAgent
from config import db, host, port, user, passwd, charset
from db import MySQLCommand 
import datetime




def get_data():
    rank_api = 'http://api.bilibili.com/x/web-interface/ranking'
    headers = {"User-Agent": UserAgent(verify_ssl=False).random}
    from_data={}
    response_comment = requests.get(rank_api, headers=headers, data=from_data)
    comment_json = response_comment.json()
    return comment_json

def insert(line,thisrank):
    database.connectMysql()
    nowtime=datetime.datetime.now().strftime('%Y-%m-%d')
    sql = 'INSERT INTO bilibili.myrank12 ' \
          '(title, author, aid, bvid, coins, play, video_review,ranking,date) ' \
          'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}","{}","{}");'.format(line["title"],
                                                                      line["author"],
                                                                      line["aid"],
                                                                      line["bvid"],
                                                                      int(line["coins"]),
                                                                      int(line["play"]),
                                                                      int(line["video_review"]),
                                                                      int(thisrank),
                                                                      nowtime)
    database.insertMysql(sql)
    database.closeMysql()


if __name__ == '__main__':
    database = MySQLCommand(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    data_json = get_data()
    thisrank=0
    rows = data_json['data']['list']
    for row in rows:
        print(row)
        #print(row["title"].encode('string-escape'))
        temp=row["title"]
        temp=temp.replace('\"','\\\"')
        print(temp)
        row["title"]=temp
        thisrank=thisrank+1
        insert(row,thisrank)
    database.closeMysql()
