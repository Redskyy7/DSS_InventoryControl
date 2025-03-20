import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

headers = {
    "User-Agent": "Mozilla/5.0"
}

st.title("📦 Controle de Estoque - SAD")

# Listar produtos
st.subheader("📋 Produtos em Estoque")
if st.button("🔄 Atualizar Lista"):
    response = requests.get(f"{API_URL}/produtos/", headers=headers)
    if response.status_code == 200 and response.text.strip():
        try:
            produtos = response.json()
            if produtos:
                df = pd.DataFrame(produtos)
                df["preco"] = df["preco"].apply(lambda x: f"R$ {x:.2f}")
                st.table(df)
            else:
                st.warning("Nenhum produto encontrado.")
        except requests.exceptions.JSONDecodeError:
            st.error("Erro ao processar os dados do servidor.")
    else:
        st.warning("Nenhum dado retornado pelo servidor.")

# Adicionar produto
st.subheader("➕ Adicionar Novo Produto")
nome = st.text_input("Nome do Produto")
estoque = st.number_input("Quantidade", min_value=0)
preco = st.number_input("Preço Unitário", min_value=0.0, format="%.2f")
if st.button("Adicionar Produto"):
    if nome and estoque >= 0 and preco > 0:
        response = requests.post(f"{API_URL}/produtos/", json={"nome": nome, "estoque": estoque, "preco": preco})
        st.success(response.json()["mensagem"])
    else:
        st.error("Preencha os campos corretamente!")
        
# Atualizar estoque
st.subheader("🔄 Atualizar Estoque")
produto_id = st.number_input("ID do Produto", min_value=1)
novo_estoque = st.number_input("Novo Estoque", min_value=0)
if st.button("Atualizar Estoque"):
    response = requests.put(f"{API_URL}/produtos/{produto_id}?novo_estoque={novo_estoque}")
    st.success(response.json()["mensagem"])

# Deletar produto
st.subheader("❌ Remover Produto")
produto_id_del = st.number_input("ID do Produto a Deletar", min_value=1)
if st.button("Deletar Produto"):
    response = requests.delete(f"{API_URL}/produtos/{produto_id_del}")
    st.success(response.json()["mensagem"])