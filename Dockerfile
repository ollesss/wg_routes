FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.10-slim
WORKDIR /app

# Копируем зависимости из builder
COPY --from=builder /root/.local /root/.local
COPY . .

# Убедимся, что скрипты в PATH
ENV PATH=/root/.local/bin:$PATH

# Явно указываем переменные для Uvicorn
ENV PORT=8080
EXPOSE 8080

# Команда запуска с таймаутом
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --no-access-log --timeout-keep-alive 30"]