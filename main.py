from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import psycopg2
import os

app = Flask(__name__)
CORS(app)

os.environ['credential.user'] = 'ytnmrkvrezuqgp'
os.environ['credential.password'] = '9096a9207a80a9ced6a46c5a1f9c347781359cba08940c4761eb722d4a0b28d6'
os.environ['credential.host'] = 'ec2-54-228-162-209.eu-west-1.compute.amazonaws.com'
os.environ['credential.port'] = '5432'
os.environ['credential.database'] = 'deebqrjrgb2m5'

@app.route("/")
def hello_world():
    return "<p>Application coffeeAPI loaded succesfully</p>"


@app.route("/consumptions")
def consumptions():
    records = readDatabase('consumption')
    parsedRecords = convertConsumptionToJSON(records)
    return jsonify(parsedRecords)

@app.route("/coffees")
def coffees():
    records = readDatabase('coffee')
    return jsonify(records)

def convertConsumptionToJSON(consumptions):
    parsedList = []
    for i in consumptions:
        parsedList.append({
            'id': i[0],
            'date': i[1],
            'coffeeType': i[2],
            'score': i[3]
        })
    return parsedList


def readDatabase(type):
    try:
        connection = psycopg2.connect(user=os.getenv('credential.user'),
                                      password=os.getenv('credential.password'),
                                      host=os.getenv('credential.host'),
                                      port=os.getenv('credential.port'),
                                      database=os.getenv('credential.database'))
        cursor = connection.cursor()
        query = ''
        if type == 'consumption':
            query = "select * from consumption"
        elif type == 'coffee':
            query = "select * from coffee"

        cursor.execute(query)
        mobile_records = cursor.fetchall()
        return mobile_records


    except (Exception, psycopg2.Error) as error:
        return str(error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()