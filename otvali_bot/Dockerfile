FROM python:3.11.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /bot
WORKDIR /bot

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
