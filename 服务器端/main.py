from fastapi import FastAPI, Form, File, UploadFile
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import json
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request":request
        }
    )

def ImageData():
    FileData = []
    FileJson = {}

    line = 0
    for paths, dirs, files in os.walk("static/Setu"):
        for file in files:
            FileData.append(f"/static/Setu/{file}")
            FileJson[line] = f"/static/Setu/{file}"
            line += 1

    return [FileData, FileJson]


_Image_ = ImageData()
@app.get("/setu/{NUM}")
async def Setu(request: Request, NUM):
    return templates.TemplateResponse(
        "setu.html",
        {
            "request":request,
            "setu":_Image_[0][int(NUM)]
        }
    )

@app.get("/SetuData")
async def SetuData(request: Request):
    return _Image_[-1]

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8990)