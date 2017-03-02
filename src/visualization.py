#encoding=utf-8
'''
Created on 2016��11��26��

@author: FengGaojie
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib# 
x_div = np.linspace(1, 57, 57)    # the x locations for the groups
# x_width = 1       # the width of the bars: can also be len(x) sequence
# y_div = np.linspace(1, 36, 36)    # the x locations for the groups
# y_width = 0.55
# 
# top100=[0,0,0,0,4,8,4,3,1,1,2,0,6,6,14,5,7,8,4,3,4,2,0,0,4,2,2,0,0,2,0,1,2,1,0,0,1,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
# data101_200=[0,1,0,4,0,4,6,2,3,3,1,3,0,5,6,5,3,6,7,2,5,1,5,2,2,1,4,1,2,2,0,0,1,1,0,0,2,2,1,1,1,0,0,0,0,0,0,0,0,0,0,3,0,0,1,0,1]
# data201_300=[0,0,2,2,1,1,2,1,1,3,2,2,1,5,6,10,4,3,6,3,3,8,2,2,0,1,1,1,5,2,0,4,1,1,0,2,0,0,3,0,0,1,1,1,0,0,1,0,1,1,0,1,1,0,1,0,0]
# data301_400=[0,0,0,1,2,4,3,3,0,2,2,1,1,2,7,3,6,5,4,5,5,2,4,0,5,1,5,2,5,1,0,1,2,2,0,0,2,0,3,0,1,1,0,0,1,1,1,0,2,0,0,0,2,0,0,0,0]
# data401_500=[1,0,0,0,1,2,3,1,0,3,3,0,0,5,2,5,6,1,4,5,3,2,5,1,3,1,3,4,1,0,1,1,2,3,1,1,4,0,2,0,3,0,2,3,0,0,0,1,0,2,5,0,2,0,1,1,0]

fig=plt.figure()
ax=fig.add_subplot(111)
# ax.set_title('click on point to plot time series')
# ax.bar(1,1,1)
# line, = ax.plot(np.random.rand(100), 'o', picker=5)

data=np.loadtxt('data.csv', delimiter=',',skiprows=1,
                dtype=bytes).astype(str)#也可以用dtype={'names':'','formats':'S100'}表示，但在python3.5中，由于导入结果奖杯编码为bytes，所以建议使用astype（str）
indexer=dict()
i=0
j=0
oldyear=newyear=""
for d in data:
    newyear=d[0]
    ranking=int(d[1])
    if(newyear==oldyear):
        j+=1
        d=np.append(d,i)
        d=np.append(d,j)
        indexer[str(i)+str(j)]=d
        if ranking>=1 and ranking<=100:
            ax.bar(i, 1, 1, color='g',bottom=j,edgecolor='k',picker=True)
        elif ranking>=101 and ranking<=200:
            ax.bar(i, 1, 1, color='b',bottom=j,edgecolor='k',picker=True)
        elif ranking>=201 and ranking<=300:
            ax.bar(i, 1, 1, color='#FFFF00',bottom=j,edgecolor='k',picker=True)
        elif ranking>=301 and ranking<=400:
            ax.bar(i, 1, 1, color='#FFC0CB',bottom=j,edgecolor='k',picker=True)
        elif ranking>=401 and ranking<=500:
            ax.bar(i, 1, 1, color='r',bottom=j,edgecolor='k',picker=True)
    else:
        i+=1
        j=0
        d=np.append(d,i)
        d=np.append(d,j)
        indexer[str(i)+str(j)]=d
#         print(i," ",j)
        if ranking>=1 and ranking<=100:
            p1=ax.bar(i, 1, 1, color='g',bottom=j,edgecolor='k',picker=True)
        elif ranking>=101 and ranking<=200:
            p2=ax.bar(i, 1, 1, color='b',bottom=j,edgecolor='k',picker=True)
        elif ranking>=201 and ranking<=300:
            p3=ax.bar(i, 1, 1, color='#FFFF00',bottom=j,edgecolor='k',picker=True)
        elif ranking>=301 and ranking<=400:
            p4=ax.bar(i, 1, 1, color='#FFC0CB',bottom=j,edgecolor='k',picker=True)
        elif ranking>=401 and ranking<=500:
            p5=ax.bar(i, 1, 1, color='r',bottom=j,edgecolor='k',picker=True)
    oldyear=newyear
#     print(d)
# print(indexer)

for label in ax.get_xticklabels(): 
                label.set_picker(True)

def onclick(event):
                if isinstance(event.artist, matplotlib.pyplot.Rectangle):
                    rect = event.artist#matplotlib中Rectangle的x就是index
                    bar_x=np.int(rect.get_x())
                    bar_y=np.int(rect.get_y())
                    album_index=str(bar_x)+str(bar_y)
#                     print(np.int(rect.get_x()),np.int(rect.get_y()))
                    plt.title('Rolling Stone TOP 500 songs'+'    Album:'+indexer[album_index][2]+'     Writers:'+indexer[album_index][3])
                    print(indexer[album_index][2],indexer[album_index][3])
#                     t1=ax.text(30,30,'Album:'+indexer[album_index][2])
#                     t2=ax.text(30,25,'Writers:'+indexer[album_index][3])
                 
#     print(d[0]," "+d[1]," "+d[2]," "+d[3])
N = 50
x = [1,2,3,4,5,6,7,8,9,10]
y1 = [1,1,0,1,1,1,1,1,1,1]
y2 = [1,0,0,1,0,1,1,1,1,1]
# p1 = plt.bar(x_div, top100, x_width, color='g')
# p2 = plt.bar(x_div, data101_200, x_width, color='b',
#              bottom=top100)
# p3 = plt.bar(x_div, data201_300, x_width, color='y',
#              bottom=np.add(data101_200,top100))
# p4 = plt.bar(x_div, data301_400, x_width, color='c',
#              bottom=np.add(np.add(data101_200,top100),data201_300))
# p5 = plt.bar(x_div, data401_500, x_width, color='r',
#              bottom=np.add(np.add(np.add(data101_200,top100),data201_300),data301_400))
plt.ylabel('Number of Albums')

plt.xticks(x_div, ("1948","1949","1953","1954","1955","1956","1957","1958","1959","1960","1961","1962","1963","1964","1965","1966","1967","1968","1969","1970","1971","1972","1973","1974","1975","1976","1977","1978","1979","1980","1981","1982","1983","1984","1985","1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1999","2000","2001","2002","2003","2004","2006","2007","2008","2009"),rotation=90)
 
plt.grid(which='major',linestyle='--',)
# plt.yticks(np.arange(0,36,1),('','',2,'',4,'',6,'',8,'',10,'',12,'',14,'',16,'',18,'',20,'',22,'',24,'',26,'',28,'',30,'',32,'',34,'',36))
plt.legend((p1[0], p2[0],p3[0],p4[0],p5[0]), ('TOP100', '101-200','201-300','301-400','401-500'))
fig.canvas.mpl_connect('pick_event', onclick)
plt.show()
#以上是bar

plt.show()

