from flask import Flask, request, json
import requests

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return 'Order Server'
############

round_purchase = True

def round_robin_purchase():
    global round_purchase
    round_purchase = not round_purchase



@app.route('/purchase', methods=['POST', 'GET'])
def purchase():
    
    round_robin_purchase()

    if request.method == 'POST':
        bookID = request.data
        bookID = bookID.decode()

        if round_purchase == True:
            print('from catalog1')
            query_response = requests.get('http://127.0.0.1:5002/info', data=bookID)
        else:
            print('from catalog2')
            query_response = requests.get('http://127.0.0.1:5003/info', data=bookID)

        if query_response.json() is not None:

            if round_purchase == True:
                print('from catalog1')
                update_response = requests.post('http://127.0.0.1:5002/update', data=bookID)#{title, items}
            else:
                print('from catalog2')
                update_response = requests.post('http://127.0.0.1:5003/update', data=bookID) 
            
            requests.post('http://127.0.0.1:5010/update', data=update_response)#updating the cache
            return update_response.json()





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)