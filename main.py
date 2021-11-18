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
    return jsonify(records)

@app.route("/coffees")
def coffees():
    records = readDatabase('coffee')
    return jsonify(records)


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