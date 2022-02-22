from fastapi import FastAPI, Body, Form, File, UploadFile, Header, HTTPException, Request, Query, Depends
from fastapi.responses import FileResponse
from typing import Optional, List
from time import ctime
from classes.classes import Applications, Subscription, Response
import os

app = FastAPI()


@app.get('/fullname/')
async def fio(second_name: str, first_name: str, middle_name: str):
    response = {
                'second name': second_name,
                'first name': first_name,
                'middle name': middle_name
                }
    return response


@app.get('/fullname2/')
async def fio(second_name: str, first_name: str, middle_name: str, nick: Optional[str] = None):
    response = {
                'second name': second_name,
                'first name': first_name,
                'middle name': middle_name
                }
    if nick:
        response.update({'nickname': nick})
    return response


@app.get('/namecut/')
async def fio(name: str, nick: Optional[str] = None, current_time=ctime()):
    response = {
                'name': name,
                'time': current_time
                }
    if nick:
        response.update({'nickname': nick})
    return response


@app.post('/json/')
async def json(applications: List[Applications], subs: Subscription, token: str = Body(...)):
    return {'applications': applications, 'subscription': subs, 'token': token}


@app.post('/form/')
async def form(second_name: str = Form(...), first_name: str = Form(...), middle_name: str = Form(...)):
    response = {
        'second name': second_name,
        'first name': first_name,
        'middle name': middle_name
    }
    return response


@app.post('/filesize/')
async def file_size(file: bytes = File(...)):
    return{'file_size': len(file)}


@app.post('/filedir/')
def file_dir(file: UploadFile = File(...)):
    try:
        with open('tmp.jpg', 'wb') as tf:
            tf.write(file.file.read())
    except Exception as ex:
        return str(ex)

    return file.filename


@app.get('/read_file/{file_name}')
def read_file(file_name: str):
    if not os.path.isfile(file_name):
        raise HTTPException(status_code=404, detail='Файл не найден')
    return FileResponse(file_name)


@app.post('/headers/')
async def headers(x_api_key: str = Header(...), referer: Optional[str] = Header(None)):
    body = {'key': x_api_key}
    if referer:
        body.update({'info': referer})
    return body


@app.post('/responce/', response_model=Response)
async def create_responce(resp: Response):
    return resp


@app.post("/request")
async def requestdata(rqst: Request):

    json_body = await rqst.json()
    return {"query": rqst.query_params, "headers": rqst.headers, "form": rqst.form, 'js': json_body}


check = {'x': 'hello', 'y': 'world'}


@app.get('/checker/{check_id}')
async def errors(check_id: str):
    if not check_id in check:
        raise HTTPException(status_code=404, detail='Данные не валидны')
    return {'Result': check[check_id]}


async def common_parameters(req: Optional[str] = Query(None)):
    req_allowed = ('chel', 'chel2')
    if not req in req_allowed:
        raise HTTPException(status_code=400, detail='Некорректный параметр')
    return {'referer': req}


async def common_parameters2(ref: str):
    return {'referer': ref}


@app.get("/dep")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
