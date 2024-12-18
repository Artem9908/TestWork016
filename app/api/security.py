from fastapi import HTTPException, Header
from app.core.config import settings

def verify_api_key(authorization: str = Header(...)):
    prefix = "ApiKey "
    if not authorization.startswith(prefix):
        raise HTTPException(status_code=401, detail="Invalid API key format")
    api_key = authorization[len(prefix):]
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
