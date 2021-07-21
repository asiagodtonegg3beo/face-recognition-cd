#------------------------------------------------------------------------------ import要用的
import collections
import numpy as np
import pandas as pd
import time
from sqlalchemy import create_engine
#------------------------------------------------------------------------------ 開檔，讀log.txt，輸出check_in.txt
f=open("log.txt","r")# open log.txt
f2=open("output.txt","w")
#------------------------------------------------------------------------------ Read log.txt row by row
log=f.readlines()
#------------------------------------------------------------------------------ 把log中的機率拔掉，存進newlog
newlog=[]#創一個空list準備存去掉機率的log
i=0
for i in range(len(log)):
    newlog.append(log[i][0:8])
#------------------------------------------------------------------------------ 把newlog中出現機率過少的移除，存進newlist，這裡newlist為list裡面包list，
#------------------------------------------------------------------------------ 可看words變數來理解我意思 #提出機率在(0.7,1]之間的人
words = [l.split() for l in newlog]
counts = collections.Counter(word for l in words for word in l)
newlist =[[s for s in l if 0.7< counts[s]/len(newlog) <= 1.0] for l in words]
#------------------------------------------------------------------------------ 把newlist美化成list 裡面包 str
i=0
j=len(log)
for i in range(j):
    newlist[i]=str(newlist[i])
#------------------------------------------------------------------------------ 1.刪除['  2.刪除']
outputlog=[]#創一個空list準備存去掉['']的newlist
i=0
for i in range(len(newlist)):
    outputlog.append(newlist[i][2:10])
#------------------------------------------------------------------------------ 刪除空元素，使用.pop(引數)           ***這邊容易出BUG***
i=0
for i in range(len(outputlog)):#如果不減，IndexError: list index out of range
    if(i<len(outputlog)):
        if(bool(outputlog[i])):
            j=j
        else:
            outputlog.pop(i)
#------------------------------------------------------------------------------ 刪除outputlog重複項，用output存
output=[]#創一個空list準備存刪掉重複項的outputlog
i=0
for i in outputlog:
    if i not in output:
        output.append(i)
output.pop(1)
#------------------------------------------------------------------------------ 輸出檔案

with open('output.txt', 'w') as f2:
    for item in output:
        f2.write("%s\n" % item)
#------------------------------------------------------------------------------ 寫入資料庫
# MySQL使用者名稱：root, password:admin, port：8763,資料庫：3B10
engine = create_engine('mysql+pymysql://root:admin@120.101.8.8:8763/3B10?charset=utf8')

# SQL查詢語句，選出表中的所有數據 
sql = ''' 
SELECT * FROM `TABLE 1`;
 '''
# 定義 on time 函數
def ontime(name):
    engine = create_engine('mysql+pymysql://root:admin@120.101.8.8:8763/3B10?charset=utf8')
    time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = ''' 
    SELECT * FROM `WEEK`;
    '''
   # df = pd.read_csv('test.csv',encoding='utf-8')      #read csv file
    df = pd.read_sql_query(sql, engine) 
    g1 = df[df['ID'].isin([name])]                  #find student id row and build as series
    
    df.iloc[g1.index,1] = 'v'                          #on time column
    df.iloc[g1.index,2] = ''                       #late    column
    df.iloc[g1.index,3] = ''                       #absence column
    #df.iloc[g1.index,4] = time1
    
    g1 = df[df['ID'].isin([name])]                  #status update
    #df.to_csv("test.csv",index=False,sep=',',encoding='utf-8-sig') #write in csv file 
    df.to_sql('WEEK', engine,if_exists='replace',index= False) 
    print(g1)
    
# 定義 late 函數
def late(name):
    engine = create_engine('mysql+pymysql://root:admin@120.101.8.8:8763/3B10?charset=utf8')
    sql = ''' 
    SELECT * FROM `TABLE 1`;
    '''
    #df = pd.read_csv('test.csv',encoding='utf-8') #read csv file
    df = pd.read_sql_query(sql, engine) 
    g2 = df[df['ID'].isin([name])]  #find student id series
    ontimeindex = g2.index.values[0]  #convert int64index to numpy array,and take the int value out
    check =  df['ONTIME'][ontimeindex]  #save the status,this value must be 'v' or NaN(numpy.nan)
    
    if check == 'v':                  #if check=='v',it represent the status 'ontime'
        print('this person has been check as ontime')
    else:
        df.iloc[g2.index,2] = 'v'     #late column
        df.iloc[g2.index,3] = ''  #absence column



    g2 = df[df['ID'].isin([name])] #status update
    df.to_sql('TABLE 1', engine,if_exists='replace',index= False) 
    #df.to_csv("test.csv",index=False,sep=',',encoding='utf-8-sig') #write in csv file
    #print(g2)
    
# 定義clear 函數
def clear():
    engine = create_engine('mysql+pymysql://root:admin@120.101.8.8:8763/3B10?charset=utf8')
    sql = ''' 
    SELECT * FROM `WEEK0`;
    '''
    df = pd.read_sql_query(sql, engine) 
    df.to_sql('WEEK', engine,if_exists='replace',index= False)
#------------------------------------------------------------------------------ 呼叫
name = str(output[0])
ontime(name)
#------------------------------------------------------------------------------ 重設
#clear()
#------------------------------------------------------------------------------ 關閉檔案
f.close()
f2.close