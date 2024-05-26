FROM python:3.9

EXPOSE 5000

# ***** Creating both backups (avro) and sources (csv) folders. *****

RUN mkdir /home/backups

RUN mkdir /home/sources

# **** Adding the three csv files to the final destination in the container. *****s

#Left is your host (the path where the docker is) and right is the container's path.
# https://stackoverflow.com/questions/27068596/how-to-include-files-outside-of-dockers-build-context

ADD sources/departments.csv /home/sources/departments.csv

ADD sources/hired_employees.csv /home/sources/hired_employees.csv

ADD sources/jobs.csv /home/sources/jobs.csv

# ***** Instruction related to the installation and configuration of both Python libraries and Flask. *****

WORKDIR /app

#Left is your host (the path where the docker is) and right is the container's path.

COPY app/requirements.txt /app

RUN apt -qq -y update && apt -qq -y upgrade
	
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY app/app.py /app

CMD python app.py