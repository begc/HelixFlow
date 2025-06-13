FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 11110

CMD ["python", "main.py"]