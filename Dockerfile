FROM python:3.12-slim
WORKDIR /health
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5004
CMD ["python", "health.py"]
