FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.10-slim
WORKDIR /app

# Копируем зависимости
COPY --from=builder /root/.local /root/.local
COPY . .

# Путь к Python-библиотекам
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

# Параметры сервера
ENV PORT=8080
ENV UVICORN_WORKERS=2
EXPOSE 8080

# Команда запуска (важно!)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers ${UVICORN_WORKERS}"]