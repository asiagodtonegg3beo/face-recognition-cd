import os
basepath = os.path.join(os.path.dirname(__file__), 'static','uploads','B0642016')
dirs=[f for f in os.listdir(os.path.join(basepath)) if os.path.isdir(os.path.join(basepath,f))]
for f in dirs:
    print("目錄：", f)
dict2={} #record all folder has what number name


