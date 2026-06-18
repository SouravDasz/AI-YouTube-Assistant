from fastapi import FastAPI,Request
from fastapi.responses  import HTMLResponse
from app.templates import templates
from app.api.workspace import router as workspace_router
app=FastAPI()
router_list=[workspace_router]
for router in router_list:
    app.include_router(router)
    
@app.get("/")
def home(request:Request):
    return templates.TemplateResponse(request=request,name="home.html")
