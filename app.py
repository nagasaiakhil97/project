from flask import Flask,render_template,request
import os
import keras
from keras.models import load_model
from flask import Flask, render_template, url_for, Response,redirect,url_for
import numpy as np
from numpy import array
import tensorflow as tf
import pandas as pd
global graph
graph = tf.get_default_graph()
from numpy import array

def getdata():
    import requests
    import json 
    url = "https://node-red-bpdoj-2021-01-15.eu-gb.mybluemix.net/data"
    x = requests.get(url)
    print(x.text)
    data = json.loads(x.text)
    Dishwasher = data["Dishwasher"]
    Home_office = data["Home_office"]
    Fridge = data["Fridge"]
    Wine_Cellar = data["Wine_Cellar"]
    Garage_Door = data["Garage_Door"]
    Barn = data["Barn"]
    Well = data["Well"]
    Microwave = data["Microwave"]
    Living_room = data["Living_room"]
    Solar = data["Solar"]
    Total_Furance = data["Total_Furance"]
    Avg_Kitchen = data["Avg_Kitchen"]
    return [float(Dishwasher),float(Home_office),float(Fridge),float(Wine_Cellar),float(Garage_Door),float(Barn),float(Well),float(Microwave),float(Living_room),float(Solar),float(Total_Furance),float(Avg_Kitchen)]

app=Flask(__name__)

model = load_model('Energy.h5')

def check(email):
    df=pd.read_csv('user.csv')
    if email in list(df['Email']):
        return df.iloc[list(df['Email']).index(email),3]
    else:
        return "success"
@app.route('/')
def login():
    return render_template("login.html")

@app.route('/afterlogin', methods = ['POST', 'GET'])
def afterlogin():
    em=request.form['uname']
    ps=request.form['psw']
    if check(em)!=ps:
        return render_template("login.html",pred="You have entered wrong password")
    elif(check(em)=="success"):
        return render_template("login.html",pred="You have not registered please register.")
    else:
        return redirect(url_for('homepage'))

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/afterreg', methods = ['POST', 'GET'])
def afterreg():
    df=pd.read_csv('user.csv')
    x = [x for x in request.form.values()]
    if x[1] in list(df['Email']):
        return render_template("register.html",pred="You have already registred, please login")
    else:
        df=pd.read_csv('user.csv')
        samp=pd.DataFrame([[x[0],x[1],x[2],x[3]]],columns=['Name', 'Email', 'Phone', 'Password'])
        df=df.append(samp)
        print(df)
        df.to_csv('user.csv')
        return render_template("register.html",pred="You have succesfully registred, please login")

@app.route('/homepage')
def homepage():
    return render_template("index.html")

@app.route('/predict', methods = ['POST', 'GET'])
def worky():
    x_test = array([int(x) for x in request.form.values()])
    print('OK')
    test_input = x_test.reshape((1, 1, 12))
    with graph.as_default():
        preds = model.predict(test_input)
        output = np.round(preds[0][0], 4)
        print(output)
        return render_template("result.html", message=": "+ str(output))
        

@app.route('/sensor')
def sensor():
    return render_template("base.html")
@app.route('/ownvalues', methods = ['POST', 'GET'])
def own():
    a = getdata()
    data=np.array(a)
    print(a)
    print('OK')
    test_input = data.reshape((1, 1, 12))
    with graph.as_default():
        preds = model.predict(test_input)
        output = np.round(preds[0][0], 4)
        print(output)
        print(a[0],a[1])
        return render_template("result1.html", dishwasher=": "+ str(a[0]),Home_Office=": "+ str(a[1]),Fridge=": "+ str(a[2]),Wine_Cellar=": "+ str(a[3]),Garage_Door=": "+ str(a[4]),Barn=": "+ str(a[5]),Well=": "+ str(a[6]),Microwave=": "+ str(a[7]),Living_room=": "+ str(a[8]),Solar=": "+ str(a[9]),Total_Furance=": "+ str(a[10]),Avg_Kitchen=": "+ str(a[11]), message=": "+ str(output))
port = os.getenv('VCAP_APP_PORT', '8080')
if __name__=='__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=port)

        