import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

from configBD import run_sql

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["*"], # rotas que podem solicitar API
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
) 

class User(BaseModel): # classe para validar os dados
    username: str
    email_user: str
    password_user: str

router = APIRouter() # criando rotas


# Cadastrar novo usuário 
@router.post('/register')
def create_user(body: User):
    password_user, email_user, username = body.password_user, body.email_user, body.username # pega os dados

    pattern = '[a-zA-Z0-9_]{3,16}' # caracteres permitidos
    validate_username = bool(re.fullmatch(pattern, username)) # retorna True se valido

    if (validate_username == False):
        raise HTTPException(status_code=400, detail='Usuário inválido')


    data = run_sql( # retorna linhas em que o username foi encontrado 
        f"""
        SELECT * FROM users WHERE username = '{username}'
        """
    )

    if data == []:
        try:
            run_sql(
                f"""
                INSERT INTO users (username, password_user, email_user)
                VALUES ('{username}', '{password_user}', '{email_user}')
                """
            )
        except:
            raise HTTPException(status_code=400, detail='Não foi possível cadastrar usuário')
    else:
        raise HTTPException(status_code=400, detail='Usuário não disponível')

    return {'detail' : 'Usuário cadastrado'}        




app.include_router(router=router) # adiciona rotas

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)