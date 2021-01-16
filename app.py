#import flask web framework
from flask import Flask,render_template,request
import os
#import keras library
import keras
#to load our saved h model, import load_model package from keras
from keras.models import load_model
from flask import Flask, render_template, url_for, Response,redirect,url_for
#import numpy and np is an alias pointing to numpy
import numpy as np
#importing array from numpy library 
from numpy import array
#import tensorflow and tf is an alias pointing to tensorflow
import tensorflow as tf
#import pandas and pd is an alias pointing to pandas
import pandas as pd
global graph
graph = tf.get_default_graph()
from numpy import array

#create function to get the data from nodered
def getdata():
    import requests
    import json 
    #get the nodered simulation data using API
    url = "https://node-red-bpdoj-2021-01-15.eu-gb.mybluemix.net/data"
    x = requests.get(url)
    print(x.text)
    #parsing the json data using json.loads
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
#create constructor to flask
app=Flask(__name__)
#loading h5 model using load_model class
model = load_model('Energy.h5')

#create check function to check the email ID from the user.csv
#will check email once after registration
def check(email):
    df=pd.read_csv('user.csv')
    if email in list(df['Email']):
        return df.iloc[list(df['Email']).index(email),3]
    else:
        return "success"
#The route() function of the Flask class,which tells the application which URL should call the associated function.
@app.route('/')
def login():
	#render login.html using render_template
    return render_template("login.html")
##The route() function of the Flask class,which tells the application which URL should call the associated function.
@app.route('/afterlogin', methods = ['POST', 'GET'])
def afterlogin():
	#request the username and password from the user.csv which we registered
    em=request.form['uname']
    ps=request.form['psw']
    #if the email is not matched returning the below statement
    if check(em)!=ps:
        return render_template("login.html",pred="You have entered wrong password")
    elif(check(em)=="success"):
    	#if it it matched rendered the message
        return render_template("login.html",pred="You have not registered please register.")
    else:
        return redirect(url_for('homepage'))
#to register account create an url
@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/afterreg', methods = ['POST', 'GET'])
def afterreg():
	#read the csv file using read_csv class
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
#creating url that redirect the homepage
@app.route('/homepage')
def homepage():
    return render_template("index.html")
#creating the predict url
@app.route('/predict', methods = ['POST', 'GET'])
def worky():
	#requesting the values/ manual data
    x_test = array([int(x) for x in request.form.values()])
    print('OK')
    #reshaping the data into 3 dimension using reshape
    test_input = x_test.reshape((1, 1, 12))
    # a session allows executing graphs or part of graphs. 
    #It allocates resources (on a single or multiple machines) for that and holds the actual values of intermediate results and variables.
    with graph.as_default():
    	#giving test_input to the model to predict the energy usage
        preds = model.predict(test_input)
        output = np.round(preds[0][0], 4)
        print(output)
        #displying the result on result.html
        return render_template("result.html", message=": "+ str(output))
        
#creating /sensor to redirect or to call simulation values
@app.route('/sensor')
def sensor():
    return render_template("base.html")
@app.route('/ownvalues', methods = ['POST', 'GET'])
def own():
	#using getdata function
    a = getdata()
    #converting values into numpy array
    data=np.array(a)
    print(a)
    print('OK')
    #reshaping the simulation data
    test_input = data.reshape((1, 1, 12))
    with graph.as_default():
    	#giving input to model
        preds = model.predict(test_input)
        output = np.round(preds[0][0], 4)
        print(output)
        print(a[0],a[1])
        #displaying the result on result1.html page with each appliance
        return render_template("result1.html", dishwasher=": "+ str(a[0]),Home_Office=": "+ str(a[1]),Fridge=": "+ str(a[2]),Wine_Cellar=": "+ str(a[3]),Garage_Door=": "+ str(a[4]),Barn=": "+ str(a[5]),Well=": "+ str(a[6]),Microwave=": "+ str(a[7]),Living_room=": "+ str(a[8]),Solar=": "+ str(a[9]),Total_Furance=": "+ str(a[10]),Avg_Kitchen=": "+ str(a[11]), message=": "+ str(output))
port = os.getenv('VCAP_APP_PORT', '8080')
#Python program to use main for function call.
if __name__=='__main__':
    app.secret_key = os.urandom(12)
    #specifying port number and host
    app.run(debug=True,host='0.0.0.0', port=port)

        