import mysql.connector
from flask import *
from flask_cors import cross_origin
from qiskit import *
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'azizamro'
app.config['MYSQL_PASSWORD'] = 'Darien84'
app.config['MYSQL_DB'] = 'awnq'

mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

cursor = mysql.cursor()


@cross_origin()
@app.route("/locations")
def get_locations():
    cursor.execute(
        "SELECT * FROM LOCATIONS NATURAL JOIN LOCATION_DETAILS NATURAL JOIN STREETS ")
    records = cursor.fetchall()
    locations = []
    for record in records:
        location = {
            "id": record[0],
            "category": record[1],
            "location_details": {
                "id": record[2],
                "longitude": record[3],
                "latitude": record[4],
                "street": {
                    "id": record[5],
                    "name": record[6]
                }
            }
        }
        locations.append(location)
    return jsonify(locations)


@app.route("/streets")
@cross_origin()
def get_streets():
    cursor.execute("SELECT * FROM STREETS")
    records = cursor.fetchall()
    streets = []
    for record in records:
        street = {
            "id": record[0],
            "name": record[1]
        }
        streets.append(street)
    return jsonify(streets)


@cross_origin
@app.route("/location_details")
def get_details():
    cursor.execute(
        "SELECT * FROM LOCATIONS NATURAL JOIN LOCATION_DETAILS NATURAL JOIN STREETS ")
    return jsonify(cursor.fetchall())


@cross_origin
@app.route("/requests")
def get_requests():
    cursor.execute("INSERT INTO requests(no_of_people) values(3)")
    mysql.commit()
    return "success"


@app.route("/create-vehicle", methods=['POST'])
def create_vehicle():
    cursor.execute(
        "INSERT INTO VEHICLES(plate_no,max_capacity,vehicle_type) values(%s,%s,%s)",
        (request.form['plate_no'], request.form['max_capacity'], request.form['vehicle_type']))
    mysql.commit()
    return "success"


if __name__ == "__main__":
    app.run(debug=True)
