from fastapi import APIRouter,Request,File
from app.templates import templates

router=APIRouter(prefix="/home")

@router.get("/workspace")
def workspace(request:Request):
    return templates.TemplateResponse(request=request,name="workspace.html")

@router.post("/workspace")
def workspace(youtube_url:str=File(...)):
    return {"youtube_url":youtube_url}