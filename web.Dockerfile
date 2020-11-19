FROM python:3.6 

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /app
COPY ./web_reqs.txt /app/reqs.txt
RUN pip install -r /app/reqs.txt
WORKDIR /app
COPY . /app

CMD ["python", "chat.py"]
