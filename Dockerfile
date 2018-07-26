FROM tiangolo/uwsgi-nginx-flask:python3.6
RUN pip install mysql-connector-python
COPY ./app /app
COPY ./config /app/config
