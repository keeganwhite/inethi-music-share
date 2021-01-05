FROM tiangolo/uwsgi-nginx-flask:python3.8
ENV LISTEN_PORT 5000
EXPOSE 5000
COPY ./app /app
