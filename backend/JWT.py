from fastapi import FastAPI, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

app = FastAPI()

@app.post("/generate-token")
def generate_token():
    expiration = datetime.utcnow() + timedelta(minutes=30)
    payload = {"sub": "user_id", "exp": int(expiration.timestamp())}  # Convertido a timestamp UNIX
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/token")
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
