FROM python:3.11.2-alpine3.17 as base
COPY requirements.txt .
RUN pip install -r requirements.txt
FROM base
COPY . /app
WORKDIR /app
EXPOSE 5000
ENTRYPOINT python3 /app/main.py

