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
def restore_table(table, timestamp = None): 
    
    pass
    


def insert_table(filename, csv_path = "/home/sources/", number_of_rows = 1000): 
    pass 



"""
   This is the section related to the tests. 
"""

# **** BACKUP *****
#print(backup_table("hired_employees"))
#print(backup_table("jobs"))
#print(backup_table("departments"))
#print(backup("other")) 

print(get_backup_names())

# **** RESTORE *****
