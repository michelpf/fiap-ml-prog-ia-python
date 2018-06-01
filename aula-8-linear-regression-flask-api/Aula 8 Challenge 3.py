#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criar formas de validar os dados dos parâmetros de entrada e criar uma forma de autenticação
por meio de parâmetros do header com as chaves key e secret
"""

from flask import Flask
from flask_restful import Api, request
import json
from sklearn.externals import joblib
import string
import random

app = Flask("api-ml")
api = Api(app)

def check_key():
    
    retorno = {}
    
    api_key = request.headers.get('key')
    api_secret = request.headers.get('secret')

    retorno["output"] = "Autenticação com sucesso"
    retorno["result"] = True

    if not (api_key == "XFac-7m-7?CjphABgfyAYGAea2E_U7_qD8AP2-FW" and
        api_secret == "UQU8?5gmd+SgGPLtM&*B&x+R3s-4Z8bqAv+aZC6k"):
        retorno["output"] = "API Key ou API Secret inválidos"
        retorno["result"] = False

    return retorno

@app.route("/hello", methods=["GET"])
def hello():
    return "Hello World"


@app.route("/predict", methods=["GET"])
def predict():

    retorno = {}
    key_check = {}

    key_check = check_key()

    if key_check["result"]:

        if "model" in request.args:
            model = request.values["model"]
        else:
            retorno["error"] = "model is missing"
            return json.dumps(retorno)

        lr_model_loaded = joblib.load('models/'+model+'.pkl')

        if "temp_max" in request.args:
            temp_max = request.values["temp_max"]
        else:
            retorno["error"] = "temp_max is missing"
            return json.dumps(retorno)

        if "precipt" in request.args:
            precipt = request.values["precipt"]
        else:
            retorno["error"] = "precipt is missing"
            return json.dumps(retorno)

        if "weekend" in request.args:
            weekend = request.values["weekend"]
        else:
            retorno["error"] = "precipt is missing"
            return json.dumps(retorno)

        if temp_max.isnumeric() is False:
            retorno["error"] = "temp_max is not a number"
            return json.dumps(retorno)

        if precipt.isnumeric() is False:
            retorno["error"] = "precipt is not a number"
            return json.dumps(retorno)

        if weekend.isnumeric() is False or int(weekend) not in [0, 1]:
            retorno["error"] = "weekend is not a number or is not 0 for non weekend or 1 for weekend"
            return json.dumps(retorno)

        predict_value = [[int(temp_max), int(precipt), int(weekend)]]

        predicted = lr_model_loaded.predict(predict_value)

        retorno["output"] = "Predicted consumption successful for model " + request.values["model"]
        retorno["value"] = predicted[0]

        return json.dumps(retorno)
    else:
        return json.dumps(key_check)

def get_random_string():
    size = 6
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


@app.route("/train", methods=["POST"])
def train():

    retorno = {}
    key_check = {}

    key_check = check_key()

    if key_check["result"]:

        if "file" in request.files:
            f = request.files['file']
            file_name = get_random_string() + '_' + f.filename
            f.save("models/" + file_name)
        else:
            retorno["error"] = "training file is missing"
            return json.dumps(retorno)

        retorno["model"] = file_name.split(".")[0]
        retorno["output"] = "Model file upload succesfully"

        return json.dumps(retorno)
    else:
        return json.dumps(key_check)

app.run(host="0.0.0.0", port=8080, debug=True)
