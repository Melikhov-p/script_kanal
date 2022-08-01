# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /script_kanal/

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade -r requirements.txt

COPY kanal-table-5eac2891ffdd.json kanal-table-5eac2891ffdd.json
ADD get_course.py /script_kanal/
ADD request_db.py /script_kanal/
ADD main.py /script_kanal/

CMD ["python3", "main.py"]