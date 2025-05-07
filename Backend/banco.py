from configBD import run_sql

run_sql(
        """
        CREATE TABLE IF NOT EXISTS users (
        
        username VARCHAR(24) PRIMARY KEY,
        email_user VARCHAR(255) NOT NULL,
        password_user VARCHAR(255) NOT NULL
        
        )   
        """
    )


run_sql(
    """
    CREATE TABLE IF NOT EXISTS posts(
    
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    conteudo VARCHAR(500) NOT NULL,
    username VARCHAR(24) NOT NULL,
    
    FOREIGN KEY (username) REFERENCES users(username)
    )
    """
)

run_sql(
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