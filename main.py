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


@app.route("/date-chart")
def getDateChart():
    records = readDatabase('line-chart')
    parsedRecords = convertDateChart(records, getAllCoffeeNames())
    return jsonify(parsedRecords)


def getCoffeeNameByID(id, coffees):
    for i in coffees:
        if i[1] == id:
            return i[0]


def getAllCoffeeNames():
    allCoffees = []
    coffees = readDatabase('coffee')
    for i in coffees:
        allCoffees.append(i[0])
    return allCoffees


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


def convertDateChart(datePoints, allCoffeeTypes):
    distinctDates = []
    allDatePoints = []
    parsedChart = []
    for i in datePoints:
        if i[2] not in distinctDates:
            distinctDates.append(i[2])
        allDatePoints.append({
            'name': i[0],
            'count': i[1],
            'date': i[2]
        })
    for coffee in allCoffeeTypes:
        series = []
        for i in distinctDates:
            value = find(allDatePoints, coffee, i) or 0
            series.append({
                'name': i,
                'value': value
            })
        parsedChart.append({
            'name': coffee,
            'series': series
        })

    return parsedChart


def find(arr, coffeetype, date):
    for x in arr:
        if x["name"] == coffeetype and str(x["date"]) == str(date):
            return x['count']


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
        elif type == 'line-chart':
            query = "select cof.\"name\", count(con.\"coffeeID\"), con.\"time\"::date from public.consumption con inner" \
                    " join public.coffee cof on (con.\"coffeeID\" = cof.\"coffeeID\")" \
                    " GROUP BY con.\"time\"::date, cof.\"name\", con.\"coffeeID\""

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
