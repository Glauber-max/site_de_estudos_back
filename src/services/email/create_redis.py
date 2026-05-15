import json
import redis
from fastapi import HTTPException
from pydantic import EmailStr

from src.schemas.user_filter import CreateUser
#create redis conection (redis in docker)
red = redis.Redis(host='localhost', port=6379, decode_responses=True)

#get a token, and email and also set in memory, after 600 seconds it is deleted
def saved_redis(key: str, code: str):
    try:
        red.setex(key, 300, code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def compare_redis_for_change_password(email: EmailStr, token: str):
    try:
        token_store = red.get(email)
        if token_store is None:
            raise HTTPException(status_code=404, detail="email pass time")
        if token == token_store:
            return True
        return False
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def redis_create_user(user: CreateUser, token):
    try:
        dados = {
                "name": user.nome,
                "email": user.email,
                "password": user.senha,
                "token": token,
            }
        json_redis = json.dumps(dados)
        red.setex(user.email, 300, json_redis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_account_after_token_correct(email: EmailStr):
    json_save = red.get(email)
    if json_save is None:
        raise HTTPException(status_code=404, detail="email pass time")
    json_result = json.loads(json_save)
    return json_result

def delete_account_after_token(email: EmailStr) -> None:
    red.delete(email)
