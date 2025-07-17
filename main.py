from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()
class Livros(BaseModel):
    titulo_livro : str
    autor_livro : str
    quantidade_livro: int
livros = {}

@app.get("/livros")
def teste():
    return list(livros.values())

@app.post("/adiciona")
def adicionar(livro : Livros):
    for existe in livros.values():
        if(livro.quantidade_livro <= 0 ):
            raise HTTPException(status_code=400, detail="Quantidade Invalida")
        if(existe["titulo_livro"] == livro.titulo_livro):
            raise HTTPException(status_code=400, detail="Livro ja existe!!")
    id = len(livros) + 1
    livros[id] = livro.dict()
    return {"msg": "Livro adicionado com sucesso", "livro": livro.dict()}                                                                                                                                                               

@app.put("/altera/{id_livro}")
def altera(id_livro : int, livro : Livros):

    if id_livro not in livros:
        raise HTTPException(status_code=404, detail="Livro não existe")
    for id_existente, existente in livros.items():
        if id_livro != id_existente and livro.titulo_livro == existente["titulo_livro"]:
            return {"msg" : "O nome que deseja  trocar ja existe"}
    livros[id_livro] = livro.dict()
    return {"msg" : "Livro atualizado com sucesso", "livros alterado" : livros[id_livro]}


