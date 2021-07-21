from flask import Flask, render_template,request,flash,redirect,url_for
from werkzeug.utils import secure_filename
import imp
import os
import zz
import sys
import threading
app = Flask(__name__)
app.secret_key = "Your Key"
def job():
    imp.load_source('c','webstreaming1.py')
@app.route("/main")
def index():
    return render_template("main.html")
@app.route("/b",methods=['GET', 'POST'])
def encoding():
    if request.method=='POST':
        if request.form.get('encoding'):
            imp.load_source('a','extract_embeddings.py')
            flash('特徵值編碼完成','success')
            return render_template("main.html")
        if request.form.get('training'):
            imp.load_source('b','train_model.py')
            flash('訓練完成','success')
            return render_template("main.html")
        if request.form.get('recognition'):
            flash('開始串流,請點選下方串流網址','success')
            t = threading.Thread(target = job)
            t.start()
            return render_template("main.html")
#%%
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        if zz.su() >= 20:
            f = request.files['file']
            basepath = os.path.dirname(__file__) # 當前檔案所在路徑
            upload_path = os.path.join(basepath, 'dataset/B0642021',secure_filename(f.filename)) #注意：沒有的資料夾一定要先建立，不然會提示沒有該路徑
            flash('上傳失敗! 照片已達上限','danger')
            return render_template('upload.html',summ=zz.su())
        else:
            f = request.files['file']
            basepath = os.path.dirname(__file__) # 當前檔案所在路徑
            upload_path = os.path.join(basepath, 'dataset/B0642021',secure_filename(f.filename)) #注意：沒有的資料夾一定要先建立，不然會提示沒有該路徑
            f.save(upload_path)
            flash(u'上傳成功!','success')
            return render_template('upload.html',summ=zz.su())
    return render_template('upload.html',summ=zz.su())
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)
