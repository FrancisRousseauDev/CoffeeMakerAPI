from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import psycopg2
import os

app = Flask(__name__)
CORS(app)

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

@app.route("/numberByType")
def getNumberByType():
    records = readDatabase('number-comparison')
    parsedRecords = convertNumberByTypeToJSON(records)
    return jsonify(parsedRecords)

def getCoffeeNameByID(id, coffees):
    for i in coffees:
        if i[1] == id:
            return i[0]


def convertConsumptionToJSON(consumptions):
    parsedList = []
    for i in consumptions:
        parsedList.append({
            'id': i[0],
            'date': i[1],
            'name': i[2],
            'value': i[3]
        })
    return parsedList

def convertNumberByTypeToJSON(numbers):
    parsedList = []
    for i in numbers:
        parsedList.append({
            'id': i[0],
            'name': i[1],
            'value': i[2]
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
        elif type == 'number-comparison':
            query = "select con.\"coffeeID\", cof.\"name\", count(*) from public.consumption con inner" \
                    " join public.coffee cof on (con.\"coffeeID\" = cof.\"coffeeID\")" \
                    " GROUP BY cof.\"name\", con.\"coffeeID\""

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