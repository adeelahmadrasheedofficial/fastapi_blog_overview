from jose import JWSError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# SECRET_KEY
# Algorithm
# Expiry Time

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_access_token(token: str, credentails_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentails_exception
        token_data = schemas.TokenData(id=id)
        # return token_data
    except JWSError:
        raise credentails_exception
    return token_data

# once the verify_access_token returns the token data which is ID
# then get_current_user function fetch the user from the database
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized User/ Unalbe to verify credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    # verifying access token
    token = verify_access_token(token, credentials_exception) 
    # making database request
    user = db.query(models.User).filter(models.User.uuid == token.id).first()
    return user