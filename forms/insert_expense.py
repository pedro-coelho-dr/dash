import streamlit as st
from database.db_handler import add_transaction, get_all_categories, PaymentMethodEnum, BankEnum, TransactionTypeEnum
from datetime import date

# Renderização do formulário de inserção de despesas
def render_form():

    with st.form(key='expense_form'):

        col1, col2 = st.columns(2)
        valor = col1.number_input("💵 Valor (R$)", min_value=0.0, format="%.2f")
        data_despesa = col2.date_input("📅 Data da Despesa", value=date.today())
        
        descricao = st.text_input("📝 Destinatário", placeholder="Nome do destinatário ou descrição da despesa")
        
        categorias = st.multiselect("📂 Categorias", get_all_categories(), default=[])

        col3, col4 = st.columns(2)
        forma_pagamento = col3.selectbox("💳 Forma de Pagamento", [e.value for e in PaymentMethodEnum])
        banco = col4.selectbox("🏦 Banco", [e.value for e in BankEnum])

        observacoes = st.text_area("✏️ Observações (Opcional)", placeholder="Detalhes adicionais sobre a despesa")
        
        st.markdown("---")

        # Botão para submeter o formulário
        if st.form_submit_button("💾 Inserir Despesa"):
            # Convertendo a lista de categorias para passar na transação
            add_transaction(
                date=data_despesa,
                type_=TransactionTypeEnum.DEBITO.name,
                description=descricao,
                payment_method=PaymentMethodEnum[forma_pagamento].name,
                bank=BankEnum[banco].name,
                value=valor,
                categories=categorias,
                notes=observacoes
            )
            st.success("✅ Despesa inserida com sucesso!")

# Executando o formulário
if __name__ == "__main__":
    render_form()
