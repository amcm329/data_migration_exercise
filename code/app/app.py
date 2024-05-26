"""
   This is a script representing the interactions as endpoints by using a Flask server. 
"""

import datetime
import pandas as pd
import mysql.connector

#To create the directory for saving backups.
from pathlib import Path

#Note: request in Flask is no the same as requests. 
from flask import Flask, jsonify, request 


directory = "backups"
config = {
          'user': 'root',
          'password': 'root',
          'host': 'database',
          'port': '3306',
          'database': 'globant'
       }
    
app = Flask(__name__)


def get_current_date(): 
    return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    
    
def get_backup_data(table): 
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM {table}')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


def employee_data():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM hired_employees')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


@app.route('/')
def index():
    return jsonify({'Employee Data': employee_data()})


@app.route('/insert', methods=['GET', 'POST']   )
def insert():
    pass


"""
   The following is a method to CREATE a backup (in avro format) 
   It will be stored in the folder avro.
   
   Parameters: 
    table name - the database to be backed up. 

   Note: 
    The backup will have the following format: 
        table_name_yyyy_mm_dd_hh_mm_ss.avro 
     
"""
@app.route('/backup', methods=['GET', 'POST'])
def backup():

    status = 200

    #Create the directory
    path = Path("../" + directory)
    path.mkdir(parents=True, exist_ok=True)

    #os.mkdir("../avro")
    result = request.get_json()
    print(result)
    return jsonify(result) #'', 204
    
    #status=201, mimetype='application/json'    
    

"""
   The following is a method to RESTORE a backup (in avro format) 
   It will be restored in the corresponding table.
   
   Parameters: 
    table name - the database to be restored.
    datetime - the date in format  "yyyy_mm_dd_hh_mm_ss" to find the desired backup.
               if the date is null, then the latest date is used. 
"""   
@app.route('/restore', methods=['GET', 'POST'])
def restore():
    result = request.get_json()
    return '', 204


""" 
   Main method.
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0')
