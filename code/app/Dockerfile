FROM python:3.9

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app

RUN apt -qq -y update && apt -qq -y upgrade
	
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY app.py /app

CMD python app.py
