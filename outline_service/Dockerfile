FROM python:3.11.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /outline_service
WORKDIR /outline_service

RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
