FROM python:3.10-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY . .

# Указываем переменные (обязательно!)
ENV PORT=8080
EXPOSE 8080

# Запускаем сервер (важно: через `sh -c` и с логами)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1 --log-level info"]