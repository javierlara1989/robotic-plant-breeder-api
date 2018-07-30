import logging
import mysql.connector as mariadb
from flask import Flask, render_template, request

app = Flask(__name__)
app.config.from_envvar('CFG_FILE')
app.config['APPLICATION_ROOT'] = '/app'

logging.basicConfig(filename=app.config['LOG_FILE'], level=logging.DEBUG)


@app.route('/handle_login', methods=['POST'])
def handle_login():
    if [app.config['USER'], app.config['PASSWORD']] == [request.form['username'], request.form['password']]:
        return render_template('dashboard.html', title = 'Plants Panel')
    else:
        return 'Login Fail.'

@app.route('/login')
def login():
    return render_template('login.html', title = 'Login')

@app.route('/plant/insert/<token>/<name>/<bank>', methods=['GET'])
def plant_put(token, plant_id, wat, hum, hea):
    if token != app.config['APP_TOKEN']:
        return 'Conmigo no perrite.'
    logging.info('Inserting plant {} from {}'.format(name, bank))
    try:
        add_status = ('INSERT INTO plants (name, bank) VALUES ({}, {})'.format(name, bank))
        logging.info('Inserting {} Query.'.format(add_status))
        result = db_execute(add_status)
    except Exception as e:
        logging.warning('Error on plant_put: ' + str(e))
        return 'ERROR'
    if not result:
        return 'ERROR'
    return '200'


@app.route('/status/insert/<token>/<plant_id>/<wat>/<hum>/<hea>', methods=['GET'])
def status_put(token, plant_id, wat, hum, hea):
    if token != app.config['APP_TOKEN']:
        return 'Conmigo no perrite.'

    logging.info('Inserting status for Plant {}'.format(plant_id))
    try:
        add_status = ('INSERT INTO status (plant_id, water, humidity, heat) VALUES ({}, {}, {}, {})'.format(plant_id, wat, hum, hea))
        logging.info('Inserting {} Query.'.format(add_status))
        result = db_execute(add_status)
    except Exception as e:
        logging.warning('Error on status_put: ' + str(e))
        return 'ERROR'
    if not result:
        return 'ERROR'
    return '200'

def db_execute(db_query):
    logging.info('Connecting with database')
    try:
        mariadb_connection = mariadb.connect(host=app.config['DB_HOST'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'], database=app.config['DB'])
        cursor = mariadb_connection.cursor()
        cursor.execute(db_query)
        mariadb_connection.commit()
        mariadb_connection.close()
        cursor.close()
        logging.info('Executed query.')
    except Exception as e:
        logging.warning('Error on db_execute: ' + str(e))
        return False
    return True

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
