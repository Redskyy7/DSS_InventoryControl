from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import database 
import os

# Configuração do PostgreSQL
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("PGHOST"),
    "database": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
    "port": os.getenv("PGPORT")
}

database.criar_banco(DB_CONFIG)

# Criação da URL de conexão do PostgreSQL
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Criando conexão com o banco
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo do Banco de Dados
class ProdutoDB(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    estoque = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)

# Criando as tabelas
Base.metadata.create_all(bind=engine)

# Inicializando a API
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8501", "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Modelo para entrada de dados
class Produto(BaseModel):
    nome: str
    estoque: int
    preco: float

# Endpoint para adicionar produtos
@app.post("/produtos/")
def adicionar_produto(produto: Produto):
    db = SessionLocal()
    novo_produto = ProdutoDB(nome=produto.nome, estoque=produto.estoque, preco=produto.preco)
    db.add(novo_produto)
    db.commit()
    db.close()
    return {"mensagem": "Produto adicionado com sucesso!"}

# Endpoint para listar produtos
@app.get("/produtos/")
def listar_produtos():
    db = SessionLocal()
    produtos = db.query(ProdutoDB).all()
    db.close()

    return [{"id": p.id, "nome": p.nome, "estoque": p.estoque, "preco": p.preco} for p in produtos]
""
# Endpoint para atualizar o estoque
@app.put("/produtos/{produto_id}")
def atualizar_estoque(produto_id: int, novo_estoque: int):
    db = SessionLocal()
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if not produto:
        db.close()
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    produto.estoque = novo_estoque
    db.commit()
    db.close()
    return {"mensagem": "Estoque atualizado!"}

# Endpoint para deletar um produto
@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int):
    db = SessionLocal()
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if not produto:
        db.close()
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    db.close()
    return {"mensagem": "Produto deletado!"}