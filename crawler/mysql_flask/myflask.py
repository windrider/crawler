from flask import Flask
from flask import Flask,send_from_directory
from flask import request
from flask_cors import *  # 导入模块
from datetime import timedelta
from config import db, host, port, user, passwd, charset
from db import MySQLCommand
import datetime
import urllib
import os



datapath = './'
date='2020-06-14'
pngdict='E:\\sbz\\Documents\\homework3\\mysql_flask\\img\\'

app= Flask(__name__)
app.config['JSON_AS_ASCII']=False
app.debug=True
CORS(app, supports_credentials=True)  # 设置跨域
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/coins_play')
@cross_origin()
def coins_play():
    pname='coins_play_'+date+'.png'
    print(pname)
    return send_from_directory(pngdict,filename=pname,as_attachment=True)

@app.route('/api/coins_review')
@cross_origin()
def coins_review():
    pname='coins_review_'+date+'.png'
    print(pname)
    return send_from_directory(pngdict,filename=pname,as_attachment=True)

@app.route('/api/play_review')
@cross_origin()
def review_play():
    pname='play_review_'+date+'.png'
    print(pname)
    return send_from_directory(pngdict,filename=pname,as_attachment=True)

@app.route('/api/changedt',methods=['GET','POST'])
def changedt():
    if request.method=='POST':
        tempdata=request.data
        tempdata=eval(tempdata)
        global date
        date=tempdata['dt']
        database = MySQLCommand(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        database.connectMysql()
        sql = 'SELECT title,  ranking, date FROM bilibili.myrank12 order by ranking asc;'
        result = database.queryMysql(sql)
        count=0
        idx=0
        retdata=[]
        while True:
            if result[idx][2]==date:
                count=count+1
                retdata.append({'title':result[idx][0],'count':count})
            if count==10:
                break
            idx=idx+1
        print(retdata)
        database.closeMysql()
        print(date)
        return{
            'titles':retdata
        }

@app.route('/api/datelist',methods=['GET','POST'])
def getdatelist():
    if request.method=='POST':
        sql='SELECT date FROM bilibili.myrank12 group by date;'
        database = MySQLCommand(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        database.connectMysql()
        result = database.queryMysql(sql)
        print(result)
        datelist=[]
        for idx in range(len(result)):
            datelist.append(result[idx][0])
        return {'datelist':datelist}







if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)