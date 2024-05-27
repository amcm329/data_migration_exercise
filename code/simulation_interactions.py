"""
   This snippet of code acts a simulation for using the endpoints created through the Flask server.
   
"""

import requests 

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
"""
def insert_table(filename, csv_path = "/home/sources/", number_of_rows = 1000): 
    pass 



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
