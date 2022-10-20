FROM python:3.9.0

RUN mkdir /app/
WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT python3 -u -m main
