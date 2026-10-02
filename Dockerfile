FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "pipeline.py", "--input", "data/retail_store_sales.csv", "--output", "results"]