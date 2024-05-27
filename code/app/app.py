"""
   This is a script representing the interactions as endpoints by using a Flask server. 
   
   https://auth0.com/blog/developing-restful-apis-with-python-and-flask/
   https://www.tutorialspoint.com/how-to-show-all-the-tables-present-in-the-database-and-server-in-mysql-using-python
"""

import os
import datetime
import pandas as pd
import pandavro as pdx
import mysql.connector

#To create the directory for saving backups.
from pathlib import Path

#Note: request in Flask is no the same as requests. 
from flask import Flask, jsonify, request 


backup_directory = "/home/backups/"

config = {
          'user': 'root',
          'password': 'root',
          'host': 'database',
          'port': '3306',
          'database': 'globant'
         }
    
app = Flask(__name__)

"""
   This secondary function allows us to obtain a timestamp in a string format. 
   so the avro backups attach this "id".
 
   https://www.programiz.com/python-programming/datetime/strftime   
   
   returns: 
     date in string format with the characteristics: "YYYY_MM_DD_HH_MM_SS" 
"""
def get_current_date(): 
    return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    

"""
   Auxiliary function that allows the creation of a table in avro format based 
   on the whole table existing at a certain point
   
   https://stackoverflow.com/questions/12047193/how-to-convert-sql-query-result-to-pandas-data-structure
   
   Parameters: 
    table - table name to be backed up.
   
   Returns: 
     count - a number indicating the amount of rows that were transformed to an avro file
     
   Important: 
     if the count is 0 or -1, no backup is created. s
"""    
def backup_data(table):
    count = 0
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    
    #First check: finding out if the table exists in the database.
    cursor.execute("SHOW TABLES")    
    schemas = cursor.fetchall()
  
    flag = 0 
    
    #https://www.tutorialspoint.com/how-to-show-all-the-tables-present-in-the-database-and-server-in-mysql-using-python
    
    for element in schemas: 
        if element['Tables_in_globant'] == table: 
           flag = 1        
    
    #The table exists in the database.     
    if flag == 1: 
       cursor.execute(f'SELECT COUNT(*) FROM {table}')    
       results = cursor.fetchall()[0]['COUNT(*)']
       
       #Second check: finding if the table is not empty.
       if results > 0: 
          count = results 
          
          #Getting the information as a dataframe and then saving it as an avro file.
          df = pd.read_sql("SELECT * FROM {0};".format(table), connection)    
          pdx.to_avro(f'{backup_directory}/{table}_{get_current_date()}.avro', df)
           
    else: 
      count = -1 
    
    cursor.close()
    connection.close()
    
    return count


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
    table_name - the database to be backed up.

   Returns: 
    A dictionary with the following structure:
      table - the table name.
      status - HTTP status code 
      message - a more particular message depending on the situations during the process. 
      count - the number of rows that contains the avro file.       
      mimetype - the document type.

   Note: 
    The backup will have the following format: 
        table_name_yyyy_mm_dd_hh_mm_ss.avro   
"""
@app.route('/backup', methods=['GET', 'POST'])
def backup():
    count = 0    
    status = 200
    message = "OK" 
    
    result = request.get_json()
    current_table = result.get("table_name")
  
    #Checking if the table is not empty.  
    if current_table is not None and current_table.replace(" ","") != "" and current_table != "": 
     
       #Getting the number of rows that were transformed into an avro file.
       count = backup_data(current_table)

       #If the count is 0, the table is empty.
       if count == 0: 
          status = 406
          message = "Table is empty."
       
       #If the count is -1, the table doesn't exist. 
       elif count == -1: 
            status = 406
            message = "Table doesn't exist."
        
    else: 
      status = 404
      message = "Table not specified."
      
    #Returning the final json
    final_json = {
                  'table': current_table,
                  'status': status,
                  'message': message, 
                  'count': count,
                  'mimetype': 'application/json'
                 }
                  
    return jsonify(final_json)   
    

"""
   The following is a method to RESTORE a backup (in avro format) 
   It will be restored in the corresponding table.
   
   Parameters: 
    files - a list with all the available backups' names.
    mimetype - the document type.

   Important: 
     if the list is empty, it means that there are no available backups.   
"""   
@app.route('/backup_names', methods=['GET'])
def backup_names():
    #Listing all available paths in the backup directory.
    files = os.listdir(backup_directory)

    #Returning the final json
    final_json = {
                  'files': files,
                  'mimetype': 'application/json'
                 }
                 
    return jsonify(final_json) 


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
