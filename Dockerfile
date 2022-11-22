FROM python:3.9.0

RUN mkdir /app/
WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001

ENTRYPOINT python3 -u -m main
