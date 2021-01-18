FROM python:3.7

# RUN apt-get update
# RUN apt-get -y install gcc

WORKDIR /opt/app

COPY . /opt/app
RUN pip install -r requirements.txt

CMD ["python","run.py","-h", "0.0.0.0"]
