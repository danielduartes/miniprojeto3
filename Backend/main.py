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

# O QUE FALTA:
# 1. Criar validação de login 
#    - Verificar se usuário existe e verificar senha digitada
#    - Se existe, continua. Se não, pede para cadastrar

# 2. Cadastro no site e validação de usuário
#    - Verificar se username já existe no banco de dados
#    - Se não existe, adiciona. Se existe, dá erro 

# Cadastrar novo usuário 
@router.post('/register')
def create_user(body: User):
    password_user, email_user, username = body.password_user, body.email_user, body.username

    run_sql(
        f"""
        INSERT INTO users (username, password_users, email_users)
        VALUES ('{username}', '{password_user}', '{email_user}')
        """
    ) 


# adiciona rotas no site
app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)