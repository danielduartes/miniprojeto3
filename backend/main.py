from fastapi import FastAPI, APIRouter, HTTPException, Form, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Union
import re
import uvicorn
import base64

from schemas import *
from configBD import run_sql, lifespan
from validar_midia import *

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

# criando rotas
router = APIRouter()


#------------------------ ROTAS ------------------------

# Login
@router.post('/')
def login_user(body: Login_user):
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
        return  {"mensagem": "Login feito com sucesso", "username" : username}

# Cadastrar novo usuário 
@router.post('/register')
def create_user(body: Register_user):
    password_user, email_user, username = body.password_user, body.email_user, body.username # pega os dados

    pattern = '[a-zA-Z0-9_]{3,24}' # caracteres permitidos
    validate_username = bool(re.fullmatch(pattern, username)) # retorna True se valido

    if (validate_username == False):
        raise HTTPException(status_code=400, detail='Usuário inválido')


    exist_user = bool(run_sql(
                        f"""
                        SELECT EXISTS (SELECT 1 FROM users WHERE username = '{username}' LIMIT 1)
                        """)[0][0]
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

    return {'detail' : 'Usuário cadastrado', 'username': username}        

# Criar post
@router.post('/feed/create_post')
async def create_post(username : str = Form(...), text: str = Form(...), midia : Optional[bytes] = Depends(validar_midia)):
    #Usar File e Form juntos quando precisar receber dados e arquivos na mesma requisição.
    # Optional bytes pega os bytes do arquivo
    # A função file espera um arquivo do front e salva como bytes direto, se não receber salva como None
    if midia != None:
        run_sql(
            f"""
            INSERT INTO posts (conteudo, midia, username) 
            VALUES ('{text}', X'{midia.hex()}', '{username}')
        """
        )
    else:
        run_sql(
            f"""
            INSERT INTO posts (conteudo, username) 
            VALUES ('{text}', '{username}')
        """
        )


    return {'detail': 'Post publicado com sucesso'}

# Criar post
@router.post('/feed/create_post/{username}')
async def create_post(username : str, text: str = Form(...), midia : Optional[bytes] = Depends(validar_midia)):
    #Usar File e Form juntos quando precisar receber dados e arquivos na mesma requisição.
    # Optional bytes pega os bytes do arquivo
    # A função file espera um arquivo do front e salva como bytes direto, se não receber salva como None
    if midia != None:
        run_sql(
            f"""
            INSERT INTO posts (conteudo, midia, username) 
            VALUES ('{text}', X'{midia.hex()}', '{username}')
        """
        )
    else:
        run_sql(
            f"""
            INSERT INTO posts (conteudo, username) 
            VALUES ('{text}', '{username}')
        """
        )


    return {'detail': 'Post publicado com sucesso'}

# Editar post
@router.put('/feed/edit_post/{username}')
async def edit_post(username: str, post_id: str, conteudo: str, midia : Optional[bytes] = Depends(validar_midia)):
    owner = (run_sql(f"SELECT username FROM posts WHERE post_id = {post_id}"))
    if not owner or owner[0][0] != username:
        raise HTTPException(status_code=400, detail='Não possui autorização para editar o post')
    
    if midia != None:
        run_sql(
            f"""
            UPDATE posts
            SET conteudo = '{conteudo}', midia = X'{midia.hex()}'
            WHERE post_id = {post_id}
            """)
        midia = base64.b64encode(midia).decode("utf-8")
    else:
        run_sql(
            f"""
            UPDATE posts
            SET conteudo = '{conteudo}'
            WHERE post_id = {post_id}
            """)
        
    return {'detail' : 'Post alterado', 'id_post_changed' : post_id, 'text_edited': conteudo, 'midia_edited': midia}

# Mostra o feed
@router.get('/feed/{username}') # o uso do {username} obriga o front a me enviar um parâmetro informando usuário 
def show_feed(username : str):
    all_posts_infos = []

    # retorna posts do mais recente (id_post maior) para o mais antigo (id_post menor)
    posts = run_sql("SELECT * FROM posts ORDER BY post_id DESC")

    # mostra todos os posts
    for p in posts: 
        # armazena os dados do post e informações de likes e dislikes
        post_id, text, owner_post, midia = p[0], p[1], p[2], p[3]
        likes = []
        dislikes = []

        if midia != None:
            midia = base64.b64encode(midia).decode("utf-8") # converte os bytes em caracteres UTF-8


        # guarda todas as informações de quem interagiu descobre se a interação foi like ou dislike
        interactions = run_sql(
                f"""
                SELECT username, interacao FROM interactions
                WHERE post_id = {post_id}
                """)  
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
            'text' : text,
            'midia' : midia,
            'likes' : likes,
            'dislikes' : dislikes,
            'viewer_is_owner' : True if (owner_post == username) else False, # indica se quem esta vendo é autor
            'viewer_give_like' : True if (username in likes) else False,
            'viewer_give_dislike' : True if (username in dislikes) else False
            }
        )

    # retorna a lista que contém todos os posts 
    return all_posts_infos

# Adicionar interações
@router.post('/feed/{post_id}/interact')
def interact_post(body: Interact, post_id: int):
    
    # descobre se quem está querendo curtir é o dono do post
    is_owner = bool(run_sql(
                        f"""
                        SELECT EXISTS (SELECT 1 FROM posts WHERE post_id = {post_id} AND username = '{body.username}' LIMIT 1)
                        """)[0][0])

    if is_owner:
        raise HTTPException(status_code=400, detail='Não é possível interagir com seu próprio post')

    # descobre se o usuário já interagiu com aquele post 
    already_interact = (run_sql(
                        f"""
                        SELECT username, interacao FROM interactions WHERE post_id = {post_id} AND username = '{body.username}'
                        """))

    if not already_interact: # se não interagiu, então registra a interação 
        run_sql(
                f"""
                INSERT INTO interactions (username, post_id, interacao)
                VALUES ('{body.username}', {post_id}, '{body.type_interact}')
                """)
        detail = "add"
    elif (already_interact[0][1] == body.type_interact): # se interagiu, descobre se a interação foi like ou dislike
        run_sql(
                f"""
                DELETE FROM interactions
                WHERE post_id = {post_id} AND username = '{body.username}'
                """)
        detail = "remove"
    else: # se já interagiu e mudou a reação, então atualiza no banco de dados
        run_sql(
                f"""
                UPDATE interactions
                SET interacao = '{body.type_interact}'
                WHERE post_id = {post_id} AND username = '{body.username}' 
                """)
        detail = "update"

    # detail informa se foi uma operação para adicionar, remover ou atualizar uma interação
    return {'username': body.username, 'post_id': post_id, 'detail': detail, 'interact': body.type_interact}

# adiciona rotas
app.include_router(router=router) 

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)