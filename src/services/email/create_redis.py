
import redis
from fastapi import HTTPException
red = redis.Redis(host='localhost', port=6379, decode_responses=True)

def saved_redis(email_end: str, code: str):
    try:
        red.setex(email_end, 600, code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def compare_redis(email_end: str, code_writed: str):
    try:
            code_save = red.get(email_end)
            if code_save == str(code_writed).strip():
                return True
            return False
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))