import sqlite3

def run_sql(sql: str):
    # conecta ao banco de dados
    con = sqlite3.connect('users.db')

    # criar cursor, que permite passar comandos para o sql pelo python
    cur = con.cursor()

    # .execute() executa a instrução passada ao BD
    # retorna uma referência para as linhas citadas do BD
    res = cur.execute(sql)

    # retorna as linhas solicitadas com uma lista com tuplas
    data = res.fetchall()

    # salva as alterações no banco de dados
    con.commit()

    # retorna a lista com as linhas 
    return data