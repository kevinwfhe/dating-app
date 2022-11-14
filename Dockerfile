FROM python:3.10-alpine AS builder
WORKDIR /app 
COPY requirements.txt /app
RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN pip3 install -r requirements.txt
COPY . /app 
EXPOSE 8000
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
