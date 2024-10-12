import streamlit as st
from database.db_handler import add_transaction, get_all_categories, PaymentMethodEnum, BankEnum, TransactionTypeEnum
from datetime import date

# Renderização do formulário de inserção de receitas
def render_form():
    with st.form(key='revenue_form'):

        col1, col2 = st.columns(2)
        valor = col1.number_input("💵 Valor (R$)", min_value=0.0, format="%.2f")
        data_receita = col2.date_input("📅 Data da Receita", value=date.today())

    
        descricao = st.text_input("📝 Origem", placeholder="Nome da origem ou descrição da receita")

        categorias = st.multiselect("📂 Categorias", get_all_categories(), default=[])

        col3, col4 = st.columns(2)

        forma_pagamento = col3.selectbox("💳 Forma de Pagamento", [e.value for e in PaymentMethodEnum])
        banco = col4.selectbox("🏦 Banco", [e.value for e in BankEnum])

        
        observacoes = st.text_area("✏️ Observações (Opcional)", placeholder="Detalhes adicionais sobre a receita")
        
        # Separador visual
        st.markdown("---")

        # Botão para submeter o formulário
        if st.form_submit_button("💾 Inserir Receita"):
            add_transaction(
                date=data_receita,
                type_=TransactionTypeEnum.CREDITO.value,
                description=descricao,
                payment_method=forma_pagamento,
                bank=banco,
                value=valor,
                categories=categorias,  # Passar a lista de categorias
                notes=observacoes
            )
            st.success("✅ Receita inserida com sucesso!")

# Executando o formulário
if __name__ == "__main__":
    render_form()
