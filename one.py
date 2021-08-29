# -*- codeing = utf-8 -*-
# @Time:2021/8/25 16:49
# @Author:A20190277
# @File:one.py
# @Software:PyCharm
''''''
'''
conda activate base
conda install missingno
conda update -all
'''
import pygal
import numpy as np
import pandas as pd
import missingno as msno
import seaborn as sns
from collections import Counter
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

df1=pd.read_csv(r'C:\Users\18356\Desktop\Kaggle\Video Game Sales\vgsales.csv')
print(df1.head())
print(df1.describe(include = 'all').T)    #默认只处理数值类型，include='all'：全处理，'object'：字符串

#msno.matrix(df1, figsize = (16, 5),labels=True)   #白线越多，缺失值越多
#plt.show()
#缺失值所占比例为：

def mis_val_tabel(df):
    mis_val = df1.isnull()   #缺失值的判断，与isna()等价，若values为缺失值则返回True
    mis_val_num= mis_val.sum()
    mis_val_pre=100*mis_val_num/len(df)
    mis_val_pre_tabel=mis_val_pre.to_frame()
    mis_val_pre_tabel.columns=['缺失率']
    mis_val_pre_tabel=mis_val_pre_tabel.sort_values(by='缺失率',ascending=False, axis=0)
    return mis_val_pre_tabel
print(mis_val_tabel(df1))
#可看出缺失值最大的也只占了1.6%，所以可直接删除
df2=df1.dropna()
# msno.matrix(df2, figsize = (16, 5),labels=True)
# plt.show()   #可看出缺失值已经剔除完毕了
print('----------------------缺失值处理完毕！-----------------------------')
#处理异常值
print(df2[df2['Year']>2017])  #只有一条，删去
df3=df2.drop([5957],axis=0)
#df3.to_csv(r'C:\Users\18356\Desktop\Kaggle\Video Game Sales\df3.csv',index=False)
print('----------------------异常值处理完毕！-----------------------------')

#数据可视化
#在对数据进行异常值处理时，发现年份的数据类型不是int，所以要先对数据类型进行处理
df3.Year=df3.Year.astype(int)
print(df3.info())

#根据提出的问题进行可视化操作
#用户最喜爱的平台，游戏类型
#Genre：游戏类型
genres_tabel=df3.pivot_table('Global_Sales',index='Genre',columns='Year',aggfunc='sum')
#数据透视表函数，'Global_Sales'：指定要聚合的列，aggfunc：统计方法
#将销售额和每个游戏类型联系起来，还有年份，这样才能看出趋势
genres=genres_tabel.idxmax()  #返回在请求轴上第一次出现最大值的索引，得出每一年中销售额最大的游戏类型
sales=genres_tabel.max()     #得出每一年中最大的销售数额
years=genres_tabel.columns.astype(int)   #得到年份数组，类型强制转化为int
genres_df=pd.concat([genres,sales],axis=1)  #游戏类型与销售额合并
genres_df.columns=['Genre', 'Global Sales']
# ax=sns.pointplot(y='Global Sales',x=years,hue='Genre',data=genres_df)
# ax.set_title('销售额最大的游戏类型随着年份的变化情况')
# ax.set_xlabel('年份')
# ax.set_ylabel('销售额')
# ax.set_xticklabels(labels = years)
# plt.savefig("p1", dpi=600)
# plt.show()
'''
可以看出：Action近几年在市场中占比较重要的地位，但是它的销售情况是逐年递减的
Role-Playing在2017年占了游戏市场的最大比重，可以大胆猜想，它未来可能会在游戏市场占一部分比重
除此之外还可以看出：Shooter,Fighting,Puzzle发展不容乐观
以上只是较为粗糙的分析与猜测，后续可以对近几年的游戏类型与销售额做饼状图进行具体分析
根据以下对平台的分析，进行补充Role-Playing在2017年虽然最受欢迎，销售额却最少，可能是与整体的游戏市场相关，所以它未来可能会在游戏市场占一部分比重这个猜想较为合理
再次思考，为什么游戏市场后续衰败：发行游戏数量？
'''
#销售额与年份
money_order=df3.groupby(by=['Year'],as_index=False).sum()
Y=years
order_order=df3.groupby(by=['Year'],as_index=False).count()
dw=pd.DataFrame({'销售额':money_order['Global_Sales'],'游戏数量':order_order['Genre']})
dw.index=[Y]
# dw.plot()
# plt.title('销售额游戏数量之间的关系如何')
# plt.xlabel('年份')
# plt.savefig("p3", dpi=600)
# plt.show()
'''
由图得出的分析见上
'''

#与上方类似，对平台进行分析
platform_tabel=df3.pivot_table('Global_Sales',index='Platform',columns='Year',aggfunc='sum')
platform=platform_tabel.idxmax()
sales=platform_tabel.max()
years=platform_tabel.columns.astype(int)
platform_df=pd.concat([platform,sales],axis=1)
platform_df.columns=['Platform', 'Global Sales']
# ax=sns.pointplot(y='Global Sales',x=years,hue='Platform',data=platform_df)
# ax.set_title('销售额最大的游戏平台随着年份的变化情况')
# ax.set_xlabel('年份')
# ax.set_ylabel('销售额')
# ax.set_xticklabels(labels = years)
# plt.savefig("p2", dpi=600)
# plt.show()
'''
可以看出：市场上的游戏平台龙头一直在发生改变
还可以看出在200？~200？年时游戏市场处于蓬勃发展
以上只是较为粗糙的分析与猜测：后续可以对为什么游戏平台的龙头地位与什么相关进行研究，是与游戏类型有较大关系还是合作的发行商有较大关系
'''

'''
再次思考，为什么游戏市场的龙头平台在一直变化，变化的原因是与合作的发行商有关还是与市场趋势有关
龙头平台的上的游戏类型最多是什么，选取前5大龙头平台进行分析，由于时效性问题，分析时只取近5年的销售数据
'''
#前五的龙头平台
FPF=pd.pivot_table(df3,index='Year',columns='Platform',values='Global_Sales',aggfunc=np.sum).sum().sort_values(ascending=False)
FPF=pd.DataFrame(data=FPF,columns={'Global_Sales'})
FPF_near5=pd.pivot_table(df3,index='Year',columns='Platform',values='Global_Sales',aggfunc=np.sum).iloc[-5:,:].sum().sort_values(ascending=False)
FPF_near5=pd.DataFrame(data=FPF_near5,columns={'Global_Sales'})
# fig,(ax1,ax2)=plt.subplots(2,1,figsize=(16,10))
# sns.barplot(x=FPF.index,y='Global_Sales',data=FPF,ax=ax1)
# sns.barplot(x=FPF_near5.index,y='Global_Sales',data=FPF_near5,ax=ax2)
# plt.title('近五年的销售情况直方图')
# plt.savefig("p4", dpi=800)
# plt.show()
'''
可以看出没有龙头企业产生了较大变化，不知道由于什么原因PS2消声灭迹，PS4稳占第一
可以分析一下PS2为什么消失，PS4为什么崛起
'''
#前五的发行商
PUB=pd.pivot_table(df3,index='Year',columns='Publisher',values='Global_Sales',aggfunc=np.sum).sum().sort_values(ascending=False)
PUB=pd.DataFrame(data=PUB,columns={'Global_Sales'})
PUB_near5=pd.pivot_table(df3,index='Year',columns='Publisher',values='Global_Sales',aggfunc=np.sum).iloc[-5:,:].sum().sort_values(ascending=False)
PUB_near5=pd.DataFrame(data=PUB_near5,columns={'Global_Sales'})
PUB=PUB.head(10)
PUB_near5=PUB_near5.head(10)
fig,(ax3,ax4)=plt.subplots(2,1,figsize=(16,10))
# sns.barplot(x=PUB.index,y='Global_Sales',data=PUB,ax=ax3)
# sns.barplot(x=PUB_near5.index,y='Global_Sales',data=PUB_near5,ax=ax4)
# plt.title('TOP发行商直方图')
# plt.savefig("p6", dpi=800)
# plt.show()
'''
TOP发行商在近几年之间的差异较小，Nintendo可以说是一直在市场的地位很高
思考：为什么Electronic Arts在近几年取代了Nintendo的地位
'''


#地区的销售额占比情况
money_order=df3.groupby(by=['Year'],as_index=False).sum()
Y=years
order_order=df3.groupby(by=['Year'],as_index=False).count()
DS=pd.DataFrame({'全球销售额':money_order['Global_Sales'],'北美销售额':money_order['NA_Sales'],
                 '欧洲销售额':money_order['EU_Sales'],'日本销售额':money_order['JP_Sales'],
                 '其他地区销售额':money_order['Other_Sales']
                 })
DS.index=[Y]
# DS.plot()
# plt.title('地区的销售额情况')
# plt.xlabel('年份')
# plt.savefig("p5", dpi=800)
# plt.show()
'''
由图可以看出在北美市场一直为主力，其次是欧洲市场
'''
#各地区喜欢的游戏类型，讨论近15年
df4=df3[df3['Year']>2003]
#游戏类型，销售额，各地区
GM=df4.groupby(by=['Genre'],as_index=False).sum()
GM=GM.set_index(['Genre'])
GM=GM.T.drop(['Rank','Year'])
# GM.plot.bar(y=['Action','Adventure','Fighting','Misc','Platform','Puzzle','Racing','Role-Playing','Shooter','Simulation','Sports','Strategy'],stacked='True')
# plt.title('近几年各地区各地区喜欢的游戏类型')
# plt.savefig("p7", dpi=800)
# plt.show()

'''
可以发现，Sports,Action,Shooter,Misc,Role-Playing进一步分析
之前绘制的线图与该图可以结合分析
绘制Sports,Action,Shooter,Misc,Role-Playing近10年的销售变化图，
总体的以及各地区的都可以进行绘制
'''
GNS=df4.pivot_table('Global_Sales',index='Genre',columns='Year',aggfunc='sum')
GNS=GNS.T
a=GNS['Action']
b=GNS['Adventure']
DS=pd.DataFrame({'Action':GNS['Action'],'Adventure':GNS['Adventure'],
                 'Fighting':GNS['Fighting'],'Misc':GNS['Misc'],
                 'Platform':GNS['Platform'],'Puzzle':GNS['Puzzle'],
                 'Racing':GNS['Racing'],'Role-Playing':GNS['Role-Playing'],
                 'Shooter':GNS['Shooter'],'Simulation':GNS['Simulation'],
                 'Sports':GNS['Sports'],'Strategy':GNS['Strategy']
                 })
# DS.plot()
# plt.title('近几年各地区销售与游戏类型之间的联系')
# plt.savefig("p8", dpi=800)
# plt.show()

'''
根据图8发现，之前关于Role-Playing的猜想错误（2017年数据不全面），但是根据日本市场近几年Role-Playing的销售额占比来看，Role-Playing未来可能在日本市场上占一席之地
估计未来市场，Action、Shooter、Sports、Role-Playing'为主流，Shooter未来有望超过Action，Role-Playing在日本可能会有较大发展空间
关于未来游戏类型的猜想结束

根据游戏类型，发行商未来可以着重发布Action、Shooter、Sports、Role-Playing类游戏
下一步，分析发行商发行的游戏类型，发行商过多，只讨论前几名
平台与发行商的合作
'''

GPC=df4.pivot_table('Year',index='Publisher',columns='Genre',aggfunc='count').T
GPC=GPC[['Nintendo', 'Electronic Arts', 'Activision', 'Sony Computer Entertainment', 'Ubisoft', 'Take-Two Interactive', 'THQ',
       'Konami Digital Entertainment', 'Sega', 'Namco Bandai Games']]
# GPC.plot.bar(y=['Nintendo', 'Electronic Arts', 'Activision', 'Sony Computer Entertainment', 'Ubisoft', 'Take-Two Interactive', 'THQ', 'Konami Digital Entertainment', 'Sega', 'Namco Bandai Games'],stacked='True')
# plt.title('近几年发行商发行与游戏类型之间的联系')
# plt.savefig("p9", dpi=800)
# plt.show()

'''
由图发现，
Nintendo虽然近几年销售额排名第一，但是它发行的数量在各个类型中并不多，原因不明
Electronic Arts在多个游戏类型中都有一些不少的占比，在Shooter中占比最大，提出建议：可以减少一些不是很受大众欢迎的游戏的发行，使资金得到更好的应用
Activision发行的大部分游戏为Action与Shooter，
发行商的分析结束
下一步，分析平台的，平台与发行商的合作
平台与发行商合作的
'''
PPP=df4.pivot_table('Year',index='Platform',columns='Publisher',aggfunc='count')
PPP=PPP[['Nintendo', 'Electronic Arts', 'Activision', 'Sony Computer Entertainment', 'Ubisoft', 'Take-Two Interactive', 'THQ',
       'Konami Digital Entertainment', 'Sega', 'Namco Bandai Games']].T
PPP.plot.bar(y=['X360', 'PS3', 'Wii', 'DS', 'PS2', 'PSP', 'PS4', '3DS', 'PC', 'XOne', 'XB', 'GBA', 'WiiU', 'GC', 'PSV', 'DC'],stacked='True')
plt.title('近几年平台与发行商之间的联系')
plt.savefig("p10", dpi=1000)
plt.show()

'''
Nintendo合作的平台也较少，与PS3合作相对紧密
将p9与p10结合起来，让平台可以尽量避免游戏种类的重复
'''

print('分析到此结束！')



