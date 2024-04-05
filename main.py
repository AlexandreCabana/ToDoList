from fastapi import FastAPI, Request, Form, status, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session

templates = Jinja2Templates(directory="templates")
app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/Image", StaticFiles(directory="Image"), name="Image")




class ItemCreate(BaseModel):
    name: str
    duedate: str
    is_completed: bool = False

    @classmethod
    def as_form(cls, name: str = Form(...), duedate: str = Form(...)):
        return cls(name=name, duedate=duedate)


class ItemWithId(ItemCreate):
    id: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependacy = Depends(get_db)

@app.get("/")
async def root(request: Request, db = db_dependacy):
    items = [i for i in db.query(models.ToDo).all()]
    return templates.TemplateResponse("mainpage.html", {"request": request, "items": items})


@app.get("/additem/")
async def additemview(request: Request):
    return templates.TemplateResponse("AddItem.html", {"request": request})


@app.post("/additem/")
async def additem(request: Request, item: ItemCreate = Depends(ItemCreate.as_form),
                  db=db_dependacy) -> RedirectResponse:
    if len([i for i in db.query(models.ToDo).all()]) == 0:
        id = 1
    else:
        id = db.query(models.ToDo).order_by(models.ToDo.id.desc()).first().id + 1
    itemwithid = ItemWithId(id=id, **item.dict())
    dbitem = models.ToDo(**itemwithid.dict())
    db.add(dbitem)
    db.commit()
    return RedirectResponse("http://127.0.0.1:8000", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/completeitem/")
async def completeitem(taskid: int = Form(...), value: bool = Form(False), db = db_dependacy) -> RedirectResponse:
    db_task = db.query(models.ToDo).filter(models.ToDo.id == taskid).first()
    db_task.is_completed = not db_task.is_completed
    db.commit()
    return RedirectResponse("http://127.0.0.1:8000", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/changename/")
async def changename(taskid: int = Form(...), taskname: str = Form(...), db = db_dependacy) -> RedirectResponse:
    db_task = db.query(models.ToDo).filter(models.ToDo.id == taskid).first()
    db_task.name = taskname
    db.commit()
    return RedirectResponse("http://127.0.0.1:8000", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/changedate/")
async def changedate(taskid: int = Form(...), taskdate: str = Form(...), db = db_dependacy) -> RedirectResponse:
    db_task = db.query(models.ToDo).filter(models.ToDo.id == taskid).first()
    db_task.duedate = taskdate
    db.commit()
    return RedirectResponse("http://127.0.0.1:8000", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/deleted/")
async def deleteditem(taskid: int = Form(...), db = db_dependacy):
    db_task = db.query(models.ToDo).filter(models.ToDo.id == taskid).first()
    db.delete(db_task)
    db.commit()
    return RedirectResponse("http://127.0.0.1:8000", status_code=status.HTTP_303_SEE_OTHER)
''