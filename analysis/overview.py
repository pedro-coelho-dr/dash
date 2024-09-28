import streamlit as st

def overview():
    st.title("Visão Geral do Fluxo de Caixa")

    # Exemplo de KPIs (dados fictícios)
    total_receitas = 5000
    total_despesas = 3000
    saldo_liquido = total_receitas - total_despesas

    # Exibe os KPIs
    st.metric("Total de Receitas", f"R$ {total_receitas}")
    st.metric("Total de Despesas", f"R$ {total_despesas}")
    st.metric("Saldo Líquido", f"R$ {saldo_liquido}")

    # Exemplo de transações recentes (dados fictícios)
    st.subheader("Transações Recentes")
    data = {
        "Data": ["2024-09-01", "2024-09-03", "2024-09-05"],
        "Descrição": ["Venda de Produto", "Serviço de Conserto", "Compra de Ferramentas"],
        "Valor": ["R$ 1000", "R$ 1500", "R$ 500"]
    }
    st.table(data)
