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

@app.route("/ranking", methods=["GET"])
def rank_get():
    rank_list = list(db.til.find({},{'_id':False}))
    return jsonify({'tils': rank_list})

@app.route("/til", methods=["POST"])
def blog_post():
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    count = list(db.til.find({},{'_id':False}))
    num = len(count) + 1

    doc = {
        'name': name_receive,
        'address': address_receive,
        'num': num,
        'like': 0
    }

    db.til.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

@app.route("/like", methods=["POST"])
def like():
    num_receive = request.form['num_give']

    db.til.update_one({'num': int(num_receive)}, {'$inc': {'like': 1}})
    return jsonify({'msg': '좋아요 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5003, debug=True)