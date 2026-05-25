import json
import redis
from fastapi import HTTPException
from pydantic import EmailStr
from src.schemas.user_filter import CreateUser
red = redis.Redis(host='localhost', port=6379, decode_responses=True)

def saved_redis(key: str, code: str) -> None:
    try:
        red.setex(key, 300, code)
    except Exception as e:
        print(f"error saving redis: {e}")
        raise HTTPException(status_code=500, detail="internal server error in cache")

def compare_redis_for_change_password(email: EmailStr, token: str) -> bool:
    try:
        redis_key = f"password_reset:{email}"
        token_store = red.get(redis_key)
        if token_store is None:
            raise HTTPException(status_code=404, detail="Password reset token expired or not found")
        return token == token_store
    except HTTPException:
        raise
    except Exception as e:
        print(f"failed in read the redis: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal cache service error"
        )


def redis_create_user(user: CreateUser, token) -> None:
    try:
        redis_key = f"account_validation:{user.email}"
        dados = {
                "name": user.nome,
                "email": user.email,
                "password": user.senha,
                "token": token,
            }
        json_redis = json.dumps(dados)
        red.setex(redis_key, 300, json_redis)
    except Exception as e:
        print(f"failed in create users in redis: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error generating temporary registration cache"
        )

def get_account_after_token_correct(email: EmailStr):
    redis_key = f"account_validation:{email}"
    try:
        json_save = red.get(redis_key)
        if json_save is None:
            raise HTTPException(status_code=404, detail="Activation token expired or not found")
        return json.loads(json_save)
    except HTTPException:
        raise
    except (json.JSONDecodeError, TypeError) as e:
        print(f"json invalid get in redis: {e}")
        raise HTTPException(
            status_code=422,
            detail="Temporary user data is corrupted"
        )
    except Exception as e:
        print(f"failed in read the redis: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error in cache service"
        )


def delete_token_from_redis_after_token(email: EmailStr) -> None:
    try:
        red.delete(f"account_validation:{email}")
        red.delete(f"password_reset:{email}")
    except Exception as e:
        print(f"error in delete the files in redis: {e}")
