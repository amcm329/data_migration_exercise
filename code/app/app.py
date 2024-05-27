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

inserts = {
           "hired_employees": "INSERT INTO hired_employees(Id, Name, My_Datetime, Department_Id) VALUES (%s, %s, %s, %s)", 
           "departments": "INSERT INTO departments(Id, Department) VALUES (%s, %s)", 
           "jobs": "INSERT INTO jobs(Id, Job) VALUES (%s, %s)", 
          }
          

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
     if the count is 0 or -1, no backup is created.
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
          df = pd.read_sql(f'SELECT * FROM {table};', connection)    
          pdx.to_avro(f'{backup_directory}/{table}_{get_current_date()}.avro', df)
           
    else: 
      count = -1 
    
    cursor.close()
    connection.close()
    
    return count


"""
   Auxiliary function that allows the restoration of a table based on the avro file. 
   
 
   Parameters: 
    table_name - table name to be restored.
    file_name - the file corresponding to the backup
   
   Returns: 
     count - a number indicating the amount of rows that were transformed to an avro file
     
   Important: 
     if the count is -1, no backup is restored.
"""    
def restore_data(table_name,file_name):
    count = 0
    saved = "" 
    
    #This is the "happy path"; any other error during the process will cause the count to be -1
    try: 
    
        #We read the avro file stored in the folder 
        restore = pdx.read_avro(f'{backup_directory}{file_name}')
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
     
        #Need SQLAlchemy for this: 
        #https://stackoverflow.com/questions/72684970/execution-failed-on-sql-select-name-from-sqlite-master-where-type-table-and-n
        #restore.to_sql(name=table_name, con=connection, if_exists='replace')
        
        #We get the INSERT statement according to the table in question
        query_insert = inserts[table_name]
        
        #We prepare the information to be inserted simultaneously.
        pars = restore.values.tolist()
        pars = list(map(tuple, pars))
        
        #We insert the information. 
        #https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-executemany.html
        cursor.executemany(query_insert, pars)
        
        #Save changes. 
        #https://stackoverflow.com/questions/30842031/attributeerror-mysqlcursor-object-has-no-attribute-commit
        connection.commit()
    
        #We get the count of the recently restored table. 
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')    
        results = cursor.fetchall()[0]['COUNT(*)'] 

        count = results 
        cursor.close() 
        connection.close()
                
    except: 
        count = -1 
           
    return count


"""
   Index with my personal data
"""
@app.route('/')
def index():
    final_json = {
                  'Name': 'Aaron Martin Castillo Medina',
                  'Version': '1.0',
                  'Email': 'aaroncastillo329@gmail.com'
                  }
                  
    return jsonify(final_json)


"""
"""
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

   Important: 
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
               
   Parameters: 
     table_name - the table name to be backed up. 
     timestampe - the timestamp IN STRING FORMAT that uniquely identifies the backup.
                  If no timestamp is specified, then the latest backup will be used.    

   Returns: 
    A dictionary with the following structure:
      table - the BACKUP file name that was restored.
      status - HTTP status code 
      message - a more particular message depending on the situations during the process. 
      count - the number of rows that contains the BACKUP.       
      mimetype - the document type.

   Important: 
      This will be a FULL RESTORATION, so you should keep that in mind.
      If you don't know the timestamps available, you can use the function get_backup_names instead.            
"""   
@app.route('/restore', methods=['GET', 'POST'])
def restore():
    final_name = ""
    status = 200
    message = "OK" 
    
    result = request.get_json()
    current_table = result.get("table_name")
    current_timestamp = result.get("timestamp")
    
    #Checking if the table is not empty.  
    if current_table is not None and current_table.replace(" ","") != "" and current_table != "": 
       final_name = "" 
    
       #If there's no timestamp, we get the latest one.
       if current_timestamp is None: 
     
          all_files = [x for x in os.listdir(backup_directory) if current_table in x]
          
          if all_files != []: 
              #Sorting all the elements by their timestamp transformed to a date object. 
              #https://stackoverflow.com/questions/14295673/convert-string-into-datetime-time-object
              #https://stackoverflow.com/questions/37693373/how-to-sort-a-list-with-two-keys-but-one-in-reverse-order
              all_files.sort(key=lambda x: datetime.datetime.strptime( x.replace(current_table,"").replace(".avro","")[1:] ,"%Y_%m_%d_%H_%M_%S"), reverse = True)
              final_name = all_files[0]
          
       #If the timestamp is not NULL, we proceed with the regular nomenclature.   
       else: 
           final_name = f'{current_table}_{current_timestamp}'
           
       #Getting the number of rows that were restored in the file.
       count = restore_data(current_table,final_name)
    
       #If the count is -1, the table doesn't exist. 
       if count == -1: 
            status = 406
            message = "Backup doesn't exist."
        
    else: 
      status = 404
      message = "Backup not specified."
      
    #Returning the final json
    final_json = {
                  'table': final_name,     
                  'status': status,
                  'message': message, 
                  'count': count,
                  'mimetype': 'application/json'
                 }
                  
    return jsonify(final_json)   


""" 
   Main method.
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0')
