#encoding=utf-8
'''
Created on 2016��11��20��

@author: FengGaojie
'''

import urllib
import urllib.request
import re

class spider:
    def __init__(self):
        self.max_page=50
        self.fp=open('rock.txt','w',encoding="utf-8")
    def getPage(self,num):
        url='http://www.rollingstone.com/music/lists/the-500-greatest-songs-of-all-time-20110407?json=true&page='+str(num)+'&limit=10'
        headers={'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        request=urllib.request.Request(url,headers=headers)
        response=urllib.request.urlopen(request)
        page=response.read().decode('utf-8')
        print("抓取第%d页:"%num)
        return page
    def parseInfo(self,content):
#         pattern=re.compile('{"id":(\d*?),"title":"(.*?)".*?'+
#                            '<p><strong>Writers?:</strong>(.*?)<br>.*?'+
#                            'Released:</strong>(.*?)<br>.*?'+
#                            '"sequence":(.*?)}', re.S)
        pattern=re.compile('[,|[]{"id":(\d*?),"title":"(.*?)","description":".*?",'+
                           '"body":"<p><strong>.*?Writer.*?</strong>(.*?)<.*?Released.*?</strong>(.*?)<.*?",'+
                           '.*?"sequence":(.*?)}',re.S)

        result=re.findall(pattern,content)
        print(content)
        n=1
        for i in result:
            print(n,":",i[4]+'*',i[0]+'*',i[1]+'*',i[2]+'*'+i[3])
            self.fp.write(i[4]+'  *  '+i[0]+'  *  '+i[1]+'*  '+i[2]+'  *  '+i[3]+'\n')
#             date=i[3].replace("&apos;","").split(",")
#             print(date[0],date[1])
            n+=1
# {"id":352107,"title":"Smokey Robinson and the Miracles, 'Shop Around'",
# "description":"",
# "body":"<p><strong>Writers:</strong> Berry Gordy, Robinson  <br><strong>Producer:</strong> Gordy  <br><strong>Released:</strong> Dec. &apos;60, Tamla <br>16 weeks; No. 2</p>\r\n<p><a href=\"../../../music/artists/smokey-robinson\"> Robinson</a> thought Barrett Strong should record &quot;Shop Around,&quot; but Gordy persuaded Smokey that he was the right man for the song. After it came out, Gordy heard it on the radio and found it way too slow. He woke Robinson at 3 a.m. and called him back to the studio to re-cut it &#x2014; faster and with Robinson&apos;s vocal more prominent. That one worked.</p>\r\n<p><strong>Appears on:</strong> <em>The Ultimate Collection</em> (Motown)</p>\r\n<p><strong>RELATED:</strong></p>\r\n<p>&#x2022; <a href=\"../../../music/lists/100-greatest-artists-of-all-time-19691231/smokey-robinson-and-the-miracles-19691231\">The 100 Greatest Artists of All Time: Smokey Robinson and the Miracles</a></p>\r\n<p><a href=\"../../../music/lists/100-greatest-artists-of-all-time-19691231/smokey-robinson-and-the-miracles-19691231\">&#x2022; </a><a href=\"../../../music/lists/100-greatest-singers-of-all-time-19691231/smokey-robinson-19691231\">The 100 Greatest Singers of All Time: Smokey Robinson</a></p>",
# "slug":"/music/lists/the-500-greatest-songs-of-all-time-20110407/smokey-robinson-and-the-miracles-shop-around-20110526",
# "order":1,"publish_date":"2011-05-26T21:57:35.000Z",
# "updated_publish_date":null,"author":null,
# "media":{"lead":{"id":"","alt":"","code":"",
# "type":"Variable Height Image","credits":"","details":"","filename":"","provider":""},
# "main_image":{"alt":null,"align":"full","caption":null,"credits":null,
# "filename":"rs-135712-260870b7a1fcd0ef2072c3529250f0effe2b88a7.jpg",
# "leadType":"Variable Height Image"}},"bitly":"","embeds":{"related":{"content":{"pinned":[]}}},"sequence":500}
    def main(self):
        num=17
        while(num<=self.max_page):
            content=self.getPage(num)
            self.parseInfo(content)
            num+=1
sp=spider()
sp.main()
        