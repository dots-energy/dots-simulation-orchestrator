FROM python:3.14

RUN mkdir /app/
WORKDIR /app

COPY . .
RUN pip install ./

EXPOSE 8001

ENTRYPOINT ["python3", "main.py"]
