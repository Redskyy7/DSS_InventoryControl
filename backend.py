from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Criando a conexão com o banco de dados SQLite
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Criando a tabela se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        estoque INTEGER NOT NULL,
        preco REAL NOT NULL
    )
""")
conn.commit()

# Modelo para adicionar produtos
class Produto(BaseModel):
    nome: str
    estoque: int
    preco: float

# Endpoint para adicionar produtos
@app.post("/produtos/")
def adicionar_produto(produto: Produto):
    cursor.execute("INSERT INTO produtos (nome, estoque, preco) VALUES (?, ?, ?)",
                   (produto.nome, produto.estoque, produto.preco))
    conn.commit()
    return {"mensagem": "Produto adicionado com sucesso!"}

# Endpoint para listar produtos
@app.get("/produtos/")
def listar_produtos():
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    return [{"id": p[0], "nome": p[1], "estoque": p[2], "preco": p[3]} for p in produtos]

# Endpoint para atualizar o estoque
@app.put("/produtos/{produto_id}")
def atualizar_estoque(produto_id: int, novo_estoque: int):
    cursor.execute("UPDATE produtos SET estoque = ? WHERE id = ?", (novo_estoque, produto_id))
    conn.commit()
    return {"mensagem": "Estoque atualizado!"}

# Endpoint para deletar um produto
@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int):
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    return {"mensagem": "Produto deletado!"}