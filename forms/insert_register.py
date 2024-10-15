import streamlit as st
from database.db_handler import Transaction, PaymentMethodEnum, BankEnum, TransactionTypeEnum, save_transaction, get_all_categories
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

            payment_method_enum = next(e for e in PaymentMethodEnum if e.value == forma_pagamento)
            bank_enum = next(e for e in BankEnum if e.value == banco)
            
            # Convertendo a lista de categorias para passar na transação
            new_transaction = Transaction(
                date=data_despesa,
                type_=TransactionTypeEnum.DEBITO.name,
                description=descricao,
                payment_method=payment_method_enum.name,
                bank=bank_enum.name,
                value=valor,
                categories=categorias,
                notes=observacoes
            )

            try:
                save_transaction(new_transaction)
            except Exception as e:
                st.error("Não foi possivel inserir a despesa")

            st.success("✅ Despesa inserida com sucesso!")

# Executando o formulário
if __name__ == "__main__":
    render_form()
