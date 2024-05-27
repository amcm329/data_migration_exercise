-- Creating and using the database. 
CREATE DATABASE IF NOT EXISTS globant;
USE globant;
      
/*
id (INTEGER)  - Id of the employee
name (STRING) -  Name and surname of the employee
datetime (STRING) -  Hire datetime in ISO format
department_id (INTEGER) - Id of the department which the employee was hired for job_id INTEGER Id of the job which the employee was hired for
*/	  
CREATE TABLE IF NOT EXISTS hired_employees (
  Id INTEGER,
  Name VARCHAR(80),
  My_Datetime VARCHAR(50),
  Department_Id INTEGER,
  Job_Id INTEGER
);

/*
INSERT INTO hired_employees
  (Id, Name, My_Datetime, Department_Id)
VALUES
  (9998, 'Aaron','today',3,9),
  (9999, 'Martin','today',4,10);
*/
  
/*
id (INTEGER) - Id of the department
department (STRING) - Name of the departmen
*/
CREATE TABLE IF NOT EXISTS departments (
  Id INTEGER,
  Department VARCHAR(50)
);

/*
INSERT INTO departments
  (Id, Department)
VALUES
  (9998, 'Health'),
  (9999, 'Finance');
*/
  
/*
id (INTEGER) - Id of the job
job (STRING) - Name of the job
*/
CREATE TABLE IF NOT EXISTS jobs (
 Id INTEGER,
 Job VARCHAR(50)
);

/*
INSERT INTO jobs
  (Id, Job)
VALUES
  (9998, 'Programmer'),
  (9999, 'Accountant');
*/
