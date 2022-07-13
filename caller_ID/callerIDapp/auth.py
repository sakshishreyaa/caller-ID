from base64 import encode
import datetime
import jwt
import os
SECRET_KEY = os.getenv("SECRET_KEY","secret")

from .models import CustomUser
def generate_token(phone):
    json_data = {
        "user_id": phone,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=86400)
    }

    encoded_data = jwt.encode(payload=json_data, key=SECRET_KEY)
    return encoded_data

def decode_token(token):
    try:
        decode_data = jwt.decode(jwt=token,key=SECRET_KEY,algorithms='HS256')
        return decode_data
    except Exception as e:
        message = f"Token is invalid --> {e}"
        return message


def authenticate(token):
    token=token.split()[1]
    decoded = decode_token(token)
    print(decoded)
    int(datetime.datetime.utcnow().timestamp())
    if CustomUser.objects.filter(phone=decoded['user_id']).first() and decoded['exp'] > int(datetime.datetime.utcnow().timestamp()):
        return True
    return False