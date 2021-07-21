import pandas as pd
from sqlalchemy import create_engine
import time
# MySQL使用者名稱：root, password:88888888, port：3306,資料庫：csv_db
#engine = create_engine('mysql+pymysql://root:admin@120.101.8.8:8763/3B10')

# SQL查詢語句，選出表中的所有數據 
#sql = ''' 
#SELECT * FROM `WEEK`;
# '''

#on time
def ontime(name):
    engine = create_engine('mysql+pymysql://root:admin@120.101.8.8:8763/3B10')
    sql = ''' 
    SELECT * FROM `counter`;
    '''
    df = pd.read_sql_query(sql, engine)
    index = int(df.iloc[0,0])
    #index = index + 1
    df.iloc[0,0] = index
    df.to_sql('counter', engine,if_exists='replace',index= False)
    
    sql = ''' 
    SELECT * FROM `WEEK`;
    '''
   # df = pd.read_csv('test.csv',encoding='utf-8')      #read csv file
    time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    df = pd.read_sql_query(sql, engine) 
    g1 = df[df['ID'].isin([name])]                  #find student id row and build as series
    
    df.iloc[g1.index,2*index-1] = 'v'                          #on time column
    df.iloc[g1.index,2*index] = time1                     #absence column

    g1 = df[df['ID'].isin([name])]                  #status update
    #df.to_csv("test.csv",index=False,sep=',',encoding='utf-8-sig') #write in csv file 
    df.to_sql('WEEK', engine,if_exists='replace',index= False) 
    print(g1)
    
    
#@#---------------------------------------------------------------------

#late
def late(name):
    engine = create_engine('mysql+pymysql://root:admin@120.101.8.8:8763/3B10')
    sql = ''' 
    SELECT * FROM `WEEK`;
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
    df.to_sql('WEEK', engine,if_exists='replace',index= False) 
    #df.to_csv("test.csv",index=False,sep=',',encoding='utf-8-sig') #write in csv file
    print(g2)
    
#@#----------------------------------------------------------------------
#clear
def clear():
    engine = create_engine('mysql+pymysql://root:admin@120.101.8.8:8763/3B10')
    sql = ''' 
    SELECT * FROM `WEEK0`;
    '''
    df = pd.read_sql_query(sql, engine) 
    df.to_sql('WEEK', engine,if_exists='replace',index= False)
#
#test
#name = 'B0642021'
#ontime(name)
#late(name)
#clear()