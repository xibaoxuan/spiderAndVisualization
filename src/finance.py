#  -*- encoding:gb2312-*-
'''
Created on 

@author: FengGaojie
'''
import urllib.request
import re
import time
from _io import open
import pymysql #��װpymysql��cmd��py setup.py install
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
#ˢ��̫Ƶ��������ҳ����⵽�����쳣
        pageItems=re.findall('<div class="title"><a href="http://bj.lianjia.com/ershoufang/(.*?).html".*?>(.*?)</a>.*?'+
                  '<div class="houseInfo">.*?<a .*?data-el="region">(.*?)</a>(.*?)</div>.*?'+
                  '<div class="positionInfo">.*?</span>(.*?)-.*?'+
                  '<a href=.*?target="_blank">(.*?)</a>.*?'+
                  '<div class="tag">(.*?)</div>.*?'+
                  '<div class="totalPrice"><span>(.*?)</span>(.*?)</div>.*?'+
                  '<div class="unitPrice".*?data-price=".*?"><span>.*?����(.*?)Ԫ/ƽ��.*?</span>', read, re.S)
#         houseItems��Ӧ����ҳ���е�30����Դ��Ϣ
        for item in pageItems:
#             matchResult��Ӧ������Ϣ
            houseItem=item[0]+'*'+item[1]+'*'+item[2]+''+item[3].replace('|','*').replace(' ','').replace('ƽ��','')+'*'+item[4].replace(' ','*')+'*'+item[5]+'*'+item[7]+'*'+item[9]+'*'
#             moreMatch���ڽ�subway��haskey���಻�����ڵ���Ϣ��һ��ƥ��
            moreMatch=re.findall('.*?>(.*?)<.*?', item[6], re.S)
            for i in moreMatch:
                houseItem+=i+'*'
            houseItem+='*****'
            self.houseItems.append(houseItem);
#         pages[]һ��׷��1����Դ��Ϣ
    def getxiaoquID(self,district,pageNo):#ץȡÿһ����������ȫ��С��ID
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

    def gethouseofxiaoqu(self,xiaoquid):#ͨ��С��idץȡ��С����ÿһ�����۷�Դ
        page=1
        while True:
            baseURL='http://bj.lianjia.com/ershoufang/pg'+str(page)+'c'+xiaoquid
            headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
            req = urllib.request.Request(baseURL, headers=headers)
            response = urllib.request.urlopen(req)
            zaishouPage = response.read().decode("utf-8")
            #�Ȳ��ҵ�ǰУ�����м��׷�Դ
            if page==1:
                searchResult=re.search('<span class="checkbox checked"></span>.*?class="name">(.*?)</span>'
                                      +'.*?<h2 class="total fl">���ҵ�<span> (.*?) </span>�ױ������ַ�</h2>', zaishouPage, re.S)
                xiaoquName=searchResult.group(1)
                zaishouNum=int(searchResult.group(2))
                print(xiaoquName,'���۷�Դ',zaishouNum,'�ף�')
            #���С����ԴΪ0
            if zaishouNum==0:
                break
            #���߷�Դ����С��(page-1)*30�����ʾֹͣץȡ��С��
            if zaishouNum<=(page-1)*30:
                break
            print('��ʼץȡ',xiaoquName,'��%dҳ��'%page)
            page+=1
            zaishouItems=re.findall('<div class="title"><a href="http://bj.lianjia.com/ershoufang/(.*?).html".*?>(.*?)</a>.*?'+
                  '<div class="houseInfo">.*?<a .*?data-el="region">(.*?)</a> \|(.*?) \| (.*?)ƽ�� \| (.*?) \| (.*?)</div>.*?'+
                  '<div class="positionInfo">.*?</span>(.*?) (.*?)-.*?'+
                  '<a href=.*?target="_blank">(.*?)</a>.*?'+#����
                  '<div class="followInfo"><span class="starIcon"></span>(.*?)�˹�ע / ��(.*?)�δ��� / (.*?)</div>.*?'#��ע��������������������ʱ��
                  '<div class="tag">(.*?)</div>.*?'+
                  '<div class="totalPrice"><span>(.*?)</span>��</div>.*?'+#�ܼ�
                  '<div class="unitPrice".*?data-price=".*?"><span>.*?����(.*?)Ԫ/ƽ��.*?</span>', zaishouPage, re.S)#����
            
            for item in zaishouItems:
                
#                 print(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12],item[14],item[15])
                tags=re.sub('<(.*?)>', ' ', item[13])
                self.houseItem.append(item[0])#��ԴID
                self.houseItem.append(item[1])#��Դ����
                self.houseItem.append(item[2])#С��
                self.houseItem.append(item[3])#����
                self.houseItem.append(item[4])#���
                self.houseItem.append(item[5])#����
                self.houseItem.append(item[6])#װ��
                self.houseItem.append(item[7])#¥��
                self.houseItem.append(item[8])#���
                self.houseItem.append(item[9])#����
                self.houseItem.append(item[10])#��ע����
                self.houseItem.append(item[11])#��������
                self.houseItem.append(item[12])#����ʱ��
                self.houseItem.append(item[14])#�ܼ�
                self.houseItem.append(item[15])#����
                self.houseItem.append(tags)#��ǩ
                #д�����ݿ�
                print(self.houseItem)
                try:
                    self.writeDB(self.houseItem, 'house')
                except Exception as e:
                        if(hasattr(e, 'reason')):
                            print('д���house��������:'+e.reason)
                self.houseItem=[]
#                 self.writeDB(item, 'house')
            
    def getXiaoquInfo(self,pageNo,district):#������������ץȡ��������������С����Ϣ������xiaoquitems��
            baseURL="http://bj.lianjia.com/xiaoqu/"+district+"/pg"+pageNo
            print("����ץȡ "+district+"��С��:"+baseURL+'����ҳ�湲��',end='')
            headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
            req = urllib.request.Request(baseURL, headers=headers)
            response = urllib.request.urlopen(req)
            xiaoquPage = response.read().decode("utf-8")
            xiaoquItems = re.findall('<li class="clear">.*?<div class="title"><a href="http://bj.lianjia.com/xiaoqu/(.*?)/"'
                                   + '.*?data-el="xiaoqu">(.*?)</a>.*?'
                                   + '.*?<div class="houseInfo">.*?</span>(.*?)</div>'
                                   + '.*?<div class="positionInfo"><span.*?class="district".*?>(.*?)</a>'
                                   + '.*?class="bizcircle".*?>(.*?)</a>&nbsp;/(.*?)/&nbsp;(.*?)�꽨��</div>'
                                   + '.*?class="tagList"><.*?>(.*?)</div>'
                                   + '.*?class="totalPrice"><span>(.*?)</span>'
                                   + '.*?class="totalSellCount"><span>(.*?)</span>��</a>.*?</div></div></li>', xiaoquPage, re.S)
            i = 0
            xiaoquItem=[]
            for item in xiaoquItems:
#                 xiaoquItem=item[0]+'*'+item[1]+'*'
                xiaoquItem.append(item[0])#С��id
                xiaoquItem.append(item[1])#С������
                moreMatch1=re.findall('<a.*?>(.*?)</a>', item[2], re.S)
                #����tmp1������item[2]
                tmp1=''
                for everyItem in moreMatch1:
                    tmp1+=everyItem
                if '����' in tmp1:
                    huxing=tmp1[tmp1.find('��')+1:tmp1.find('��')]#�ҳ����͸���
                else:
                    huxing=''
                chengjiao=tmp1[tmp1.find('��')+1:tmp1.find('��')]#�ҳ��ɽ�����
                chuzu=tmp1[tmp1.find('��')+1:tmp1.find('��')-1]#�ҳ����͸���
#                 xiaoquItem=xiaoquItem+huxing+'*'+chengjiao+'*'+chuzu+'*'+item[3]+'*'+item[4]+'*'+item[5]+'*'+item[6]
                xiaoquItem.append(huxing)#���͸���
                xiaoquItem.append(chengjiao)#30��ɽ�����
                xiaoquItem.append(chuzu)#���ڳ�������
                xiaoquItem.append(item[3])#������
                xiaoquItem.append(item[4])#��Ȧ
                xiaoquItem.append(item[5])#¥��
                xiaoquItem.append(item[6])#���
#                  xiaoquItem+='*'+item[8]+'*'+item[9]
                xiaoquItem.append(item[8])#����
                xiaoquItem.append(item[9])#��������
                
                moreMatch2=re.findall('(<.*?>)', item[7], re.S)
                #t��һ������item[7]
                tmp2=item[7]
                for everyItem in moreMatch2:#ʹ��<>ƥ��html��ǩ��ʹ��ѭ������ǩ�滻��
                    tmp2=tmp2.replace(everyItem,' ')
                tmp2=tmp2.lstrip()
                tmp2=tmp2.rstrip()#ȥ��tag��Ϣ���˵Ŀո�
                
                tags=tmp2.split()
                if ' ' in tmp2:
                    xuequ=tags[0]
                    ditie=tags[1]   #���tmp2�м��пո���ָ����ֱ���xuequ��ditie
                else :
                    xuequ=''
                    ditie=tmp2   #���tmp2�в����ո�,��xuequΪ�գ�ditie����tmp2
#                 xiaoquItem+='*'+xuequ+'*'+ditie#tmp��item[7]������֮��Ľ��
                xiaoquItem.append(xuequ)#ѧ��
                xiaoquItem.append(ditie)#����
                self.xiaoquItems.append(xiaoquItem)
                xiaoquItem=[]
            print(len(xiaoquItems),'��С����')
    def writeTxt(self):
        for houseItem in self.houseItems:
            self.fp.write(houseItem)
    def writeDB(self,info_array,infoType):
        cur=self.conn.cursor()
        if infoType=='house':
            print('insert house ��%dҳ  '%(self.pageNo),info_array)
            insert_sql="insert into `house`(`id`,`biaoti`,`quyu`,`xiaoqu`,`huxing`,`mianji`,`zongjia`,`danjia`,`fabushijian`,`chaoxiang`,`zhuangxiu`,`louceng`,`nianfen`,`guanzhu`,`daikan`,`tags`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(insert_sql,(info_array[0],info_array[1],info_array[9],info_array[2],info_array[3],info_array[4],info_array[14],info_array[15],info_array[12],info_array[5],info_array[6],info_array[7],info_array[8],info_array[10],info_array[11],info_array[16]))
            self.conn.commit()
            print(cur)
        if infoType=='xiaoqu':
            
            print('����д���%dҳ  '%(self.pageNo),info_array)
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
            print("С��ID��ѯ�����Ϊ0")
        
    def main(self):
        self.fp.truncate()
#         _thread.start_new_thread(self.refreshPage, ())

#�����������ȡ���з�Դ��Ϣ�ģ���Ŀǰֻ��ץ��3000��
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
#                     self.writeDB(info_array)#�����ݿ����Ѿ�����ĳ�����ݣ�����������޷�����ӡ�ڿ���̨
#                 except Exception as e:
#                     if(hasattr(e, 'reason')):
#                         print('Something wrong while outputing:'+e.reason)
#             num1+=1
#             print("����%dҳ��,%d����Դ��"%(num1,num2))
#             self.pageNo+=1

#�����������ȡ����С����Ϣ��
#         xingzhengqus=['chaoyang','yanqing','xicheng','dongcheng','shijingshang','haidian','miyun','huairou','pinggu','shunyi','mentougou','daxing','fangshan','fengtai','yanjiao','tongzhou','changping']
#         for district in xingzhengqus:
#             self.pageNo=1
#             while self.keepdoing:
#                 self.getXiaoquInfo(str(self.pageNo),district)#ץȡÿһ��������������סլС��
#                 if len(self.xiaoquItems)==0:
#                     break#���ץ����С���б���Ϊ0����������һ��������
#                 while self.xiaoquItems:
#                     xiaoquinfo=self.xiaoquItems[0]
#                     del self.xiaoquItems[0]#�������Ϊ0��С����Ϣ������xiaoquinfo
# #                    ��С����Ϣд�����ݿ�
#                     try:
#                         self.writeDB(xiaoquinfo, 'xiaoqu')
#                     except Exception as e:
#                         if(hasattr(e, 'reason')):
#                             print('Something wrong while outputing:'+e.reason)
#                 self.pageNo+=1
        print("С����ȡ��ϣ�")
#         ���濪ʼ�����ݿ��а���ȡ��С��id��Ȼ��ץȡ��С����ķ�Դ��Ϣ
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
