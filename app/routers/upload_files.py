from fastapi import APIRouter, File, Depends, Form, UploadFile
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from ..static import html_generator
from .. import database, schemas, models, utils, oauth2



router = APIRouter(
    prefix='/file',
    tags=['Upload Files']
)


@router.get("/", response_class=HTMLResponse)
async def get_upload_page(current_user: int = Depends(oauth2.get_current_user)):

    return html_generator.gen_upload()


@router.post("/")
async def create_upload_file(current_user: int = Depends(oauth2.get_current_user),
patient_first_name: str = Form(...), patient_last_name: str = Form(...), file_name: str = Form(...),
files: list[UploadFile] = File(..., description="Upload muitiple files")):

    return {"filenames": [file_name for file in files],
    "patient_first_name": [patient_first_name for file in files]}
    #{ "filenames": [filename1, filename2, filename3, ...] }
    '''    
    print(patient_first_name + patient_last_name)
    print(files)
    file_content = await files.read()
    print(file_content)'''



'''
# Use StreamingResponse to iterate over file object 

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

some_file_path = "large-video-file.mp4"
app = FastAPI()


@app.get("/")
def main():
    def iterfile():  # 
        with open(some_file_path, mode="rb") as file_like:  # 
            yield from file_like  # 

    return StreamingResponse(iterfile(), media_type="video/mp4")

'''