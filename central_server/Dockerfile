FROM python:3.9-slim

WORKDIR /app

RUN pip install flask requests

RUN mkdir -p /app/logs

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
