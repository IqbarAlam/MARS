import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask,render_template,jsonify,request
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get('MONGO_DB_URI')
DB_NAME =  os.environ.get('DB_NAME')

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mars',methods=['GET'])
def web_mars_get():
    orders = list(db.Mars.find({},{'_id':False}))
    return jsonify({'orders': orders})

@app.route('/mars',methods=['POST'])
def web_mars_post():
    name_of_buyer = request.form['name']
    address = request.form['address']
    size = request.form['size']
    print(name_of_buyer,' | ',address,' | ',size)
    doc = {
        'name': name_of_buyer,
        'address': address,
        'size': size
    }
    db.Mars.insert_one(doc)
    return jsonify({'msg': 'Success'})

if __name__=='__main__':
    app.run('0.0.0.0',5000,debug=True)