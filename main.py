from fastapi import FastAPI, Form, UploadFile, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import io
from utils import parse_allowed_ips, generate_bat_file

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(
    request: Request,
    file: UploadFile,
    gateway: str = Form("0.0.0.0"),
    extra_ips: str = Form("")
):
    content = await file.read()
    config_text = content.decode("utf-8")

    ips = parse_allowed_ips(config_text)

    if extra_ips.strip():
        extra_list = [i.strip() for i in extra_ips.split(",")]
        ips.extend(extra_list)

    bat_content = generate_bat_file(ips, gateway)
    buffer = io.BytesIO(bat_content.encode())

    return StreamingResponse(
        buffer,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=routes.bat"}
    )
