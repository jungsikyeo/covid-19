FROM python:3.8-buster

WORKDIR /var/jenkins_home/workspace/Covid-19

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "gunicorn", "--bind", "0.0.0.0:8000" "main:server" ]