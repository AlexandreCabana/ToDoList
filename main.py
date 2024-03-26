from datetime import datetime

from fastapi import FastAPI, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.mount("/css", StaticFiles(directory="css"
                              ), name="css")

items = []


class ItemBase(BaseModel):
    name: str
    due_date: str
    is_completed: bool = False

class ItemBaseWithId(ItemBase):
    id: int


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("mainpage.html", {"request": request, "items":items})


@app.get("/additem/")
async def additemview(request: Request):
    return templates.TemplateResponse("AddItem.html", {"request": request})


@app.post("/additem/")
async def additem(taskname: str = Form(...), duedate: str = Form(...)) -> RedirectResponse:
    item_data = {"name": taskname, "due_date":duedate}
    if len(items) == 0:
        id = 1
    else:
        id = items[-1]["id"] + 1
    item = ItemBaseWithId(id=id, **item_data).model_dump()
    items.append(item)
    return RedirectResponse("http://127.0.0.1:8000", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/completeitem/")
async def completeitem(taskid: int = Form(...), value:bool = Form(False)) -> RedirectResponse:
    items[taskid-1]["is_completed"] = not items[int(taskid)-1]["is_completed"]
    return RedirectResponse("http://127.0.0.1:8000", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/changename/")
async def changename(taskid: int = Form(...), taskname: str = Form(...)) -> RedirectResponse:
    items[taskid-1]["name"] = taskname
    return RedirectResponse("http://127.0.0.1:8000", status_code=status.HTTP_303_SEE_OTHER)
