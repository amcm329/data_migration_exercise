# <center> Data Migration Exercise </center> 
### Full Name: Aarón Martin Castillo Medina 
### Email: aaroncastillo329@gmail.com

<br>

The following project consists in the development of a system that creates a API REST and, by using its corresponding endpoints,
it inserts, restores and creates backups to a MySQL database.

As you can see, the SQL database used in this case was MySQL (5.7) and the tool used for API REST is Flask () 

The project's structure is the following: 

```
.
|-- app
| ´-- app.py 
| ´-- requirements.txt 
|-- db 
| `-- init.sql
|-- sources
| `-- hired_employees.csv
| `-- departments.csv
| `-- jobs.csv
|-- Dockerfile
|-- docker-compose.yml
|-- simulation_interactions.py

```

<br>

I briefly explain each one of these elements: 

* **app.py** - the file that contains the Flask server. 
* **requirements.txt** - Python libraries that are required for the project. 
* **init.sql** - script that initializes the creation of tables in the database. 
* **hired_employees.csv, departments.csv, jobs.csv** - files required for the insertions. 
* **Dockerfile** - file requested to initialize the server.
* **docker-compose.yml** - file used to launch two services independently (Flask and MySQL).
* **simulation_interactions.py** - file created to emulate the actions from the user perspective (requests).

<br>

In order to execute the code by using docker, you should utilize the following command: 
**docker-compose up -d --build**

<br>

Regarding the considerations mentioned for the project:

## STORAGE
* In the container, I included the source files in the container so the experience can be more real from the user side. By executing the code simulation_interactions.py, the user will be able to carry out the mentioned activities (insert, restore, backup).
* During the creation of the container, I considered the directories /home/backups and /home/sources which correspond to their respective activities.

## LOGS
* I used Python's library logger to carry out this exercise, especially for the insertions section. 

## DOCKERFILE 
* Besides it, I created a file docker-compose.yml so I could launch these two services (MySQL and Flask).

## SECURITY
* I am keen on security by obscurity, which means that each one of the functionalities does exactly what it's needed, even the script simulation_interactions.py contains this essence as it represents only the necessary actions that a user or a client-side script would carry out, for instance, I prepare some data to be json-friendly (see insert_table); initially, that section doesn't correspond to the server since it only works on the assumption that the data comes in a reliable format.
It's the same example as in the insertions, I delegated this task to the user side by performing batch processing, and if it wasn't what the evaluator wanted, then I'd suggest moving to a ELT approach, where we can handle bulk_data without using enpoints since it wouldn't be scalable.
* I also added simple yet powerful checks in the code so we can make sure that the inputs have been sanitized. 
   
## NEXT STEPS 

There are many things to consider to harden this project, I mention the following: 
* Using https certificate for better security.
* Put primary and foreign key restrictions in the tables.
* Sanitize inputs in order to avoid SQL injection attacks.
* (For Flask) Use the WSGI server.
* For more security, specially in the insertion sections, it would be desirable to avoid using direct schemas, my point is that an automated engine like SQLAlchemy can skip this step and therefore, avoiding showing information to malicious users.
* Same as the previous one but using a vault server to store crucial information (paths, credentials), moreover, I tried to use a python version (hvac) but unfortunately, I ran out of time.
<br>


