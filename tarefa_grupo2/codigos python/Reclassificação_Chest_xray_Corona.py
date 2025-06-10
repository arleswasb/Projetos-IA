#codigo elaborado para reclassificar o database Chest X-ray Corona Metadata
#inserindo uma nova coluna de classificação
#e removendo as linhas que não se encaixam nas categorias de pneumonia
#bem como descartando colunas desnecessárias

import pandas as pd

# Carrega o dataset
df = pd.read_csv('coronahack_dataset\Chest_xray_Corona_Metadata.csv')

# Cria a nova coluna de classificação
df['Tipo_Classificacao'] = ''

# Preenche a nova coluna com base nas condições corrigidas
# Classifica como 'Normal'
df.loc[df['Label'] == 'Normal', 'Tipo_Classificacao'] = 'Normal'

# Classifica como 'Pneumonia Viral' (considerando o erro de digitação 'Pnemonia' e 'Virus')
df.loc[(df['Label'] == 'Pnemonia') & (df['Label_1_Virus_category'] == 'Virus'), 'Tipo_Classificacao'] = 'Pneumonia Viral'

# Classifica como 'Pneumonia Bacteriana' (considerando o erro de digitação 'Pnemonia' e 'bacteria' em minúsculas)
df.loc[(df['Label'] == 'Pnemonia') & (df['Label_1_Virus_category'] == 'bacteria'), 'Tipo_Classificacao'] = 'Pneumonia Bacteriana'

# Classifica outras pneumonias que não se encaixam nas categorias Viral ou Bacteriana
df.loc[(df['Label'] == 'Pnemonia') & (~df['Label_1_Virus_category'].isin(['Virus', 'bacteria'])), 'Tipo_Classificacao'] = 'Outros tipos de Pneumonia'

# remove as linhas onde a coluna 'Tipo Classificacao' = outros tipos de pneumonia
df = df[df['Tipo_Classificacao'] != 'Outros tipos de Pneumonia']
#        
# Descarta as colunas especificadas
df = df.drop(columns=['Dataset_type', 'Label_2_Virus_category'])

# Exibe as primeiras 5 linhas da nova tabela e a contagem de valores da nova coluna de classificação
print("Primeiras 5 linhas da nova tabela:")
print(df.head())
print("\nContagem de valores na nova coluna 'Tipo_Classificacao':")
print(df['Tipo_Classificacao'].value_counts())

# Salva a nova tabela em um arquivo CSV
df.to_csv('Chest_xray_Corona_Metadata_Classified.csv', index=False)
print("\nNova tabela 'Chest_xray_Corona_Metadata_Classified.csv' gerada com sucesso!")