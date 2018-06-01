#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 23:43:36 2018

@author: michel.fernandes
"""

from flask import Flask
from flask_restful import Api, request
import json
from sklearn.externals import joblib

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


    if key_check["result"]:

        if "model" in request.args:
            model = request.values["model"]

        lr_model_loaded = joblib.load('models/'+model+'.pkl')

        if "temp_max" in request.args:
            temp_max = request.values["temp_max"]

        if "precipt" in request.args:
            precipt = request.values["precipt"]

        if "weekend" in request.args:
            weekend = request.values["weekend"]

        predict_value = [[int(temp_max), int(precipt), int(weekend)]]

        predicted = lr_model_loaded.predict(predict_value)

        retorno["output"] = "Predicted consumption successful for model " + request.values["model"]
        retorno["value"] = predicted[0]

        return json.dumps(retorno)
    else:
        return json.dumps(key_check)

app.run(host="0.0.0.0", port=8080, debug=True)