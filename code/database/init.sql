-- Creating and using the database. 
CREATE DATABASE globant;
USE globant;


/*
id (INTEGER) - Id of the department
department (STRING) - Name of the departmen
*/
CREATE TABLE departments (
  id INTEGER,
  department VARCHAR(50)
);


/*
id (INTEGER) - Id of the job
job (STRING) - Name of the job
*/
CREATE TABLE jobs (
 id INTEGER,
 job VARCHAR(50)
);


/*
id (INTEGER)  - Id of the employee
name (STRING) -  Name and surname of the employee
datetime (STRING) -  Hire datetime in ISO format
department_id (INTEGER) - Id of the department which the employee was hired for job_id INTEGER Id of the job which the employee was hired for
*/
CREATE TABLE hired_employees (
  id INTEGER,
  name VARCHAR(80),
  datetime VARCHAR(50),
  department_id INTEGER
);

