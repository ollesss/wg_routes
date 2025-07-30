FROM python:3.10-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend ./backend
COPY frontend ./frontend

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]