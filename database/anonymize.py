import pandas as pd

# Nome do arquivo de entrada e saída
input_file = "database/seed3.csv"
output_file = "database/seed.csv"

# Ler o arquivo CSV
df = pd.read_csv(input_file)

# Substituir os valores das colunas 'description' e 'notes' por 'anonimizado'
df['description'] = "anonimizado"
df['notes'] = "anonimizado"

# Salvar o dataframe em um novo arquivo CSV
df.to_csv(output_file, index=False)

print(f"Arquivo processado e salvo como {output_file}")
