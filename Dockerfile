FROM python:3.6.3-slim-stretch

RUN mkdir /app /deploy

WORKDIR /app

COPY /deploy/requirements.txt /deploy/requirements.txt

RUN pip install --no-cache-dir -r /deploy/requirements.txt

COPY "$PWD/joplin" /app/joplin

EXPOSE 80

CMD ["./joplin/manage.py", "runserver", "0.0.0.0:80"]
