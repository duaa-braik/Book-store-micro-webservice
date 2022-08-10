import json
from flask import Flask, jsonify, redirect, render_template, request
import requests
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)


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
    
    response = requests.get('http://127.0.0.1:5010/search', data=topic)
    responseList = json.dumps(response.json())
    if len(responseList) > 2 :
        return responseList
    else:
        return 'the book(s) you\'re searching for is not available'
    

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
    response = requests.get('http://127.0.0.1:5010/info', data=bookid)
    
    if response.json() != {}:
        return response.json()
    else:
        return 'the book you\'re searching for is not available'

##########################################################

@app.route('/purchase')
def purchase_template():
    return render_template('purchase.html')

@app.route('/purchase/', methods=['POST'])
def purchase_data():
    book_id = request.form['bookid']
    return redirect('/purchase/' + book_id)


round_purchase = True

def round_robin_purchase():
    global round_purchase
    round_purchase = not round_purchase


@app.route('/purchase/<bookid>')
def purchase_result(bookid):

    round_robin_purchase()

    if round_purchase == True:
        print('from order1')
        response = requests.post('http://127.0.0.1:5004/purchase', data=bookid)
    else:
        print('from order2')
        response = requests.post('http://127.0.0.1:5005/purchase', data=bookid)

    response_data = response.json()
    return f"You bought the book: {response_data['title']}, and there are {response_data['items']} remaining copies"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)