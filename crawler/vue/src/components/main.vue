<template>
  <div class="main">
    <el-container>
  <el-header>bilibili视频排行榜数据</el-header>
  <el-main>
    <el-row class= 'grid-content'>
      <el-select v-model="selecteddt" placeholder="请选择日期">
    <el-option
      v-for="item in dt"
      :key="item"
      :label="item"
      :value="item">
    </el-option>
  </el-select>
 <!-- {{value}}  -->
    <!--</el-col> -->
    </el-row>
    <el-row class= 'grid-content'>
        <el-col :span="8">
          <div class='grid-content bg-purple'>
          排行榜前十
          </div>
        </el-col>
        <el-col :span="16">
          <div class='grid-content bg-purple'>
          <el-radio v-model="pngtype" label="0">coins-play</el-radio>
          <el-radio v-model="pngtype" label="1">coins-review</el-radio>
          <el-radio v-model="pngtype" label="2">play-review</el-radio>
      </div>
        </el-col> 
  </el-row>
      <el-row>
        <el-col :span="8">
       <div class='grid-content2 bg-purple'>
         <div v-for= 'title in titles'>{{title.count}}.{{title.title}}</div>
       </div>
        </el-col >
        <el-col :span="16">
          <img v-bind:src= 'coins_play'  v-if= "pngtype==0" />
          <img v-bind:src= 'coins_review'  v-if= "pngtype==1" />
          <img v-bind:src= 'play_review' v-if= "pngtype==2" />
        </el-col>
      </el-row>
  </el-main>
</el-container>
   </div>
</template>

<script>
export default {
  name: 'main',
  data () {
    return {
      selecteddt: '',
      dt: [],
      pngtype:0,
      coins_play:'http://127.0.0.1:5000/api/coins_play',
      coins_review:'http://127.0.0.1:5000/api/coins_review',
      play_review:'http://127.0.0.1:5000/api/play_review',
      titles:[]
    }
  },
  methods:{

    

    
  },
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
  },
  created(){
    this.axios({
        method: 'post',
        url: '/datelist',
      })
  .then(response => (this.dt = response.data.datelist));  
  ;
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
    text-align: center;
    padding-left: 10px;
    padding-right: 10px;
  }
  .el-col-2{
    border-radius: 4px;
    text-align: center;
    line-height: 300px;
    padding-left: 10px;
    padding-right: 10px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .bg-red {
    background: #f56c6c;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
    line-height: 30px;
  }
  .grid-content2 {
    margin-top: 10px;
    border-radius: 2px;
    min-height: 450px;
    line-height: 30px;
    overflow-x: hidden;
    text-align: left;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
  .el-header, .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }
  
  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }
  
  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 300px;
  }
  
  body > .el-container {
    margin-bottom: 40px;
  }
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
