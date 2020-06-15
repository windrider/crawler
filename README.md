# crawler
## 1.简介

​	本项目使用了vue+flask+mysql,爬取了bilibili上近三日热门视频排行榜的数据，并进行了相关的数据分析和可视化呈现在前端中。所有代码已经打包，vue目录下是前端部分的代码，mysql_flask目录下是后端部分的代码。

## 2.建表与数据获取

​	mysql代码在mysql_flask/create.sql文件中，建立数据表的代码如下：

```mysql
use bilibili;
create table `myrank12`
(
  `title` varchar(500) not null,
  `author` varchar(500) not null,
  `aid`    varchar(50)    not null,
  `bvid`   varchar(50)  not null,
  `coins`  int    not null,
  `play`   int    not null,
  `video_review` int    not null,
  `ranking` int   not null,
  `date`   varchar(50) not null,
  PRIMARY KEY(`bvid`,`date`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

​	  myrank表存储bilibili近三日热门视频排行榜中的视频数据，title为视频的标题，author为视频的作者，aid为视频的av号，bvid为视频的bv号，coins为视频的硬币数，play为视频的播放量，video_review为视频的评论数，ranking为视频的排名，date为当天日期。

​	数据获取部分的代码在mysql_flask/get_data.py文件中。

​        我们在bilibili的排行榜页面中找到其获取数据的api地址：'http://api.bilibili.com/x/web-interface/ranking'

​	在我们的get_data函数中向这个地址发送get请求，获取当天的排行榜数据。

```python
def get_data():
    rank_api = 'http://api.bilibili.com/x/web-interface/ranking'
    headers = {"User-Agent": UserAgent(verify_ssl=False).random}
    from_data={}
    response_comment = requests.get(rank_api, headers=headers, data=from_data)
    comment_json = response_comment.json()
    return comment_json
```

​         我们建数据表就是根据获取得数据的格式来建立的。

​          之后调用insert函数将数据按行插入到bilibili.myrank12表中。

​         这里插入数据时发现有的视频标题带了双引号，插入数据表时报错，需要对其进行转义的处理：

```python
for row in rows:
        print(row)
        temp=row["title"]
        temp=temp.replace('\"','\\\"')
        print(temp)
        row["title"]=temp
        thisrank=thisrank+1
        insert(row,thisrank)
```

​	这样处理后，数据表中能有带双引号的标题了。

## 3.绘制数据分析图

​	绘制数据分析图部分的代码在mysql_flask/visualize.py文件中。

​	调用get_data函数从数据库中获取数据，我们这里演示的是获取2020-06-15这一天的数据：

```python
def get_data():
    database.connectMysql()
    sql = 'SELECT title, author, bvid, coins, play, video_review, ranking, date FROM bilibili.myrank12 where date="2020-06-15";'
    result = database.queryMysql(sql)
    database.closeMysql()
    return result
```

​	 之后用draw_coins_play、draw_coins_review、draw_play_review三个函数画出视频的硬币数、播放量、评论数这三个属性两两之间的关系散点图。

​	因为榜上都是热门视频，所以这三个属性的值比较大，而且存在榜首和榜尾数据相差过大的情况，直接可视化的效果很糟糕，所以我们对数据做了log10的处理。

## 4.vue前端界面

​	前端的主要内容在vue/src/components/main.vue文件中。

​	UI的制作使用了element-ui。el-container为整体的页面布局容器，el-header顶栏呈现标题“bilibili视频排行榜数据”。el-main主要区域中有三个部分，第一部分是一个el-select选择器，可以选择要查看的数据的日期；第二部分位于左下，呈现排行榜前十的视频标题；第三部分位于右下，是el-radio单选框加上img组件，单选框有coins-play、coins_review、play_review三种选择，即根据单选框选择的内容呈现对应的分析图。

​	前端界面在建立时会向后端datelist接口发送post请求以获取所有可供选择的日期，保存在列表dt中，el-select选择器呈现的就是列表dt的内容：

```javascript
created(){
    this.axios({
        method: 'post',
        url: '/datelist',
      })
  .then(response => (this.dt = response.data.datelist));  
```

​	el-select选择器选中的值和selecteddt数据关联，前端监听selecteddt，当其值发生变化时，向后端changedt接口发送post请求，传递selecteddt参数，获取前十的视频标题，保存在前端的列表titles中：

```javascript
 watch:{
    selecteddt:function(val){
      console.log(7)
      this.axios({
        method: 'post',
        url: '/changedt',
        data: {
          dt: this.selecteddt
        }
      })
      .then(response => (this.titles = response.data.titles));
      this.mytime=new  Date().getTime();
      this.coins_play=this.coins_play + "?timestamp=" + this.mytime
      this.coins_review=this.coins_review + "?timestamp=" + this.mytime
      this.play_review=this.play_review + "?timestamp=" + this.mytime
    }
```

​	前端遍历列表titles，呈现前十的视频标题：

```vue
<div v-for= 'title in titles'>{{title.count}}.{{title.title}}</div>
```

​	el-radio单选框选中的值和pngtype数据绑定，根据pngtype的值呈现出选中的分析图：

​	其中coins_play、coins_review、play_review是三个URI,指向后端返回对应分析图的接口，这三个URI会在el-select选择器选中一个日期后修改时间戳，以应对浏览器的缓存机制（之前watch监听selecteddt的代码中表现出了这个设计）。

## 5.flask后端接口

​	flask设计后端接口的代码在mysql_flask的myflask.py文件中。

​	coins_play、coins_review、play_review这三个接口的作用就是向前端返回对应的三种分析图。

​	changedt接口，顾名思义，就是前端el-select选择器选定一个日期后会访问的接口，将后端的date变量修改为前端传来的日期值，然后向数据库查询title、ranking和date数据，按升序排列，将该日期排前十的视频数据封装进字典返回给前端：

```python
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
```

​	getdatelist接口，作用是向数据库查询当前所有的日期，返回给前端：

```python
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
```



## 6 系统运行

​	启动本地的mysql服务。

​	运行get_data.py和visualize.py，获取当天的bilibili热门排行榜视频数据并绘制分析图保存。

​	进入mysql_flask目录，执行python myflask.py命令，该程序会运行在5000端口。

​	进入vue目录，执行npm run dev命令，前端会运行在8080端口。

​	浏览器访问8080端口，可以操作前端界面。
