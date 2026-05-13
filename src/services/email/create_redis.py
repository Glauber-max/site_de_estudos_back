import json
import redis
from fastapi import HTTPException
from pydantic import EmailStr

from src.schemas.user_filter import CreateUser
#create redis conection (redis in docker)
red = redis.Redis(host='localhost', port=6379, decode_responses=True)

#get a token, and email and also set in memory, after 600 seconds it is deleted
def saved_redis(nome: str, code: str):
    try:
        red.setex(nome, 600, code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#simple function for get the code and compare, if True, return True, else, return False
def compare_redis(email_end: str, code_write: str):
    try:
            code_save = red.get(email_end)
            if code_save == str(code_write).strip():
                return True
            return False
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def redis_create_user(user: CreateUser):
    try:
        dados = {
                "name": user.nome,
                "email": user.email,
                "password": user.senha,
            }
        json_redis = json.dumps(dados)
        red.setex(user.email, 600, json_redis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_account_after_token_correct(email: EmailStr):
    json_save = red.get(email)
    if json_save is None:
        raise HTTPException(status_code=404, detail="email pass time")
    return json_save
