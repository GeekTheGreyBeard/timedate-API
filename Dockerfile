FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY timedate_app.py ./

EXPOSE 8200

CMD ["uvicorn", "timedate_app:app", "--host", "0.0.0.0", "--port", "8200"] 