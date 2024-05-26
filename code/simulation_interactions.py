"""
   This snippet of code acts a simulation for using the endpoints created through the Flask server.
   
"""

import requests 
import datetime

headers = {
            'Content-type':'application/json', 
            'Accept':'application/json'
          }
    
    
def backup_table(table = "hired_employees"): 

    additional_data = { 
                        'table_name': table, 
                      }
                      
    response = requests.post('http://127.0.0.1:5000/backup', json=additional_data, headers=headers)
    
    #response = requests.get('http://127.0.0.1:5000', params=additional_data)
    
    
    print(response.json())



def restore_table(): 
    pass
    



def get_current_date(): 
     #datetime.datetime.now().isoformat()
    pass

print(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))

#backup_table()
