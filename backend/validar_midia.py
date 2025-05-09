from fastapi import FastAPI, APIRouter, HTTPException, Form, File, UploadFile, Depends
from typing import Optional, Union

# Validar mídia enviada
def validar_midia(file: Union[UploadFile, str, None] = File(None)) -> Optional[bytes]:
    # Se veio string vazia (caso típico do Swagger UI), ignora como se nada fosse enviado
    if isinstance(file, str) or file is None or (hasattr(file, "filename") and file.filename == ""):
        return None
    # None atribui ao modelo um valor padrão, tornando-o opcional. O Json não precisa tem essas keys
    # isinstance retorna se objeto pertence àquela classe
    # hasattr verifica se objeto tem aquele atributo
    if file.content_type not in ['image/png', 'image/jpeg']:
        raise HTTPException(status_code=400, detail="Apenas arquivos PNG ou JPG são permitidos")

    return file.file.read()