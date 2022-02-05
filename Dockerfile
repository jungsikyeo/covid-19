FROM python:3.8-buster

WORKDIR /var/jenkins_home/workspace/Covid-19

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8050

CMD [ "python", "main.py" ]