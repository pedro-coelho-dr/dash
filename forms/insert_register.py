import streamlit as st
from database.db_handler import Transaction, PaymentMethodEnum, BankEnum, TransactionTypeEnum, save_transaction, get_all_categories
from datetime import date

# Função para renderizar o formulário genérico
def render_formulario_registros():
    st.title("📋 Formulário de Registros")

    # Seleção do tipo de Registro
    tipo_Registro = st.selectbox("💼 Tipo de Registro", ["Despesa", "Receita"])

    with st.form(key='registro_form'):
        col1, col2 = st.columns(2)
        valor = col1.number_input("💵 Valor (R$)", min_value=0.0, format="%.2f")
        data_Registro = col2.date_input("📅 Data da Registro", value=date.today())

        descricao = st.text_input("📝 Descrição", placeholder="Nome ou descrição da Registro")
        categorias = st.multiselect("📂 Categorias", get_all_categories(), default=[])

        col3, col4 = st.columns(2)
        forma_pagamento = col3.selectbox("💳 Forma de Pagamento", [e.value for e in PaymentMethodEnum])
        banco = col4.selectbox("🏦 Banco", [e.value for e in BankEnum])

        observacoes = st.text_area("✏️ Observações (Opcional)", placeholder="Detalhes adicionais sobre a Registro")

        st.markdown("---")

        # Botão para submeter o formulário
        if st.form_submit_button("💾 Inserir Registro"):
            payment_method_enum = next(e for e in PaymentMethodEnum if e.value == forma_pagamento)
            bank_enum = next(e for e in BankEnum if e.value == banco)

            # Define o tipo da Registro com base na seleção
            tipo = TransactionTypeEnum.DEBITO.name if tipo_Registro == "Despesa" else TransactionTypeEnum.CREDITO.name
            
            # Criando a nova Registro
            new_transaction = Transaction(
                date=data_Registro,
                type=tipo,
                description=descricao,
                payment_method=payment_method_enum.name,
                bank=bank_enum.name,
                value=valor,
                categories=categorias,
                notes=observacoes
            )

            try:
                save_transaction(new_transaction)
                st.success("✅ Registro inserida com sucesso!")
            except Exception as e:
                st.error(f"❌ Não foi possível inserir o Registro: {e}")

# Executando o formulário
if __name__ == "__main__":
    render_formulario_registros()
