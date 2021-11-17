from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Application coffeeAPI loaded succesfully</p>"


@app.route("/consumptions")
def consumptions():
    records = readDatabase()
    return jsonify(records)


def readDatabase():
    try:
        connection = psycopg2.connect(user=os.getenv('credential.user'),
                                      password=os.getenv('credential.password'),
                                      host=os.getenv('credential.host'),
                                      port=os.getenv('credential.port'),
                                      database=os.getenv('credential.database'))
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from consumption"

        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall()
        return mobile_records


    except (Exception, psycopg2.Error) as error:
        return str(error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()