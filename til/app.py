from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.dq4uizr.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/post')
def post():
    return render_template('index2.html')

@app.route('/rank')
def rank():
    return render_template('index3.html')

@app.route("/show", methods=["GET"])
def til_get():
    til_list = list(db.til.find({},{'_id':False}))
    return jsonify({'tils': til_list})

@app.route("/til", methods=["POST"])
def blog_post():
    name_receive = request.form['name_give']
    vlog_url_receive = request.form['vlog_url_give']
    title_receive = request.form['title_give']
    img_receive = request.form['img_give']
    comment_receive = request.form['comment_give']
    desc_receive = request.form['desc_give']
    count = list(db.til.find({},{'_id':False}))
    num = len(count) + 1

    doc = {
        'name': name_receive,
        'vlog_url': vlog_url_receive,
        'title': title_receive,
        'img': img_receive,
        'comment': comment_receive,
        'desc_receive': desc_receive,
        'like_num': num,
        'like': 0
    }

    db.til.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

@app.route("/like", methods=["POST"])
def like():
    like_receive = request.form['like_give']

    db.til.update_one({'like_num': int(like_receive)}, {'$inc': {'like': 1}})
    return jsonify({'msg': '좋아요 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)