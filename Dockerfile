FROM python:3.11.11-slim-bookworm
RUN apt-get update
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./source .
CMD ["sh", "-c", "python createdb.py && python creategamedb.py && python trainmodel.py && python telegrambot.py"]