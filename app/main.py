import mysql.connector as mariadb
from flask import Flask
app = Flask(__name__)
app.config.from_envvar('CFG_FILE')

@app.route("/")
def hello():
    return 'Hello Harvester'

@app.route("/status/insert/<plant_id>/<wat>/<hum>/<hea>", methods=["GET"])
def status_put(plant_id, wat, hum, hea):
    db = db_connection()
    add_status = ("INSERT INTO status (plant_id, water, humidity, heat) VALUES ({}, {}, {}, {})".format(plant_id, wat, hum, hea))
    db.execute(add_status)
    return True

def db_connection():
    mariadb_connection = mariadb.connect(user=app.config['DB_USER'], password=app.config['DB_PASSWORD'], database=app.config['DB'])
    cursor = mariadb_connection.cursor()
    return cursor

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
