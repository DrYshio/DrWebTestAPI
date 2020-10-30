from fastapi import FastAPI, File, UploadFile, HTTPException, Response
import hashlib
import os
from starlette.responses import FileResponse
import uvicorn
import logging
from config import *


app = FastAPI()


def delete_directory_if_empty(file_hash):
    if len(os.listdir(os.path.join('store', file_hash[:2]))) == 0:
        os.rmdir(os.path.join('store', file_hash[:2]))


@app.post('/files')
async def upload(file: UploadFile = File(...)) -> Response:
    file_hash = hashlib.sha224(file.filename.encode()).hexdigest()
    file_type = file.filename.split(sep='.')[1]

    if not os.path.isdir(os.path.join('store', file_hash[:2])):
        os.makedirs(os.path.join(os.getcwd(), 'store', file_hash[:2]))

    with open(os.path.join('store', file_hash[:2], f'{file_hash}.{file_type}'), "wb") as f:
        for chunk in iter(lambda: file.file.read(10000), b''):
            f.write(chunk)

    return Response(f'{file_hash}.{file_type}')


@app.delete('/files')
async def delete_file(data: str) -> Response or HTTPException:
    if os.path.isfile(os.path.join('store', data[:2], data)):
        os.remove(os.path.join('store', data[:2], data))
        delete_directory_if_empty(data.split(sep=".")[0])
        return Response('File deleted successfully')
    else:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )


@app.get('/files')
async def download(data: str) -> FileResponse or HTTPException:
    if os.path.isfile(os.path.join('store', data[:2], data)):
        return FileResponse(
            path=os.path.join('store', data[:2], data),
            filename=f'content.{data.split(sep=".")[1]}'
        )
    else:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )


if __name__ == "__main__":
    os.chdir(PATH_TO_WORKING_DIRECTORY)
    logger = logging.getLogger('DrWeb API')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('app.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.debug('The server is running')
    uvicorn.run(app, port=PORT, log_level="info")
    logger.debug('the server is down')
