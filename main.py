from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.mount("/css", StaticFiles(directory="css"
                              ), name="css")

@app.get("/")
async def root():
    return RedirectResponse(url="/additem")

@app.get("/additem")
async def additem(request: Request):
    return templates.TemplateResponse("AddItem.html", {"request": request})