import uvicorn
import logging

import yaml
import os

from typing import Union
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/")
def read_root():
    logging.info("Root 엔드포인트에 요청이 들어왔습니다.")
    return {"path": "root"}

@app.get("/hello")
def read_hello():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

LOG_FILE_PATH = "./app.log"
# 최근 30줄 로그 반환하는 API
@app.get("/logs", response_class=PlainTextResponse)
async def get_logs():
    return get_last_n_lines(LOG_FILE_PATH, 30)

# n 파라미터의 따라 로그라인을 반환하는 함수
def get_last_n_lines(file_path, n):
    """
    주어진 파일에서 마지막 N줄을 반환하는 함수
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return ''.join(lines[-n:])
    except Exception as e:
        return f"오류 발생: {e}"

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    log_config_path = os.path.join(BASE_DIR, "log_config.yaml")
    
    # YAML 로그 설정 파일을 로드
    with open(log_config_path, 'r') as f:
        log_config = yaml.safe_load(f.read())
        logging.config.dictConfig(log_config)

    # uvicorn 실행 
    uvicorn.run("main:app", host='0.0.0.0', port=8000, log_level="info", log_config=log_config)