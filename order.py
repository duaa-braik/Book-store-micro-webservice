from flask import Flask, request, json
import requests

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return 'Order Server'


############


@app.route('/purchase', methods=['POST', 'GET'])
def purchase():

    if request.method == 'POST':
        bookID = request.data
        bookID = bookID.decode()
        query_response = requests.get('http://127.0.0.1:5002/info', data=bookID)
        if query_response.json() is not None:
            update_response = requests.post('http://127.0.0.1:5002/update', data=bookID)
            return update_response.json()


 




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)