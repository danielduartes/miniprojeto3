from pydantic import BaseModel

# schemas: define qual deve ser o formato dos dados e entradas aceitas pela API
# este código define como o front end deve enviar cada requisição para a API

# Dados necessários para registrar
class Register_user(BaseModel):
    username: str
    email_user: str
    password_user: str

# Dados necessários para login
class Login_user(BaseModel):
    username : str
    password_user : str

# Dados para postar
class Post(BaseModel):
    username : str
    conteudo : str

# Dados para editar
class Edit_post(BaseModel):
    username : str
    post_id : int
    conteudo : str

# Para mostrar no feed
class Show_feed(BaseModel):
    username : str

class Delete(BaseModel):
    username : str
    post_id : int
