"""
   This snippet of code acts a simulation for using the endpoints created through the Flask server.
   
"""

import os
import math
import requests 
import numpy as np
import pandas as pd

#Creating the headers section for all the following requests. 
headers = {
            'Content-type':'application/json', 
            'Accept':'application/json'
          }

    
"""
   This is a function meant to test the creation of backups, according to the exercise statements. 
   
   Parameters:
     table_name - the table name to be backed up. 
   
   Returns: 
    A dictionary with the following structure:
      table - the table name.
      status - HTTP status code 
      message - a more particular message depending on the situations during the process. 
      count - the number of rows that contains the avro file.       
      mimetype - the document type.
"""    
def backup_table(table_name): 

    additional_data = { 
                        'table_name': table_name, 
                      }
                      
    response = requests.post('http://127.0.0.1:5000/backup', json=additional_data, headers=headers)
    return response.json()


"""
   This function retrieves all available backups.
   
   Returns: 
    A dictionary with the following structure:
      files - all files names.
      
   Important: 
     if the list is empty, it means that there are no available backups.
"""
def get_backup_names():                   
    response = requests.get('http://127.0.0.1:5000/backup_names',  headers=headers)
    return response.json()


"""
   This is a function meant to test the backup RESTORATION in .avro format, according
   to the exercise statements. 
   
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
def restore_table(table_name, timestamp = None): 
    
    additional_data = { 
                        'table_name': table_name, 
                      }
    
    #If there is a timestamp, then the corresponding key-value
    #is added.
    if timestamp is not None: 
       additional_data["timestamp"] = timestamp
    
    response = requests.post('http://127.0.0.1:5000/restore', json=additional_data, headers=headers)
    return response.json()

    

"""
   This is a function meant insert rows from a csv as chunks to a specified table. 
   
   Parameters:
     filename - the filename contanining the csvs. 
     csv_path -  the path that contains the csvs. 
     number_of_rows - the "chunk size" to be sent. 
     
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
def insert_table(filename, csv_path = "/home/sources/", number_of_rows = 1000): 
    list_of_responses = []
 
    complete_file = f'{csv_path}{filename}.csv'
    
    #Checking if the file exists.
    if os.path.exists(complete_file): 
    
       df = pd.read_csv(complete_file)
       
       #Preparing the data so it can be json-friendly 
       #https://stackoverflow.com/questions/38821132/bokeh-valueerror-out-of-range-float-values-are-not-json-compliant
       #https://stackoverflow.com/questions/17173524/pandas-dataframe-object-types-fillna-exception-over-different-datatypes
       for col in df:
           #get dtype for column
           dt = df[col].dtype 
           #check if it is a number
           if dt == int or dt == float:
              df[col] = df[col].fillna(0.0)
           else:
              df[col] = df[col].fillna("")
       
    
       how_many_elements = df.shape[0] 
       final_number_of_rows = number_of_rows
    
       #if the number of chunks is 0, then we avoid a division by zero.
       if number_of_rows == 0: 
          final_number_of_rows = 1 
    
       #Calculating the number of chunks.      
       number_of_chunks = int(math.ceil(how_many_elements/final_number_of_rows)) 
    
       #https://stackoverflow.com/questions/17315737/split-a-large-pandas-dataframe
       df_list = np.array_split(df, number_of_chunks)
    
    
       #Sending the information per chunks
       for current_df in df_list: 
           dataset = current_df.values.tolist()
           
           #print(dataset) 

           additional_data = { 
                              'table_name': filename, 
                              'dataset': dataset
                             }
                            
           response = requests.post('http://127.0.0.1:5000/insert', json=additional_data, headers=headers)
           return response.json()
    else: 
        print("Path doesn't exist")
   
    return list_of_responses 
    
      
"""
   This is the section related to the tests. 
"""

# **** BACKUP *****
#print(backup_table("hired_employees"))
#print(backup_table("jobs"))
#print(backup_table("departments"))
#print(backup_table("other")) 

#print(get_backup_names())

# **** RESTORE *****
#print(restore_table("hired_employees"))
#print(restore_table("jobs"))
#print(restore_table("departments"))
#print(restore_table("other")) 


# **** INSERT *****
#print(insert_table("hired_employees"))
#print(insert_table("jobs"))
#print(insert_table("departments"))
#print(insert_table("other")) 

# **** INSERT (MY LOCAL MODE ONLY)*****
#print(insert_table("hired_employees", csv_path = "sources/"))
#print(insert_table("jobs", csv_path = "sources/"))
#print(insert_table("departments", csv_path = "sources/"))
#print(insert_table("other", csv_path = "sources/")) 
