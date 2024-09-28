import streamlit as st
from database.db_handler import add_transaction  # Importa a função de adicionar transação
from datetime import date

def render_form():
    st.header("Inserir Receita")

    # Campos do formulário para receitas
    data_recebimento = st.date_input("Data de Recebimento", value=date.today())
    valor = st.number_input("Valor", min_value=0.0)
    origem = st.selectbox("Origem", ["Cliente", "Serviço Específico", "Venda de Produto", "Outro"])
    forma_pagamento = st.selectbox("Forma de Pagamento", ["Transferência Bancária", "Crédito", "Boleto", "Dinheiro"])
    numero_documento = st.text_input("Número do Documento/Recibo/Nota Fiscal")
    categoria = st.selectbox("Categoria", ["Venda de Produto", "Prestação", "Outro"])
    responsavel = st.text_input("Responsável")
    observacoes = st.text_area("Observações (Opcional)")

    # Inserção de receita
    if st.button("Inserir Receita"):
        add_transaction(
            date=data_recebimento,
            type_="Receita",
            value=valor,
            category=categoria,
            description=origem,  # Aqui, 'origem' é tratado como descrição
            payment_method=forma_pagamento,
            document_number=numero_documento,
            responsible=responsavel,
            notes=observacoes
        )
        st.success("Receita inserida com sucesso!")
