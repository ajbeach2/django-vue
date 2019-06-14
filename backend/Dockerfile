FROM python:3.7.2
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
EXPOSE 8000
ADD . /app
ENTRYPOINT ["/app/bin/entrypoint.sh"]
CMD python manage.py runserver 0.0.0.0:80