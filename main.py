from fastapi import FastAPI, File, UploadFile
import hashlib
import shutil
import os
from starlette.responses import FileResponse
import uvicorn


app = FastAPI()


def delete_directory_if_empty(file_hash):
    if len(os.listdir(os.path.join('store', file_hash[:2]))) == 0:
        os.rmdir(os.path.join('store', file_hash[:2]))


@app.post('/files', response_description="File's sha224 hash")
async def upload(file: UploadFile = File(...)) -> dict:
    file_hash = hashlib.sha224(file.filename.encode()).hexdigest()

    if not os.path.isfile(os.path.join('store', file_hash[:2])):
        os.mkdir(os.path.join('store', file_hash[:2]))

    with open(os.path.join('store', file_hash[:2], file_hash), "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file hash": file_hash}


@app.delete('/files', response_description="Result of deleting")
async def delete_file(data: str) -> dict:
    if os.path.isfile(os.path.join('store', data[:2], data)):
        os.remove(os.path.join('store', data[:2], data))
        delete_directory_if_empty(data)
        return {'response': 'Successful deleted'}
    else:
        return {'response': 'File does not exist.'}


@app.get('/files', response_description='Requested file')
async def download(data: str) -> FileResponse or dict:
    if os.path.isfile(os.path.join('store', data[:2], data)):
        return FileResponse(
            os.path.join('store', data[:2], data),
            media_type='picture/jpeg',
            filename='content')
    else:
        return {'response': 'File does not exist.'}


if __name__ == "__main__":
    uvicorn.run(app, port=8000, log_level="info")
