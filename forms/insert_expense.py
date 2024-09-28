import streamlit as st
from database.db_handler import add_transaction  # Importa a função de adicionar transação
from datetime import date

def render_form():
    st.header("Inserir Despesa")

    # Campos do formulário para despesas
    data_despesa = st.date_input("Data da Despesa", value=date.today())
    valor = st.number_input("Valor", min_value=0.0)
    categoria = st.selectbox("Categoria", ["Materiais", "Serviços", "Manutenção", "Salário", "+Adicionar"])
    fornecedor = st.text_input("Fornecedor (Pessoa/Empresa)")
    forma_pagamento = st.selectbox("Forma de Pagamento", ["Transferência Bancária", "Crédito", "Boleto", "Dinheiro"])
    numero_documento = st.text_input("Número do Documento/Recibo/Nota Fiscal")
    periodicidade = st.radio("Periodicidade", ["Pontual", "Recorrente"])  # Esse campo pode ser adicionado ao banco se necessário
    responsavel = st.text_input("Responsável")
    observacoes = st.text_area("Observações (Opcional)")

    # Inserção de despesa
    if st.button("Inserir Despesa"):
        add_transaction(
            date=data_despesa,
            type_="Despesa",
            value=valor,
            category=categoria,
            description=fornecedor,  # Aqui, 'fornecedor' é tratado como descrição
            payment_method=forma_pagamento,
            document_number=numero_documento,
            responsible=responsavel,
            notes=observacoes
        )
        st.success("Despesa inserida com sucesso!")

