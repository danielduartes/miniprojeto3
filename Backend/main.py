import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional
import re

from configBD import run_sql, lifespan

# cria o banco de dados
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["*"], # rotas que podem solicitar API
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
) 

 # classe para validar os dados
class User(BaseModel):
    username: str
    email_user: Optional[str] = None
    password_user: str

# criando rotas
router = APIRouter()

# Login
@router.post('/login')
def login_user(body: User):
    password_user, username = body.password_user, body.username

    result_user = run_sql (f"""
        SELECT 
            username,
            password_user

        FROM
            users
        WHERE username = '{username}' AND password_user = '{password_user}'
""") 
    
    #Retorna none se o usuario não for encontrado, retorna um diconario com o usuario e a senha ,caso encontre

    if not result_user :
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
        #o raise para o código para mostrar um erro na tela
        #HTTPException retorna uma mensagem de erro HTTP
    else:
        return  {"mensagem": "Login feito com sucesso", "user" : username}

# Cadastrar novo usuário 
@router.post('/register')
def create_user(body: User):
    password_user, email_user, username = body.password_user, body.email_user, body.username # pega os dados

    pattern = '[a-zA-Z0-9_]{3,24}' # caracteres permitidos
    validate_username = bool(re.fullmatch(pattern, username)) # retorna True se valido

    if (validate_username == False):
        raise HTTPException(status_code=400, detail='Usuário inválido')


    exist_user = run_sql( # retorna linhas em que o username foi encontrado 
        f"""
        SELECT * FROM users WHERE username = '{username}'
        """
    )

    if not exist_user:
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

# Mostra o feed
@router.get('/feed/{username}') # o uso do {username} obriga o front a me enviar um parâmetro informando usuário 
def show_feed(username: str):
    all_posts_infos = []

    # retorna posts do mais recente (id_post maior) para o mais antigo (id_post menor)
    posts = run_sql("SELECT * FROM posts ORDER BY post_id DESC")

    # mostra todos os posts
    for p in posts: 
        # armazena os dados do post
        post_id, conteudo, owner_post = p[0], p[1], p[2]
        likes = []
        dislikes = []

        # guarda todas as informações de quem interagiu
        interactions = run_sql(
                f"""
                SELECT username, interacao FROM interactions
                WHERE post_id = {post_id}
                """)
        
        # descobre se a interação foi like ou dislike
        for i in interactions:
            name, type_interact = i[0], i[1]

            if (type_interact == 'like'):
                likes.append(name)
            else:
                dislikes.append(name)

        # armazena as informações da postagem 
        all_posts_infos.append(
            {
            'post_id' : post_id,
            'owner_post' : owner_post,
            'conteudo' : conteudo,
            'likes' : likes,
            'dislikes' : dislikes,
            'viewer_is_owner' : True if owner_post == username else False, # indica se quem esta vendo é autor
            'viewer_give_like' : True if username in likes else False,
            'viewer_give_dislike' : True if username in dislikes else False
            }
        )

    # retorna a lista que contém todos os posts 
    return all_posts_infos





# adiciona rotas
app.include_router(router=router) 

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)