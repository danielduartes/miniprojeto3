import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from configBD import run_sql

app = FastAPI()

run_sql(
    """
    CREATE TABLE IF NOT EXISTS users (
        name_users INTEGER PRIMARY KEY AUTOINCREMENT,
        password_users TEXT NOT NULL,
        email_users TEXT NOT NULL
    )
    """
)

# middleware 
app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["*"], # rotas que podem solicitar API
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

# O QUE FALTA:
# 1. Criar validação de login 
#    - Verificar se usuário existe e verificar senha digitada
#    - Se existe, continua. Se não, pede para cadastrar

@router.post('/login')
def create_user(body: User):
    password_user, username = body.password_user, body.username

    result_user = run_sql (f"""
        SELECT 
            name_users,
            password_users

        FROM
            users
        WHERE name_users = '{username}' AND password_users = '{password_user}'
""", fetch_one = True) 
    #Retorna none se o usuario não for encontrado, retorna um diconario com o usuario e a senha ,caso encontre


    if not result_user :
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
        #o raise para o código para mostrar um erro na tela
        #HTTPException retorna uma mensagem de erro HTTP
    else:
        return  {"mensagem": "Login feito com sucesso"}


# adiciona rotas no site
app.include_router(router=router)
