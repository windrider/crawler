import matplotlib.pyplot as plt
import math
from config import db, host, port, user, passwd, charset
from db import MySQLCommand
def get_data():
    database.connectMysql()
    sql = 'SELECT title, author, bvid, coins, play, video_review, ranking, date FROM bilibili.myrank12 where date="2020-06-15";'
    result = database.queryMysql(sql)
    database.closeMysql()
    return result

def draw_coins_play(data):
    coins=[]
    play=[]
    date=data[0][7]
    for idx in range(len(data)):
        coins.append(math.log10(data[idx][3]))
        play.append(math.log10(data[idx][4]))
        #coins.append((data[idx][3]))
        #play.append((data[idx][4]))
    plt.plot(coins,play,'bo')
    plt.xlabel(u'coins')
    plt.ylabel(u'play')
    plt.xlim(0, max(coins))
    plt.ylim(0, max(play))
    # plt.show()
    plt.savefig('E:\sbz\Documents\homework3\mysql_flask\img\coins_play_'+date+'.png')

def draw_coins_review(data):
    coins=[]
    play=[]
    date=data[0][7]
    for idx in range(len(data)):
        coins.append(math.log10(data[idx][3]))
        play.append(math.log10(data[idx][5]))
        #coins.append((data[idx][3]))
        #play.append((data[idx][5]))
    plt.plot(coins,play,'bo')
    plt.xlabel(u'coins')
    plt.ylabel(u'review')
    plt.xlim(0, max(coins))
    plt.ylim(0, max(play))
    # plt.show()
    plt.savefig('E:\sbz\Documents\homework3\mysql_flask\img\coins_review_'+date+'.png')

def draw_play_review(data):
    coins=[]
    play=[]
    date=data[0][7]
    for idx in range(len(data)):
        coins.append(math.log10(data[idx][4]))
        play.append(math.log10(data[idx][5]))
    plt.plot(coins,play,'bo')
    plt.xlabel(u'play')
    plt.ylabel(u'review')
    plt.xlim(0, max(coins))
    plt.ylim(0, max(play))
    # plt.show()
    plt.savefig('E:\sbz\Documents\homework3\mysql_flask\img\play_review_'+date+'.png')



if __name__ == '__main__':
    # 显示中文
    # mpl.rcParams['font.sans-serif'] = ['SimHei']
    # mpl.rcParams['axes.unicode_minus'] = False
    database = MySQLCommand(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    data = get_data()
    draw_coins_play(data)
    draw_coins_review(data)
    draw_play_review(data)