#importing libraries
import os
import numpy as np
import flask
import pickle
from flask import Flask, render_template, request

reg_model = pickle.load(open("checkpoints\\reg_model_1vars.pkl", 'rb'))
class_model = pickle.load(open("checkpoints\\class_model_3vars.pkl", 'rb'))


#creating instance of the class
app=Flask(__name__)

#to tell flask what url shoud trigger the function index()
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

def ValuePredictor(to_predict_list, shape):
    to_predict = np.array(to_predict_list).reshape(1, shape)

    if shape == 3:
        loaded_model = class_model
    elif shape == 1:
        loaded_model = reg_model
    else:
        raise ValueError
    
    result = loaded_model.predict(to_predict)
    return result[0]

def class_prediction(result):
    if int(result)==0:
        prediction='Loser'
    elif int(result)==1:
        prediction='Winner'
    else:
        prediction=f'{int(result)} No-definida'
    
    return prediction

@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':

        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())

        to_predict_list = list(filter(None, to_predict_list))

        try:
            to_predict_list = list(map(float, to_predict_list))

            if len(to_predict_list) == 3:
                result = ValuePredictor(to_predict_list, 3)
                prediction = "Match Win or Loss: "+class_prediction(result)

            elif len(to_predict_list) == 1:
                result = ValuePredictor(to_predict_list, 1)
                prediction = "Team Starting Equipment Value: "+"%.0f" % result
            else:
                raise ValueError

        except ValueError as e:
            prediction=f'Error en el formato de los datos \n {e}'

        return render_template("result.html", prediction=prediction)


if __name__=="__main__":

    app.run(port=5001)