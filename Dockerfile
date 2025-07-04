FROM python:3.13

RUN mkdir /app/
WORKDIR /app

COPY ./pyproject.toml ./
RUN pip install ./

COPY . .

EXPOSE 8001

ENTRYPOINT ["python3", "main.py"]
