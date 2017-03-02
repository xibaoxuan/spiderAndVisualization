#  -*- encoding:gb2312-*-
'''
Created on 

@author: FengGaojie
'''
import urllib.request
import re
import time
from _io import open
import pymysql #安装pymysql：cmd中py setup.py install
from idlelib.ReplaceDialog import replace
from macpath import split
# import locale   

class spider:
    def __init__(self):
        self.pageNo=1
        self.houseItems=[]
        self.houseItem=[]
        self.xiaoquItems=[]
        self.keepdoing=True
        self.fp=open('houseInfo.txt','w',encoding="utf-8")
        self.conn=pymysql.connect(host='localhost',user='root',password='',db='app_',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
   
    def refreshPage(self):
        while(self.keepdoing):
            time.sleep(0.1)
            print("fetching page"+str(self.pageNo)+":")
            if(len(self.houseItems)<2):
                try:
                    self.getPage(str(self.pageNo))
                    self.pageNo+=1
                except Exception as e:
                    if(hasattr(e, 'reason')):
                        print('exception:'+e.reason)
                        self.keepdoing=False
                except Exception as e:
                    if(hasattr(e, 'reason')):
                        print('Due to:'+e.reason)
            print(len(self.houseItems))
    
    def getHouseInfo(self,pageNo):
        print("Get page",self.pageNo,":")
        myUrl="http://bj.lianjia.com/ershoufang/pg"+ pageNo
        headers={'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        req=urllib.request.Request(myUrl,headers=headers)
        response=urllib.request.urlopen(req)
        read=response.read().decode('utf-8')
#刷新太频繁，链家页面会检测到流量异常
        pageItems=re.findall('<div class="title"><a href="http://bj.lianjia.com/ershoufang/(.*?).html".*?>(.*?)</a>.*?'+
                  '<div class="houseInfo">.*?<a .*?data-el="region">(.*?)</a>(.*?)</div>.*?'+
                  '<div class="positionInfo">.*?</span>(.*?)-.*?'+
                  '<a href=.*?target="_blank">(.*?)</a>.*?'+
                  '<div class="tag">(.*?)</div>.*?'+
                  '<div class="totalPrice"><span>(.*?)</span>(.*?)</div>.*?'+
                  '<div class="unitPrice".*?data-price=".*?"><span>.*?单价(.*?)元/平米.*?</span>', read, re.S)
#         houseItems对应整个页面中的30条房源信息
        for item in pageItems:
#             matchResult对应单条信息
            houseItem=item[0]+'*'+item[1]+'*'+item[2]+''+item[3].replace('|','*').replace(' ','').replace('平米','')+'*'+item[4].replace(' ','*')+'*'+item[5]+'*'+item[7]+'*'+item[9]+'*'
#             moreMatch用于将subway、haskey这类不定存在的信息进一步匹配
            moreMatch=re.findall('.*?>(.*?)<.*?', item[6], re.S)
            for i in moreMatch:
                houseItem+=i+'*'
            houseItem+='*****'
            self.houseItems.append(houseItem);
#         pages[]一次追加1条房源信息
    def getxiaoquID(self,district,pageNo):#抓取每一个行政区的全部小区ID
            baseURL="http://bj.lianjia.com/xiaoqu/"+district+"/pg"+pageNo
            print("fetching "+district+":"+baseURL)
            headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
            req = urllib.request.Request(baseURL, headers=headers)
            response = urllib.request.urlopen(req)
            xiaoquPage = response.read().decode("utf-8")
            xiaoquItems = re.findall('<li class="clear">.*?<div class="title"><a href="http://bj.lianjia.com/xiaoqu/(.*?)/"'
                                       + '.*?data-el="xiaoqu">(.*?)</a>.*?', xiaoquPage, re.S)
            for item in xiaoquItems:
                print(item)

    def gethouseofxiaoqu(self,xiaoquid):#通过小区id抓取该小区的每一个在售房源
        page=1
        while True:
            baseURL='http://bj.lianjia.com/ershoufang/pg'+str(page)+'c'+xiaoquid
            headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
            req = urllib.request.Request(baseURL, headers=headers)
            response = urllib.request.urlopen(req)
            zaishouPage = response.read().decode("utf-8")
            #先查找当前校区共有几套房源
            if page==1:
                searchResult=re.search('<span class="checkbox checked"></span>.*?class="name">(.*?)</span>'
                                      +'.*?<h2 class="total fl">共找到<span> (.*?) </span>套北京二手房</h2>', zaishouPage, re.S)
                xiaoquName=searchResult.group(1)
                zaishouNum=int(searchResult.group(2))
                print(xiaoquName,'在售房源',zaishouNum,'套：')
            #如果小区房源为0
            if zaishouNum==0:
                break
            #或者房源数量小于(page-1)*30，则表示停止抓取本小区
            if zaishouNum<=(page-1)*30:
                break
            print('开始抓取',xiaoquName,'第%d页：'%page)
            page+=1
            zaishouItems=re.findall('<div class="title"><a href="http://bj.lianjia.com/ershoufang/(.*?).html".*?>(.*?)</a>.*?'+
                  '<div class="houseInfo">.*?<a .*?data-el="region">(.*?)</a> \|(.*?) \| (.*?)平米 \| (.*?) \| (.*?)</div>.*?'+
                  '<div class="positionInfo">.*?</span>(.*?) (.*?)-.*?'+
                  '<a href=.*?target="_blank">(.*?)</a>.*?'+#区域
                  '<div class="followInfo"><span class="starIcon"></span>(.*?)人关注 / 共(.*?)次带看 / (.*?)</div>.*?'#关注人数、带看次数、发布时间
                  '<div class="tag">(.*?)</div>.*?'+
                  '<div class="totalPrice"><span>(.*?)</span>万</div>.*?'+#总价
                  '<div class="unitPrice".*?data-price=".*?"><span>.*?单价(.*?)元/平米.*?</span>', zaishouPage, re.S)#单价
            
            for item in zaishouItems:
                
#                 print(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12],item[14],item[15])
                tags=re.sub('<(.*?)>', ' ', item[13])
                self.houseItem.append(item[0])#房源ID
                self.houseItem.append(item[1])#房源标题
                self.houseItem.append(item[2])#小区
                self.houseItem.append(item[3])#户型
                self.houseItem.append(item[4])#面积
                self.houseItem.append(item[5])#朝向
                self.houseItem.append(item[6])#装修
                self.houseItem.append(item[7])#楼层
                self.houseItem.append(item[8])#年份
                self.houseItem.append(item[9])#区域
                self.houseItem.append(item[10])#关注人数
                self.houseItem.append(item[11])#带看次数
                self.houseItem.append(item[12])#发布时间
                self.houseItem.append(item[14])#总价
                self.houseItem.append(item[15])#单价
                self.houseItem.append(tags)#标签
                #写入数据库
                print(self.houseItem)
                try:
                    self.writeDB(self.houseItem, 'house')
                except Exception as e:
                        if(hasattr(e, 'reason')):
                            print('写入表house发生错误:'+e.reason)
                self.houseItem=[]
#                 self.writeDB(item, 'house')
            
    def getXiaoquInfo(self,pageNo,district):#给定行政区，抓取该行政区的所有小区信息，存在xiaoquitems中
            baseURL="http://bj.lianjia.com/xiaoqu/"+district+"/pg"+pageNo
            print("正在抓取 "+district+"的小区:"+baseURL+'，此页面共有',end='')
            headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
            req = urllib.request.Request(baseURL, headers=headers)
            response = urllib.request.urlopen(req)
            xiaoquPage = response.read().decode("utf-8")
            xiaoquItems = re.findall('<li class="clear">.*?<div class="title"><a href="http://bj.lianjia.com/xiaoqu/(.*?)/"'
                                   + '.*?data-el="xiaoqu">(.*?)</a>.*?'
                                   + '.*?<div class="houseInfo">.*?</span>(.*?)</div>'
                                   + '.*?<div class="positionInfo"><span.*?class="district".*?>(.*?)</a>'
                                   + '.*?class="bizcircle".*?>(.*?)</a>&nbsp;/(.*?)/&nbsp;(.*?)年建成</div>'
                                   + '.*?class="tagList"><.*?>(.*?)</div>'
                                   + '.*?class="totalPrice"><span>(.*?)</span>'
                                   + '.*?class="totalSellCount"><span>(.*?)</span>套</a>.*?</div></div></li>', xiaoquPage, re.S)
            i = 0
            xiaoquItem=[]
            for item in xiaoquItems:
#                 xiaoquItem=item[0]+'*'+item[1]+'*'
                xiaoquItem.append(item[0])#小区id
                xiaoquItem.append(item[1])#小区名称
                moreMatch1=re.findall('<a.*?>(.*?)</a>', item[2], re.S)
                #利用tmp1来修正item[2]
                tmp1=''
                for everyItem in moreMatch1:
                    tmp1+=everyItem
                if '户型' in tmp1:
                    huxing=tmp1[tmp1.find('共')+1:tmp1.find('个')]#找出户型个数
                else:
                    huxing=''
                chengjiao=tmp1[tmp1.find('交')+1:tmp1.find('套')]#找出成交个数
                chuzu=tmp1[tmp1.find('套')+1:tmp1.find('正')-1]#找出户型个数
#                 xiaoquItem=xiaoquItem+huxing+'*'+chengjiao+'*'+chuzu+'*'+item[3]+'*'+item[4]+'*'+item[5]+'*'+item[6]
                xiaoquItem.append(huxing)#户型个数
                xiaoquItem.append(chengjiao)#30天成交套数
                xiaoquItem.append(chuzu)#正在出租套数
                xiaoquItem.append(item[3])#行政区
                xiaoquItem.append(item[4])#商圈
                xiaoquItem.append(item[5])#楼型
                xiaoquItem.append(item[6])#年份
#                  xiaoquItem+='*'+item[8]+'*'+item[9]
                xiaoquItem.append(item[8])#单价
                xiaoquItem.append(item[9])#在售数量
                
                moreMatch2=re.findall('(<.*?>)', item[7], re.S)
                #t进一步修正item[7]
                tmp2=item[7]
                for everyItem in moreMatch2:#使用<>匹配html标签，使用循环将标签替换掉
                    tmp2=tmp2.replace(everyItem,' ')
                tmp2=tmp2.lstrip()
                tmp2=tmp2.rstrip()#去除tag信息两端的空格
                
                tags=tmp2.split()
                if ' ' in tmp2:
                    xuequ=tags[0]
                    ditie=tags[1]   #如果tmp2中间有空格，则分割它分别是xuequ和ditie
                else :
                    xuequ=''
                    ditie=tmp2   #如果tmp2中不含空格,则xuequ为空，ditie等于tmp2
#                 xiaoquItem+='*'+xuequ+'*'+ditie#tmp是item[7]修正过之后的结果
                xiaoquItem.append(xuequ)#学区
                xiaoquItem.append(ditie)#地铁
                self.xiaoquItems.append(xiaoquItem)
                xiaoquItem=[]
            print(len(xiaoquItems),'个小区：')
    def writeTxt(self):
        for houseItem in self.houseItems:
            self.fp.write(houseItem)
    def writeDB(self,info_array,infoType):
        cur=self.conn.cursor()
        if infoType=='house':
            print('insert house 第%d页  '%(self.pageNo),info_array)
            insert_sql="insert into `house`(`id`,`biaoti`,`quyu`,`xiaoqu`,`huxing`,`mianji`,`zongjia`,`danjia`,`fabushijian`,`chaoxiang`,`zhuangxiu`,`louceng`,`nianfen`,`guanzhu`,`daikan`,`tags`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(insert_sql,(info_array[0],info_array[1],info_array[9],info_array[2],info_array[3],info_array[4],info_array[14],info_array[15],info_array[12],info_array[5],info_array[6],info_array[7],info_array[8],info_array[10],info_array[11],info_array[16]))
            self.conn.commit()
            print(cur)
        if infoType=='xiaoqu':
            
            print('正在写入第%d页  '%(self.pageNo),info_array)
            insert_sql="insert into `xiaoqu`(`xiaoquid`,`xiaoqu`,`huxingshu`,`chengjiaoshu`,`chuzushu`,`xingzhengqu`,`quyu`,`louxing`,`nianfen`,`junjia`,`zaishou`,`xuequ`,`jiaotong`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(insert_sql,(info_array[0],info_array[1],info_array[2],info_array[3],info_array[4],info_array[5],info_array[6],info_array[7],info_array[8],info_array[9],info_array[10],info_array[11],info_array[12]))
            self.conn.commit()
            
    def getXiaoquIDfromDB(self,page):
        sql="select xiaoquid from (select @rownum:=@rownum+1 as rank,xiaoquid from (select @rownum:=0)num,xiaoqu)temp where rank>"+str((page-1)*5)+" and rank<="+str(page*5)
        cur=self.conn.cursor()
        result=cur.execute(sql)
        xiaoquids=[]
        if result!=0:
            for i in cur:
                xiaoquids.append(i['xiaoquid'])
            return xiaoquids
        else :
            print("小区ID查询结果集为0")
        
    def main(self):
        self.fp.truncate()
#         _thread.start_new_thread(self.refreshPage, ())

#下面这段是爬取所有房源信息的，但目前只能抓到3000条
#         num1=0
#         num2=0
#         while self.keepdoing:
#             self.getHouseInfo(str(self.pageNo))
# #             logging.basicConfig(filename='logging.log',level=logging.DEBUG)
#             while self.houseItems:
#                 try:
#                     houseinfo=self.houseItems[0]
#                     del self.houseItems[0]
#                     self.fp.write(houseinfo+'\n')
#                     info_array=houseinfo.split('*')
#                     num2+=1
#                     self.writeDB(info_array)#若数据库中已经存在某条数据，则此条数据无法被打印在控制台
#                 except Exception as e:
#                     if(hasattr(e, 'reason')):
#                         print('Something wrong while outputing:'+e.reason)
#             num1+=1
#             print("共计%d页面,%d条房源！"%(num1,num2))
#             self.pageNo+=1

#下面这段是爬取所有小区信息的
#         xingzhengqus=['chaoyang','yanqing','xicheng','dongcheng','shijingshang','haidian','miyun','huairou','pinggu','shunyi','mentougou','daxing','fangshan','fengtai','yanjiao','tongzhou','changping']
#         for district in xingzhengqus:
#             self.pageNo=1
#             while self.keepdoing:
#                 self.getXiaoquInfo(str(self.pageNo),district)#抓取每一个行政区的所有住宅小区
#                 if len(self.xiaoquItems)==0:
#                     break#如果抓到的小区列表长度为0，则跳到下一个行政区
#                 while self.xiaoquItems:
#                     xiaoquinfo=self.xiaoquItems[0]
#                     del self.xiaoquItems[0]#弹出序号为0的小区信息，存入xiaoquinfo
# #                    将小区信息写入数据库
#                     try:
#                         self.writeDB(xiaoquinfo, 'xiaoqu')
#                     except Exception as e:
#                         if(hasattr(e, 'reason')):
#                             print('Something wrong while outputing:'+e.reason)
#                 self.pageNo+=1
        print("小区爬取完毕！")
#         下面开始从数据库中挨个取出小区id，然后抓取该小区里的房源信息
        n=1
        while(self.getXiaoquIDfromDB(n)):
            xiaoquids=self.getXiaoquIDfromDB(n)
            print(xiaoquids)
            for xiaoquid in xiaoquids:
                self.gethouseofxiaoqu(xiaoquid)
            n=n+1
        self.fp.close()  
        self.conn.close()
    
spiderOnLianjia=spider()
spiderOnLianjia.main()
