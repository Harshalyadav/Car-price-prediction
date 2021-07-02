from flask import Flask, render_template, request, jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app=Flask("car_model")
model = pickle.load(open('car-price-prediction.pkl', 'rb'))

@app.route('/',methods=['GET'])

def home():
  return render_template('index.html')

standard = StandardScaler()

@app.route('/predict',methods=['POST'])

def predict():
    Fuel_type_Diesel=0

    if request.methods == "POST":
        Year=int(request.form['Year'])
        Year=2021-Year
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='petrol'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0

        elif(Fuel_Type_Petrol =='Diesel'):
            Fuel_Type_Diesel=1
            Fuel_Type_Petrol=0

        else:
            Fuel_Type_Petrol==0
            Fuel_type_Diesel==0


        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
                Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0

        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
           Transmission_Mannual=1
        else:
            Transmission_Mannual=0

        prediction=model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Petrol,Fuel_type_Diesel,Seller_Type_Individual,Transmission_Mannual]])

        output=round(prediction[0],2)


        if(output<0):
           return render_template('index.html',prediction_text="Sorry you cannot sell this car")


        else:
          return render_template('index.html',prediction_text="You Can Sell the Car at {} lakhs".format(output))
        
    #html form to be displayed on screen when no values are inserted; without any output or prediction
    else:
      return render_template('index.html')


if __name__ == '__main__':

    app.run(debug=True)