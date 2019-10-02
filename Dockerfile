FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN rm /code/db.sqlite3 -f

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN chmod +x /code/runserver.sh
CMD ["./runserver.sh"]