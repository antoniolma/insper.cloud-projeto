FROM python:3.11-slim

WORKDIR /usr/src/app

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      libpq-dev \
      build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app/ .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
