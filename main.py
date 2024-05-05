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
from typing import List

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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                user_id TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            """)
cur = con.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                game_id INTEGER,
                FOREIGN KEY (game_id) REFERENCES games(id)
            );
            """)
cur = con.cursor()

# 토큰 발급
load_dotenv()
SECRET = os.getenv("TOKEN_KEY") # 인코딩키
manager = LoginManager(SECRET, '/login')

@app.get('/answer')
def get_answer():
    return {"answer" : answer}

# 게임 만들기
@app.post('/game')
async def post_game(title:Annotated[str,Form()], 
                description:Annotated[str,Form()], 
                words:Annotated[List[str],Form()],
                user=Depends(manager)): # 인증된 상태에만 허용
    # 게임 정보 삽입
    cur = con.cursor()
    cur.execute(f"""
                INSERT INTO games(title, description, user_id)
                VALUES('{title}', '{description}', '{user['id']}');
                """)
    con.commit()

    # 삽입된 게임의 id를 가져오기
    cur = con.cursor()
    cur.execute("SELECT last_insert_rowid();")
    con.commit()
    game_id = cur.fetchone()[0]

    # 단어들을 삽입
    for word in words:
        cur.execute(f"""
                    INSERT INTO words(word, game_id)
                    VALUES('{word}', {game_id});
                    """)
        con.commit()
        
    return JSONResponse(content={'game_id': game_id}, status_code=status.HTTP_200_OK)

# 게임 내용 조회
@app.get('/game/{game_id}')
async def get_game(game_id):
    cur = con.cursor()
    image_bytes = cur.execute(f"""
        SELECT image FROM items WHERE id={item_id}
    """).fetchone()[0]
    response = JSONResponse()
    return response

# 토큰 유효성 확인
@app.get('/user')
async def check_user(user=Depends(manager)):
    # 로그인 실패 시 에러 처리
    if not user:
        raise InvalidCredentialsException

    return Response(status_code=status.HTTP_200_OK)

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
