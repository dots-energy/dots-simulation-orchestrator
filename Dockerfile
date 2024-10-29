FROM python:3.9.0

RUN mkdir /app/
WORKDIR /app

COPY ./requirements.in ./
RUN pip install pip-tools
RUN pip-compile requirements.in
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001

ENTRYPOINT ["python3", "main.py"]
