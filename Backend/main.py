import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from configBD import run_sql

app = FastAPI()

# middleware 
app.add_middleware(
    CORSMiddleware, 
    allow_origin = ["*"], # rotas que podem solicitar API
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
) 

# classe para validar os dados
class User(BaseModel):
    username: str
    email_user: str
    password_user: str

# criando rotas
router = APIRouter()

# Cadastrar novo usuário 
@router.post('/register')
def create_user(body: User):
    password_user, email_user, password_user = body.password_user, body.email_user, body.username
    




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)