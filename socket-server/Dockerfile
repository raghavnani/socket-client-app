FROM python:3.7-buster

RUN apt-get update -y && \
    apt-get upgrade -y

RUN python -m pip install --upgrade pip

COPY requirements.txt /src/
WORKDIR /src

RUN pip install -r requirements.txt

COPY raven_real_time.py /src/

COPY raven_pack_tickers.csv /src/

COPY run.py /src/

ENV FLASK_ENV=development

CMD python run.py
