from fastapi import FastAPI, Request, Form, status, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/Image", StaticFiles(directory="Image"), name="Image")

items = []


class ItemCreate(BaseModel):
    name: str
    duedate: str
    is_completed: bool = False
    @classmethod
    def as_form(cls, name: str = Form(...), duedate: str = Form(...)):
        return cls(name=name, duedate=duedate)


class ItemWithId(ItemCreate):
    id: int
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("mainpage.html", {"request": request, "items": items})


@app.get("/additem/")
async def additemview(request: Request):
    return templates.TemplateResponse("AddItem.html", {"request": request})


@app.post("/additem/")
async def additem(request: Request, item: ItemCreate = Depends(ItemCreate.as_form)) -> RedirectResponse:
    if len(items) == 0:
        id = 1
    else:
        id = items[-1].id + 1
    items.append(ItemWithId(id=id, **item.dict()))
    return RedirectResponse("http://127.0.0.1:8000", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/completeitem/")
async def completeitem(taskid: int = Form(...), value: bool = Form(False)) -> RedirectResponse:
    items[taskid - 1].is_completed = not items[int(taskid) - 1].is_completed
    return RedirectResponse("http://127.0.0.1:8000", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/changename/")
async def changename(taskid: int = Form(...), taskname: str = Form(...)) -> RedirectResponse:
    items[taskid - 1].name = taskname
    return RedirectResponse("http://127.0.0.1:8000", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/changedate/")
async def changedate(taskid: int = Form(...), taskdate: str = Form(...)) -> RedirectResponse:
    items[taskid - 1].duedate = taskdate
    return RedirectResponse("http://127.0.0.1:8000", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/deleted/")
async def deleteditem(taskid: int = Form(...)):
    del items[taskid - 1]
    return RedirectResponse("http://127.0.0.1:8000", status_code=status.HTTP_303_SEE_OTHER)
