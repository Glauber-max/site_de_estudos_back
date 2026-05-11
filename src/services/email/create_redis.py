import redis

red = redis.Redis(host='localhost', port=6379, decode_responses=True)

def saved_redis(email_end: str, code: str):
    try:
        if red.ping():
            red.setex(email_end, 600, code)
    except Exception as e:
        raise {"error": str(e)}

def compare_redis(email_end: str, code_writed: str):
    try:
        if red.ping():
            code_save = red.get(email_end)
            if code_save == str(code_writed):
                return True
            else:
                return False
    except Exception as e:
        raise {"error": str(e)}