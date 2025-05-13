from pydantic import BaseModel
from fastapi import Form, File, UploadFile
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

# Dados para deletar posts
class Delete(BaseModel):
    post_id : int

class Interact(BaseModel):
    username : str
    type_interact : str
