# etapa de build
FROM python:3.11-slim AS build
WORKDIR /usr/src/app

# 1) copie só o requirements para acelerar cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 2) copie todo o código da sua app
COPY app/ .

# --- fim da build stage ---

# etapa de runtime
FROM python:3.11-slim
WORKDIR /usr/src/app

# pegue tudo do estágio de build
COPY --from=build /usr/src/app .

EXPOSE 8000

# exemplo com Uvicorn/FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
