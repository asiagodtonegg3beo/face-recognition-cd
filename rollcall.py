#from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd


#app = Flask(__name__)
def statistics():
    f = open("index.txt","r")
    index = int(f.read())


    df = pd.read_csv('PROG.csv',encoding='utf-8') 

    df_init = pd.read_csv('PROG.csv',encoding='utf-8') #原始資料

    df_cnt = pd.read_csv('PROG.csv',encoding='utf-8')

    df_num = pd.read_csv('PROG.csv',encoding='utf-8')

    for col in df.columns: #去掉'Time'
        if col.isdigit()==False and col != 'ID':
            del df[col],df_cnt[col],df_num[col]
     

    for i in range(0,df.shape[1]-1):        #'v' 改成 '1'
        for index, row in df.iterrows():
    # Access any cell in row and set it to 0
    # Check if value in cell fulfils condition
            if df.loc[index,str(i)] == 'v':
                df.loc[index,str(i)] = 1


#df_num = df #只有簽到次數資料,無時間



#print(df_num)
#print(df.describe())
#出席率
    count = df_cnt.count() #'每次到課人數'
    total = count['ID'] #'總人數'
    count/=total
    percent = count.apply(lambda x: format(x, '.0%'))
    df_per = percent.to_frame()
    df_per = df_per[1:]
    df_per = df_per.T
    df_per.insert(0,'次數','出席率')


#%%-----------------------------------------------轉置
    df_t = df.set_index('ID').rename_axis(None).T
    df_t = df_t.count() #'全班到課總次數'
    df_t = df_t.to_frame()
    df_t = df_t.T
    df_t.insert(0,'學號','出席次數')
    
    return df_init,df_num,df_per,df_t

'''
@app.route('/', methods=("POST", "GET"))
def html_table():

    return render_template('statistics.html',  tables=[df_init.to_html(classes='fl-table',index=False,na_rep='')],tables2=[df_num.to_html(classes='fl-table',index=False,na_rep='')],tables3=[df_per.to_html(classes='fl-table',index=False)],tables4=[df_t.to_html(classes='fl-table',index=False)])



if __name__ == '__main__':
    app.run(host='0.0.0.0')
'''