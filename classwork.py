from flask import Flask, request,render_template
import csv
import os
from datetime import datetime



headers = ["time", "temperature", "humidity"]
def checkDB(dbName):
    if not os.path.exists(dbName):
        print("creating new db")         
        with open(dbName,"w") as file:
            writer = csv.DictWriter(file,fieldnames=headers)
            writer.writeheader()  

    else:
        print("db exists") 
# A.if we have data inside our csv file
def last():
    with open(DBNAME,newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        if data:  
            return(data[-1]) 
        else:
            return{"temperature":0,"humidity":0}
        
# B.if we dont have data in our csv
def hh():
    holder = []
    with open(DBNAME,newline="")as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            holder.append(row)
        if len(holder)>0:
            return (reader[-1])
        else:
            return{"temperature":0,"humidity":0}          
                

def logData(temp, hum):
    try:
        curr_time = datetime.now().strftime("%H-%M-%S")  
        with open(DBNAME,"a",newline="") as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writerow({"time":curr_time,"temperature":temp,"humidity":hum }) 
        return ("saved")   
    except Exception as e:
        return(e)    

DBNAME = "Climate_log.csv"
checkDB(DBNAME)       

app = Flask(__name__)

@app.route("/saveData")
def saveData():
    temperature = request.args.get("curr_temp")
    humidity = request.args.get("curr_hum")
    logData(temperature,humidity)
    return(f"temperature = {temperature} and humidity = {humidity}")

@app.route("/")
def load_html():
    values = last()
    print(values)
    tem = values['temperature']
    hum = values['humidity']
    return render_template("indexcl.html",temp_corr =tem,hum_corr = hum)


if __name__ == "__main__":
    app.run(port=8248,host="0.0.0.0",debug=True)