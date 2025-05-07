import sqlite3
from fastapi import FastAPI

# função que inicializa a aplicação
async def lifespan(app: FastAPI):
    # conecta ao banco de dados
    con = sqlite3.connect('users.db')

    # criar cursor, que permite passar comandos para o sql pelo python
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
        
        username VARCHAR(24) PRIMARY KEY,
        email_user VARCHAR(255) NOT NULL,
        password_user VARCHAR(255) NOT NULL
        
        )   
        """
    )


    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS posts(

        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        conteudo VARCHAR(500) NOT NULL,
        username VARCHAR(24) NOT NULL,

        FOREIGN KEY (username) REFERENCES users(username)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS interactions (

        intera_id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        username VARCHAR(24) NOT NULL,
        interacao VARCHAR(24) NOT NULL,

        FOREIGN KEY (post_id) REFERENCES posts(post_id)
        FOREIGN KEY (username) REFERENCES users(username)
        )
    """
    )

    con.commit()
    yield

def run_sql(sql: str):
    # conecta ao banco de dados
    con = sqlite3.connect('users.db')

    # criar cursor, que permite passar comandos para o sql pelo python
    cur = con.cursor()
    con.execute("PRAGMA foreign_keys = ON;")

    # .execute() executa a instrução passada ao BD
    # retorna uma referência para as linhas citadas do BD
    res = cur.execute(sql)

    # retorna as linhas solicitadas com uma lista com tuplas
    data = res.fetchall()

    # salva as alterações no banco de dados
    con.commit()

    # retorna a lista com as linhas 
    return data