from flask import Flask, render_template,request,flash,redirect,url_for
import rollcall as ro
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:admin@120.101.8.8:8763/3B10')
sql = ''' 
SELECT * FROM `counter`;
'''
df = pd.read_sql_query(sql, engine)
index = int(df.iloc[0,0])
index = 6
df.iloc[0,0] = index
df.to_sql('counter', engine,if_exists='replace',index= False)
