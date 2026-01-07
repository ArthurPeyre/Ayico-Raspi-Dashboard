FROM python:3.11-slim

WORKDIR /app
RUN pip install flask docker

COPY app.py .

CMD ["python", "app.py"]
