from datetime import datetime
import csv
import re
import pandas as pd
from flask import Flask, jsonify, request, make_response
import math

#Instansierer flask (til API hosting)
app = Flask(__name__)
app.config["DEBUG"] = True
#Flask, når dataen skal hostes, skal den sorteres slik som dataen er i listen
app.config['JSON_SORT_KEYS'] = False


df = pd.read_csv('eurofxref-hist.csv')
#print(df)

nan_value = float("NaN")
df.replace("1", nan_value, inplace=True)
headers = list(df.columns.values)

headersWithoutDate = headers[1:42]
country_long=""
length = len(df)
list1=[]
cleanedlist=[]

for i in headersWithoutDate:
    for x in range(0,length):
        spot = df[i].iloc[x]
        date= df["Date"].iloc[x]
        currency_short = str(i)
        temp_list=(currency_short, spot, date)
        list1.append(temp_list)

for transaction in list1:
    if math.isnan(transaction[1])==False:
        cleanedlist.append(transaction)
        #print("NAAAAAAAAAN")



@app.route('/')
def home():
    return 'Hello World'

@app.route('/unprotected')
def unprotected():
	return jsonify(cleanedlist)


@app.route('/FreeCurrencyConverter', methods=['GET'])
def api_base():
    # Check if an ID was provided as part of the URL.
    #Ser om en ID var gitt som parameter i URL. Hvis den er, så assign den til en variabel. Hvis ikke display error.
        if 'base' in request.args:
            id = str(request.args['base'])
        else:
            return "Error: No base field provided. Please specify an base."

        # Create an empty list for our results
        #Oppretter et tomt array for resultatene
        results = []

        #Looper gjennom dataen og finner matchene resultater med vat_number
        for transaction in cleanedlist:
            if transaction[0] == id:
                print("Succes")
                print(transaction)
                results.append(transaction)

        #Bruker JSONIFY funksjonen fra flask til å konverter listen til JSON format
        return jsonify(results)

@app.route('/FreeCurrencyConverter/period', methods=['GET'])
def api_date():
    # Check if an ID was provided as part of the URL.
    #Ser om en ID var gitt som parameter i URL. Hvis den er, så assign den til en variabel. Hvis ikke display error.
        if 'date' in request.args:
            date = str(request.args['date'])
        else:
            return "Error: No base field provided. Please specify an base."
        

        # Create an empty list for our results
        #Oppretter et tomt array for resultatene
        results = []

        #Looper gjennom dataen og finner matchene resultater med vat_number
        for transaction in cleanedlist:
            if transaction[2] == date:
                print("Succes")
                results.append(transaction)

        #Bruker JSONIFY funksjonen fra flask til å konverter listen til JSON format
        return jsonify(results)


#http://127.0.0.1:5000/FreeCurrencyConverter/calculation?base=NOK&symbol=DKK&date=2021-05-07
@app.route('/FreeCurrencyConverter/calculation', methods=['GET'])
def api_converter():
    # Check if an ID was provided as part of the URL.
    #Ser om en ID var gitt som parameter i URL. Hvis den er, så assign den til en variabel. Hvis ikke display error.
        if 'base' and 'symbol' and 'date' in request.args:
            base = str(request.args['base'])
            symbol = str(request.args['symbol'])
            date = str(request.args['date'])

        else:
            return "Error: No base field provided. Please specify an base."
        
        

        # Create an empty list for our results
        #Oppretter et tomt array for resultatene
        results = []
        resultDone = []
        print(base)
        print(symbol)
        print(date)
        #Looper gjennom dataen og finner matchene resultater med vat_number
        for transaction in cleanedlist:
            if transaction[2] == date and transaction[0] == base or transaction[2] == date and transaction[0] == symbol:
                print("Succes")
                print(transaction)
                results.append(transaction)
        print("OVER HERE",results)
        print("Base currency", results[0])
        print("symbol currency", results[1])
        baseCurrency = results[0]
        symbolCurrency = results[1]
        basespot =float(baseCurrency[1])
        symbolspot = float(symbolCurrency[1])
        print(symbolspot,basespot)
        calculated_fx = float(basespot)/float(symbolspot)
        fx_rate = 1/calculated_fx
        CurrencyExplanation ="1 "+ baseCurrency[0]+" = "+symbolCurrency[0]
        templist = [CurrencyExplanation, fx_rate, date]
        resultDone.append(templist)


        #Bruker JSONIFY funksjonen fra flask til å konverter listen til JSON format
        return jsonify(resultDone)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
        


