from fastapi import FastAPI, UploadFile, Form, Response, Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Annotated
import sqlite3

# DB 연결
con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

app = FastAPI()

# IF NOT EXISTS : 없을 때만 테이블 생성
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                image BLOB,
                price INTEGER NOT NULL,
                description TEXT,
                place TEXT NOT NULL,
                insertAt INTEGER NOT NULL
            );
            """)

# IF NOT EXISTS : 없을 때만 테이블 생성
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                image BLOB,
                price INTEGER NOT NULL,
                description TEXT,
                place TEXT NOT NULL,
                insertAt INTEGER NOT NULL
            );
            """)

# 오늘의 정답
answer = 'WORLD'

@app.get('/answer')
def get_answer():
    return {"answer" : answer}

# static 경로에 있는 파일을 사용할 예정
app.mount("/", StaticFiles(directory="static", html=True), name="static")