from flask import Flask, render_template, request
#from model import calculate_similarity
from model2 import calculate_similarity1
from model3 import calculate_similarity2
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nyu', methods=["GET", "POST"])
def nyu():
    if request.method == "GET":
        return render_template('nyuryoku.html')
    elif request.method == "POST":
        # 追加箇所
        text = request.form["input_text"]
        appropiate,advise=calculate_similarity1(text)
        return render_template('kekka.html',appropiate=appropiate,advise=advise)
    

@app.route('/nyu2')
def nyu2():
    return render_template('kekka.html')

@app.route('/eng', methods=["GET", "POST"])
def eng():
    if request.method == "GET":
        return render_template('eng.html')
    elif request.method == "POST":
        # 追加箇所
        txt = request.form["input_text"]
        ap,ad,adj=calculate_similarity2(txt)
        return render_template('engf.html',ap=ap,ad=ad,adj=adj)


@app.route('/eng2')
def eng2():
    return render_template('engf.html')

if __name__ == "__main__":
    app.run(port=8000,debug=True)