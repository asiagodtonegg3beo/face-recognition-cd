from flask import Flask, render_template,request
import imp
import subprocess
app = Flask(__name__)
@app.route("/main")
def main():
    return render_template("main.html")
@app.route("/b",methods=['GET', 'POST'])
def encoding():
    if request.method=='POST':
        if request.form.get('encoding'):
            imp.load_source('a','extract_embeddings.py')
            return "<h1>特徵值編碼完成</h1>"
        if request.form.get('training'):
            imp.load_source('b','train_model.py')
            return "<h1>訓練完成</h1>"
        if request.form.get('recognition'):
            a = subprocess.run('bash -c "source activate 3B10 && python webstreaming.py; python -V"', shell=True)
            return "<h1>開始串流</h1>"
        
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)
