# ☁️ Nimbo
Este projeto é parte da disciplina **Projetos 5** do curso de **Ciência da Computação** e **Design** da [**Cesar School**](https://cesar.school). O objetivo deste aplicativo é fornecer uma plataforma de gestão financeira para a [Eceel-Tec](https://eceel-tec.com.br/) uma empresa de assistência técnica, permitindo o acompanhamento de entradas, saídas, e visualização e análise avançada de dados financeiros.

## Status
Estamos na fase do Status Report 1, focada na aquisição e análise inicial de dados, definição de métricas de desempenho, e criação das primeiras visualizações. O protótipo atual está em desenvolvimento, com as funcionalidades principais sendo testadas e refinadas.

**Próximos Passos:**
- Análise Aprofundada: Aplicação de técnicas de análise mais complexas, como análise multivariada, relacionando múltiplas variáveis para insights mais ricos.
- Dashboard Baseado em Métricas: Expansão do dashboard atual para incluir as métricas e indicadores definidos, apresentando uma visualização mais detalhada e informativa.
- Storytelling com Dados: Desenvolvimento de técnicas de apresentação para comunicar insights de forma clara e impactante, utilizando storytelling com os dados.


## Instalação e Execução
### Pré-requisitos
- **Python**
- **Streamlit** e outras bibliotecas listadas em `requirements.txt`.

### Instruções para Linux

- Clone o repositório:
   ```bash
   git clone https://github.com/pedro-coelho-dr/dash.git
   ```
   ```bash
   cd dash
   ```

- Crie e ative o ambiente virtual:   
  
    Linux:
   ```bash
   python3 -m venv venv
   ```
   ```bash
   source venv/bin/activate
   ```
    Windows:
   ```bash
   python -m venv venv
   ```
   ```bash
   venv\Scripts\activate
   ```

- Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

 - Rode o app:
   ```bash
   streamlit run app.py
   ```
---

## Vídeo Demo

[![alt text](/screenshots/yt.png)](https://youtu.be/4o1jFVl1eh8)

## Como Usar

### Menu Principal  
Escolha entre as opções para gerenciar, inserir receitas ou despesas.

![menu principal](screenshots/image.png)

### Visão Geral  
Acompanhe um resumo financeiro com receitas, despesas e saldo líquido. Utilize filtros de período para refinar a visualização.

![visão geral](screenshots/image-1.png)

### Análise Avançada  
Explore gráficos detalhados sobre receitas e despesas, filtrando por ano e mês.

![análise avançada](screenshots/image-2.png)

### Gerenciar Transações  
Pesquise, edite ou exclua transações. Utilize filtros de tipo, categoria e data para encontrar rapidamente o que precisa.

![gerenciar transações](screenshots/image-3.png)

![editar transações](screenshots/image-4.png)

### Inserir Receita/Despesa  
Adicione novas transações com detalhes como valor, categoria, forma de pagamento, e banco.

![inserir receita/despesa](screenshots/image-6.png)

## Análise e Visualização de Dados

### Receitas e Despesas ao Longo do Tempo
Gráfico de linha que mostra a variação de receitas (verde) e despesas (vermelho) ao longo das datas.

![alt text](screenshots/image_0.png)

### Histórico de Saldo
Gráfico que exibe a evolução do saldo acumulado ao longo do tempo, calculado com base em receitas e despesas.

![alt text](/screenshots/image-5.png)

### Métodos de Pagamento e Bancos Utilizados
Gráficos donut quem representam a proporção de cada método de pagamento e bancos utilizados.

![alt text](screenshots/image_01.png)

## Gráfico Sunburst (Porcentagens de Receita e Despesa por Categoria)
Mostra interativamente a distribuição de receitas e despesas por categorias, facilitando a visualização de quais categorias representam maiores porcentagens em cada tipo (Receita/Despesa).

![alt text](/screenshots/newplot_(2).png)  
![alt text](/screenshots/newplotx.png)

### Gráficos de Dispersão (Valor por Categoria)
Dois gráficos de dispersão, um para receitas e outro para despesas, que mostram o valor de cada transação por categoria, representando a magnitude com o tamanho dos pontos.

![alt text](/screenshots/newplot_(3).png)

![alt text](/screenshots/newplot_(4).png)

### Gráfico de Barras Sobrepostas (Receita e Despesa por Categoria)
Compara lado a lado as receitas e despesas por categorias, utilizando cores distintas para receitas (verde) e despesas (vermelho).

![alt text](/screenshots/newplot_(5).png)




## Equipe

- Caio Hirata
- Camila Cirne
- Clara Wanderley
- Gabriela Viana
- Leo Kaiser
- Pedro Coelho
- Virna Amaral
- Yara Rodrigues