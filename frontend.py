import json
from flask import Flask, jsonify, redirect, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search_template():
    return render_template('search.html')


@app.route('/search/data', methods=['GET'])
def search_data():
    topic = request.args['topic']
    return redirect('/search/' + topic)

@app.route('/search/<topic>')
def search_result(topic):
    response = requests.get('http://127.0.0.1:5002/search', data=topic)
    return json.dumps(response.json())

####################################################################################


@app.route('/info')
def info_template():
    return render_template('info.html')

@app.route('/info/data', methods=['GET'])
def info_data():
    bookID = request.args['bookid']
    return redirect('/info/' + bookID)

@app.route('/info/<bookid>')
def info_result(bookid):
    response = requests.get('http://127.0.0.1:5002/info', data=bookid)
    return response.json()

##########################################################

@app.route('/purchase')
def purchase_template():
    return render_template('purchase.html')

@app.route('/purchase/', methods=['POST'])
def purchase_data():
    book_id = request.form['bookid']
    return redirect('/purchase/' + book_id)

@app.route('/purchase/<bookid>')
def purchase_result(bookid):
    response = requests.post('http://127.0.0.1:5003/purchase', data=bookid)
    response_data = response.json()
    return f"You bought the book of ID: {response_data['id']}, and there are {response_data['items']} remaining copies"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)