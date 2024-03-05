from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.mount("/css", StaticFiles(directory="css"), name="css")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/testtemplatename/{name}")
async def testtemplatename(request: Request, name: str):
    return templates.TemplateResponse("testtemplatename.html", {"request":request, "name":name})

dogs = [{"name":"Bob", "age":10},{"name":"Alice", "age":30},{"name":"David", "age":2}]
@app.get("/testdisplaytable")
async def testdisplaytable(request: Request):
    return templates.TemplateResponse("testdisplaytable.html", {"request":request, "dogs":dogs})