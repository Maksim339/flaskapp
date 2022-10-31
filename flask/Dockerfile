FROM python:3.9.13

WORKDIR /app

ADD . /app

RUN chmod +x configure.sh && ./configure.sh
RUN python -m pip install amazon-textract-helper
RUN pip install -r requirements.txt
RUN apt install poppler-utils -y

CMD ["uwsgi", "app.ini"]
