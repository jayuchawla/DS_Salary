import pickle
import flask
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

def load_models():
    serialized_model_file = 'models/final_ds_salary_model.pickle'
    with open(serialized_model_file, 'rb') as pickled:
        model = pickle.load(pickled)
    return model

# @app.route('/values', methods=['GET'])
def read_input():
    with open('data_input.txt', 'r') as f:
        line = f.readline()
        values = line.split(' = ')[1].strip().split(', ')
        values = [float(v) for v in values]
        return values


@app.route('/predict', methods = ['GET'])
def predict():
    # response = json.dumps({'response': 'hello'})
    print('json: ' + str(request.get_json()))
    # X = read_input()
    X = request.get_json()['input']
    model = load_models()
    prediction = model.predict([[X]][0])
    response = json.dumps({'predicted_value':list(prediction)[0]})
    return response, 200
    # return 'e',200


if __name__ == '__main__':
    # read_input('data_input.txt')
    application.run(debug=True)