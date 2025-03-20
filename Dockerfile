FROM python:3.9-slim

WORKDIR /app

# Installer Redis client
RUN pip install redis

COPY task.py /app/

CMD ["python", "task.py"]
