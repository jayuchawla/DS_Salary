import json
import requests

def read_input():
    with open('data_input.txt', 'r') as f:
        line = f.readline()
        values = line.split(' = ')[1].strip().split(', ')
        values = [float(v) for v in values]
        return values



URL = 'http://127.0.0.1:5000/predict'
HEADERS = {'Content-Type':'application/json'}
DATA = {'input':read_input()}

r = requests.get(url=URL, headers=HEADERS, json=DATA)
print(r.json())

