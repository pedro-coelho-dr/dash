import streamlit as st
from database.db_handler import Transaction, PaymentMethodEnum, BankEnum, TransactionTypeEnum, update_transaction, get_all_categories
from datetime import date

# Função para renderizar o formulário de edição de transação
def render_formulario_edicao(transaction):
    st.title("✏️ Editar Transação")

    # Determina o tipo de registro com base na transação fornecida
    tipo_Registro = "Despesa" if transaction.type == TransactionTypeEnum.DEBITO.name else "Receita"

    # Seleção do tipo de Registro
    tipo_Registro = st.selectbox("💼 Tipo de Registro", ["Despesa", "Receita"], index=0 if tipo_Registro == "Despesa" else 1)

    with st.form(key='edicao_form'):
        col1, col2 = st.columns(2)
        valor = col1.number_input("💵 Valor (R$)", min_value=0.0, format="%.2f", value=transaction.value)
        data_Registro = col2.date_input("📅 Data do Registro", value=transaction.date)

        descricao = st.text_input("📝 Descrição", placeholder="Nome ou descrição do Registro", value=transaction.description)
        categorias = st.multiselect("📂 Categorias", get_all_categories(), default=[cat.name for cat in transaction.categories])

        col3, col4 = st.columns(2)
        forma_pagamento = col3.selectbox("💳 Forma de Pagamento", [e.value for e in PaymentMethodEnum], index=[e.value for e in PaymentMethodEnum].index(PaymentMethodEnum[transaction.payment_method].value))
        banco = col4.selectbox("🏦 Banco", [e.value for e in BankEnum], index=[e.value for e in BankEnum].index(BankEnum[transaction.bank].value))

        observacoes = st.text_area("✏️ Observações (Opcional)", placeholder="Detalhes adicionais sobre o Registro", value=transaction.notes)

        st.markdown("---")

        # Botão para submeter o formulário
        if st.form_submit_button("💾 Atualizar Registro"):
            payment_method_enum = next(e for e in PaymentMethodEnum if e.value == forma_pagamento)
            bank_enum = next(e for e in BankEnum if e.value == banco)

            # Define o tipo da transação com base na seleção
            tipo = TransactionTypeEnum.DEBITO.name if tipo_Registro == "Despesa" else TransactionTypeEnum.CREDITO.name
            
            # Atualizando a transação existente
            updated_transaction = Transaction(date = data_Registro,
                        type = tipo,
                        description = descricao,
                        payment_method = payment_method_enum.name,
                        bank = bank_enum.name,
                        value = valor,
                        categories = categorias,
                        notes = observacoes
                        )
            
            try:
                update_transaction(updated_transaction)
                st.success("✅ Registro atualizado com sucesso!")
            except Exception as e:
                st.error(f"❌ Não foi possível atualizar o Registro: {e}")

# Executando o formulário
if __name__ == "__main__":
    # Aqui você deve fornecer a transação que deseja editar
    # Exemplo: transacao = get_transaction(1)
    transaction = Transaction(
        date=date.today(),
        type=TransactionTypeEnum.DEBITO.name,
        description="Exemplo de Despesa",
        payment_method=PaymentMethodEnum.CASH.name,
        bank=BankEnum.BRAZIL_BANK.name,
        value=100.0,
        categories=["Alimentação"],
        notes="Notas de exemplo"
    )
    
    render_formulario_edicao(transaction)
