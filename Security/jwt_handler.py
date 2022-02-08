from typing import Dict
from decouple import config
import time,jwt



JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    return {
         token
    }


    
def signJWT(mobile_number: str)-> Dict[str, str]:
    payload = {
        "mobile_number": mobile_number,
        "expires": time.time()+1000
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)




def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token["expires"] >= time.time() else None
    except:
        return {}