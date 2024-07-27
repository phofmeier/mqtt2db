FROM python:3

WORKDIR /home/app
COPY . .
RUN pip install .

CMD [ "mqtt2db" ]
