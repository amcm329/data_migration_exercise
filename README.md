# Data Migration Exercise
## Full Name: Aarón Martin Castillo Medina 
## Email: aaroncastillo329@gmail.com

The following project consists in the development of a system that creates a API REST and, by using its corresponding endpoints,
it inserts, restores and creates backups to a MySQL database.

As you can see, the SQL database used in this case was MySQL (5.7) and the tool 

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

We briefly explain each one of these elements: 

* app.py - the file that contains the Flask server. 
* requirements.txt - Python libraries that are required for the project. 
* init.sql - script that initializes the creation of tables in the database. 
* hired_employees.csv, departments.csv, jobs.csv - files required for the insertions. 
* Dockerfile - file requested to initialize the server.
* doccker-compose.yml - file used to launch two services independently (Flask and MySQL).
* simulation_interactions.py - file created to emulate the actions from the user perspective (requests).

Regarding the considerations mentioned for the project 
