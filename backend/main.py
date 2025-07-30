from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import re
from pathlib import Path
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_routes(
    config: UploadFile = File(None),
    gateway: str = Form("0.0.0.0"),
    extra_ips: str = Form("")
):
    allowed_ips = []
    
    if config:
        content = await config.read()
        matches = re.findall(r'AllowedIPs\s*=\s*(.+?)(?=\n|$)', content.decode(), re.IGNORECASE)
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
    
    return {"bat_content": "\n".join(bat_lines)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))