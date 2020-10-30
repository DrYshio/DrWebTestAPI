from fastapi import FastAPI, File, UploadFile, HTTPException, Response
import hashlib
import os
from starlette.responses import FileResponse
import uvicorn
import logging
import config
from typing import Union


app = FastAPI()


def delete_directory_if_empty(file_hash):
    if len(os.listdir(os.path.join('store', file_hash[:2]))) == 0:
        os.rmdir(os.path.join('store', file_hash[:2]))


def create_path_to_file(file_hash):
    return os.path.join('store', file_hash[:2])


@app.post('/files')
async def upload(file: UploadFile = File(...)) -> Response:
    file_hash = hashlib.sha224(file.filename.encode()).hexdigest()
    file_type = file.filename.split(sep='.')[1]
    folder_path = create_path_to_file(file_hash)

    if not os.path.isdir(folder_path):
        os.makedirs(os.path.join(os.getcwd(), folder_path))

    with open(os.path.join(folder_path, f'{file_hash}.{file_type}'), "wb") as f:
        for chunk in iter(lambda: file.file.read(10000), b''):
            f.write(chunk)

    return Response(f'{file_hash}.{file_type}')


@app.delete('/files')
async def delete_file(data: str) -> Union[Response, HTTPException]:
    folder_path = create_path_to_file(data)

    if os.path.isfile(os.path.join(folder_path, data)):
        os.remove(os.path.join(folder_path, data))
        delete_directory_if_empty(data.split(sep=".")[0])
        return Response('File deleted successfully')
    else:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )


@app.get('/files')
async def download(data: str) -> Union[FileResponse, HTTPException]:
    folder_path = create_path_to_file(data)

    if os.path.isfile(os.path.join(folder_path, data)):
        return FileResponse(
            path=os.path.join(folder_path, data),
            filename=f'content.{data.split(sep=".")[-1]}'
        )
    else:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )


if __name__ == "__main__":
    os.chdir(config.PATH_TO_WORKING_DIRECTORY)
    logger = logging.getLogger('DrWeb API')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('app.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.debug('DrWeb HTTP API server is running')
    uvicorn.run(app, host=config.HOST, port=config.PORT, debug=config.DEBUG, log_level="info")
    logger.debug('DrWeb HTTP API server is down')
