from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses  import HTMLResponse

app=FastAPI()
template=Jinja2Templates(directory=r"E:\Youtube learning assitance\AI-Youtube-assistent\frontend\templates")
@app.get("/")
def home(request:Request):
    return template.TemplateResponse(request=request,name="base.html")
