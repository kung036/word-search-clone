from fastapi import FastAPI, UploadFile, Form, Response, Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from fastapi import FastAPI, HTTPException
from starlette import status

# env 가져오기
from dotenv import load_dotenv
import os

# DB 연결
con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

app = FastAPI()

# CORS 설정
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# 데이터베이스 설정
# IF NOT EXISTS : 없을 때만 테이블 생성
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                password TEXT NOT NULL
            );
            """)
cur = con.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL
            );
            """)
cur = con.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS texts (
                id INTEGER PRIMARY KEY,
                word TEXT NOT NULL,
                game_id INTEGER,
                FOREIGN KEY (game_id) REFERENCES users(id)
            );
            """)
cur = con.cursor()

# 토큰 발급
load_dotenv()
SECRET = os.getenv("TOKEN_KEY") # 인코딩키
print(SECRET)
manager = LoginManager(SECRET, '/login')

# 오늘의 정답
answer = 'WORLD'

@app.get('/answer')
def get_answer():
    return {"answer" : answer}

# 회원가입한 정보 찾기
@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'id="{data}"'
    if type(data) == dict:
        WHERE_STATEMENTS = f'''name="{data["name"]}"'''
    
    con.row_factory = sqlite3.Row # 컬럼명을 가져옴
    cur = con.cursor()

    user = cur.execute(f"""
                       SELECT * FROM users
                       WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

# 로그인
@app.post('/login')
def login (id:Annotated[str,Form()], 
           password:Annotated[str,Form()]):
    user = query_user(id)
    
    # 로그인 실패 시 에러 처리
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    
    # access token 발급
    access_token = manager.create_access_token(data={
        'sub' : {
            'id':user['id'],
            'name':user['name'],
        }
    })
    
    return {'access_token':access_token}

#회원가입
@app.post('/sign')
def post_sign(id:Annotated[str,Form()],
           name:Annotated[str,Form()],
           password:Annotated[str,Form()]):
    cur = con.cursor()
    cur.execute(f"""
                INSERT INTO users(id,name,password)
                VALUES('{id}','{name}','{password}');
                """)
    con.commit()
    return Response(status_code=status.HTTP_200_OK)
