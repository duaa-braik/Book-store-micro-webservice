import redis 
import json
from flask import Flask, request
import requests

app = Flask(__name__)

round_search = True
round_info = True

def round_robin_search():
    global round_search 
    round_search = not round_search

def round_robin_info():
    global round_info 
    round_info = not round_info    

@app.route('/search', methods=['GET', 'POST'])
def search():
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    data = request.data
    round_robin_search()
    

    if redis_client.exists(data) == 1:

        redis_result = redis_client.get(data)
        print('data is found in cache')
        return redis_result

    else:
        print('not found in cache, data is brought from server')
        if round_search == True:
            print('from catalog1')
            response = requests.get('http://127.0.0.1:5002/search', data=data)
        else:
            print('from catalog2')
            response = requests.get('http://127.0.0.1:5003/search', data=data)                
        
        redis_client.set(data, json.dumps(response.json()))
        redis_client.expire(data, 10)
        
        return json.dumps(response.json())
    

##############################################################################

@app.route('/info', methods=['GET', 'POST'])
def info():
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    data = request.data
    round_robin_info()


    if redis_client.exists(data) == 1:
        redis_result = redis_client.get(data)
        print('data is found in cache')
        return redis_result
    
    else:
        print('not found in cache, data is brought from server')
        if round_info == True:
            print('from catalog1')
            response = requests.get('http://127.0.0.1:5002/info', data=data)
            
        else:
            print('from catalog2')
            response = requests.get('http://127.0.0.1:5003/info', data=data)
            
        redis_client.set(data, json.dumps(response.json()))
        return json.dumps(response.json())

        

    

@app.route('/update', methods=['GET', 'POST'])
def update():

    if request.method == 'POST':
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        data = request.data
        data_json = json.loads(data)
        data_str = data.decode()
        key = data_json['id']
        value = int(key)
        redis_client.mset({value:data_str})
        return {'status': 200}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010)