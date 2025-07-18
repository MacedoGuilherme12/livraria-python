from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


app = FastAPI()
class Livros(BaseModel):
    titulo_livro: str
    autor_livro: str
    quantidade_livro: int
class LivrosUpdate(BaseModel):
    titulo_livro: str
    autor_livro: Optional[str] = None
    quantidade_livro: Optional[int] = None
livros = {}
chaves_obrigatorias = ["titulo_livro", "autor_livro", "quantidade_livro"]

@app.get("/livros")
def getLivros():
    return list(livros.values())

@app.get("/livros/{id_livro}")
def getLivro(id_livro : int):
    if id_livro not in livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado!")
    return { "livro" : livros[id_livro]}

@app.post("/adiciona")
def postLivros(livro : Livros):
    for existe in livros.values():
        if(livro.quantidade_livro <= 0 ):
            raise HTTPException(status_code=400, detail="Quantidade Invalida!")
        if(existe["titulo_livro"] == livro.titulo_livro):
            raise HTTPException(status_code=400, detail="Livro ja existe!")
    id = len(livros) + 1
    livros[id] = livro.dict()
    return {"msg": "Livro adicionado com sucesso", "livro": livro.dict()}                                                                                                                                                               

@app.put("/altera/{id_livro}")
def putLivros(id_livro : int, livro : LivrosUpdate):
    if id_livro not in livros:
        raise HTTPException(status_code=404, detail="Livro não existe!")
    
    for id_existente, existente in livros.items():
        if id_livro != id_existente and livro.titulo_livro == existente["titulo_livro"]:
            return {"msg" : "O nome que deseja  trocar ja existe!"}
        
    
    if livro.titulo_livro is not None:
        livros[id_livro]['titulo_livro'] = livro.titulo_livro
    else:
        return { "msg" : "Campo obrigatorio não preenchido!", "Campo Obrigatorio" : "titulo_livro"}
    if livro.autor_livro is not None:
        livros[id_livro]['autor_livro'] = livro.autor_livro 
    if livro.quantidade_livro is not None:
        if(livro.quantidade_livro <= 0 ):
            raise HTTPException(status_code=400, detail="Quantidade Invalida!")
        livros[id_livro]['quantidade_livro'] = livro.quantidade_livro
    return {"msg" : "Livro atualizado com sucesso!", "livros alterado" : livros[id_livro]}

@app.delete("/delete/{id_livro}")
def delete_livros(id_livro : int):
    if id_livro not in livros:
        raise HTTPException(status_code=404, detail="ID inexistente!")
    else:
        livro_excluido = livros[id_livro]
        livros.pop(id_livro)
        return { "msg" : "Livro excluido com sucesso!", "Livro Excluido" : livro_excluido}