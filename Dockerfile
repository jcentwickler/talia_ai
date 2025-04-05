FROM python:3.11.11-slim-bookworm
RUN apt-get update
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./TaliaAI/main/createdb.py .c
CMD ["python", "createdb.py"]
CMD ["python", "train_model.py"]
CMD ["python", "telegrambot.py"]
#CMD ["tail", "-f", "/dev/null"]