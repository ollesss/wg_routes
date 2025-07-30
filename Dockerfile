FROM python:3.10-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY . .

# Явно указываем переменные окружения
ENV PORT=8080
ENV UVICORN_WORKERS=2
EXPOSE 8080

# Команда запуска с явным указанием хоста
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers ${UVICORN_WORKERS}"]