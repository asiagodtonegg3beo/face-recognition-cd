import pandas as pd
from sqlalchemy import create_engine
import time
def indexplus_1():
    f = open("index.txt","r")
    index = int(f.read())
    index = index + 1
    print(index)
    f.close()
    f = open("index.txt","w")
    f.write(str(index))
    f.close()
    return index
    
def init():
    f = open("index.txt","w")
    f.write(str(0))
    f.close()

#on time
def ontime(name):
    engine = create_engine('mysql+pymysql://root:88888888@192.168.0.2:3306/test?charset=utf8')
    time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    f = open("index.txt","r")
    index = int(f.read())
    sql = ''' 
    SELECT * FROM `prog`;
    '''
   # df = pd.read_csv('test.csv',encoding='utf-8')      #read csv file
    df = pd.read_sql_query(sql, engine) 
    g1 = df[df['ID'].isin([name])]                  #find student id row and build as series
    
    df.iloc[g1.index,2*index+1] = 'v'                          #on time column
    df.iloc[g1.index,2*index+2] = time1                     #absence column

    g1 = df[df['ID'].isin([name])]                  #status update
    #df.to_csv("test.csv",index=False,sep=',',encoding='utf-8-sig') #write in csv file 
    df.to_sql('prog', engine,if_exists='replace',index= False) 
    print(g1)
    
#@#---------------------------------------------------------------------




#%%---------------------------------------------------test
print(indexplus_1())
#init()

#name = 'B0642016'
#ontime(name)


















