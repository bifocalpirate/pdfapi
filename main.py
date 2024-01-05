import uuid
from fastapi import FastAPI, HTTPException, status, Security
from pydantic import BaseModel
import pdfkit
from fastapi.responses import FileResponse
from api_keys import API_KEYS
from fastapi.security import APIKeyHeader, APIKeyQuery


api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

app = FastAPI()


class PayLoad(BaseModel):
    htmlContent:str

def get_api_key(api_key_query:str = Security(api_key_query), api_key_header:str = Security(api_key_header))->str:
    if api_key_query in API_KEYS:                
        return api_key_query
    if api_key_header in API_KEYS:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API key"
    )        

@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.post("/generate")
def generate_pdf(item:PayLoad, api_key:str=Security(get_api_key)):
    file_name = '{}{:-%Y%m%d%H%M%S}.pdf'.format(str(uuid.uuid4().hex), datetime.now())
    pdfkit.from_string(item.htmlContent, file_name)
    return FileResponse(file_name)
    


