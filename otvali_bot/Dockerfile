FROM python:3.11.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /bot
WORKDIR /bot

RUN pip install -r requirements

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
