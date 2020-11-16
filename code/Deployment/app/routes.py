from flask import render_template, current_app
from app import app
from app import connection
import pandas as pd
from app.BiLSTM_15Classes import prediction as prediction15
from app.BiLSTM_6Classes import prediction as prediction6
from app.BiLSTM_3Classes import prediction as prediction3



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Global Terrorism Analysis')

@app.route('/exploration')
def exploration():
    return render_template('exploration.html')

@app.route('/model')
def model():
    return render_template('model.html')


@app.route('/get_prediction/<sentence>/<numClasses>', methods=['GET'])
def get_prediction(sentence, numClasses = 15):
    print("in get prediction ", sentence, numClasses)
    if numClasses == "15":
        output = prediction15(sentence)
    elif numClasses == "6":
        output = prediction6(sentence)
    elif numClasses == "3":
        output = prediction3(sentence)

    print(output)

    return str(output)
