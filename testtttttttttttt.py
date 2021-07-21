import numpy as np
import pandas as pd

df_init = pd.read_csv('PROG.csv',encoding='utf-8')
df_id = df_init['ID']
df_init = df_init.drop(['ID'], axis=1)

'''
f = open("index.txt","r")
index = int(f.read())
df_init[str(index)]=np.nan
df_init['TIME'+str(index)]=np.nan
'''

drop_col = 0
df_init = df_init.drop([str(drop_col),'TIME'+str(drop_col)], axis=1)
#f = open("index.txt","r")
index = 13
index = index-1
new_col = []
for i in range(0, index):
    for j in range(i,i+1):
        new_col += [i]
        new_col += ['TIME'+str(i)]

df_init.columns = new_col
df_init.insert(0,'ID',df_id)

df_rename = df_init

'''
index = 5
sum = []
for i in range(1, index+1):
    for j in range(i):
        sum += [i]
        sum += ['TIME'+str(i)]

'''