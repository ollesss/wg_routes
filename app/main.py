from fastapi import FastAPI, Request, Form, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import re
from pathlib import Path
import os

app = FastAPI()

# Настройка шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Настройка шаблонов
templates = Jinja2Templates(directory="templates")

# Функция генерации BAT-файла
def generate_bat(config_text: str, gateway: str, extra_ips: str = ""):
    allowed_ips = []
    
    # Парсим IP из конфига WireGuard
    if config_text:
        matches = re.findall(r'AllowedIPs\s*=\s*(.+?)(?=\n|$)', config_text, re.IGNORECASE)
        for match in matches:
            allowed_ips.extend([ip.strip() for ip in match.split(',') if ip.strip()])
    
    # Добавляем дополнительные IP
    if extra_ips:
        allowed_ips.extend([ip.strip() for ip in extra_ips.split(',') if ip.strip()])
    
    # Генерируем команды route
    bat_lines = []
    for cidr in allowed_ips:
        if '/' in cidr:
            ip, prefix = cidr.split('/')
            prefix = int(prefix)
            mask = (0xffffffff << (32 - prefix)) & 0xffffffff
            netmask = f"{(mask >> 24) & 0xff}.{(mask >> 16) & 0xff}.{(mask >> 8) & 0xff}.{mask & 0xff}"
            bat_lines.append(f"route ADD {ip} MASK {netmask} {gateway}")
    
    return "\n".join(bat_lines)

# Главная страница
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Обработка формы
@app.post("/generate")
async def generate(
    request: Request,
    config: UploadFile = File(None),
    gateway: str = Form("0.0.0.0"),
    extra_ips: str = Form("")
):
    config_text = (await config.read()).decode() if config else ""
    bat_content = generate_bat(config_text, gateway, extra_ips)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "bat_content": bat_content,
            "gateway": gateway,
            "extra_ips": extra_ips
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        workers=int(os.getenv("UVICORN_WORKERS", 1)),
        log_level="info",
        reload=False
    )