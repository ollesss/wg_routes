# Шаг сборки фронтенда
FROM node:18 as frontend-builder
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --silent
COPY frontend/ .
RUN npm run build

# Основной образ
FROM python:3.10-slim
WORKDIR /app

# Копируем бекенд
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./backend

# Копируем собранный фронтенд
COPY --from=frontend-builder /app/dist /app/frontend/dist

# Копируем serve.py
COPY serve.py .

ENV PORT=8080
EXPOSE 8080

CMD ["python", "serve.py"]