import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

# Настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_routes(config_text: str, gateway: str, extra_ips: str):
    allowed_ips = []
    
    if config_text:
        matches = re.findall(r'AllowedIPs\s*=\s*(.+?)(?=\n|$)', config_text, re.IGNORECASE)
        for match in matches:
            allowed_ips.extend([ip.strip() for ip in match.split(',') if ip.strip()])
    
    if extra_ips:
        allowed_ips.extend([ip.strip() for ip in extra_ips.split(',') if ip.strip()])
    
    bat_lines = []
    for cidr in allowed_ips:
        if '/' in cidr:
            ip, prefix = cidr.split('/')
            prefix = int(prefix)
            mask = (0xffffffff << (32 - prefix)) & 0xffffffff
            netmask = f"{(mask >> 24) & 0xff}.{(mask >> 16) & 0xff}.{(mask >> 8) & 0xff}.{mask & 0xff}"
            bat_lines.append(f"route ADD {ip} MASK {netmask} {gateway}")
    
    return "\n".join(bat_lines)

@app.post("/api/generate")
async def create_routes(
    config: UploadFile = File(None),
    gateway: str = Form("0.0.0.0"),
    extra_ips: str = Form("")
):
    config_text = (await config.read()).decode() if config else ""
    return {
        "bat_content": generate_routes(config_text, gateway, extra_ips)
    }