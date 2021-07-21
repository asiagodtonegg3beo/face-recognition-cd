from flask import Flask, render_template,request,flash,redirect,url_for
import rollcall as ro
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
app = Flask(__name__)
app.secret_key = "Your Key"
@app.route("/")
def main():
    return render_template("control.html")
@app.route("/b",methods=['GET', 'POST'])
def encoding():
    if request.method=='POST':
        if request.form.get('start'):
            #f = open("index.txt","r")
            #index = int(f.read())
            #index = index + 1
            #f.write(str(index))
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
            df = pd.read_sql_query(sql, engine)
            df[str(index)]=''
            df['TIME'+str(index)]=''
            df.to_sql('WEEK', engine,if_exists='replace',index= False)

            f = open("state.txt","w+")
            f.write(str(1))
            f.close()

            flash('開始點名,本次為第%d次點名,請在老師規定時間內進行簽到!'%index,'success')

            return render_template("control.html")
        if request.form.get('exit'):
            f = open("state.txt","w+")
            f.write(str(0))
            f.close()
            flash('結束點名','danger')
            return render_template("control.html")

@app.route("/statistics",methods=['GET', 'POST'])
def statistics():
    table = ro.statistics()
    df_init = table[0]
    df_num = table[1]
    df_per = table[2]
    df_t = table[3]
    return render_template('statistics.html',  tables=[df_init.to_html(classes='fl-table',index=False,na_rep='')],tables2=[df_num.to_html(classes='fl-table',index=False,na_rep='')],tables3=[df_per.to_html(classes='fl-table',index=False)],tables4=[df_t.to_html(classes='fl-table',index=False)])

@app.route("/camera",methods=['GET', 'POST'])
def camera():
    return render_template("camera.html")
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)
