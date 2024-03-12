import requests
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


orig_url='https://drive.google.com/file/d/1UrlwBHa47H5lpAkLtDsfuEWfTMQj491X/view?usp=sharing'


file_id = orig_url.split('/')[-2]
dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
url = requests.get(dwn_url).text
csv_raw = StringIO(url)
df_servidores = pd.read_csv(csv_raw,sep=';',low_memory=False)
pd.set_option('display.max_rows', None)
df_servidores['BRUTO'] = df_servidores['BRUTO'].str.replace(',', '').astype(float)
df_servidores['LÍQUIDO'] = df_servidores['LÍQUIDO'].str.replace(',', '').astype(float)   
df_servidores['REMUNERAÇÃO BÁSICA'] = df_servidores['REMUNERAÇÃO BÁSICA'].str.replace(',', '').astype(float)   
df_servidores['IRRF'] = df_servidores['IRRF'].str.replace(',', '.').astype(float)


print('1) Qual o espaço amostral compreendido nesta base de dados?')
df_servidores.shape[0]
# 237125


print('2) Quantos servidores estão lotados no corpo de bombeiros?')
servidores_bombeiros = df_servidores['ÓRGÃO'].value_counts()['CORPO DE BOMBEIRO MILITAR DO DISTRITO FEDERAL - SIAPE']
print("Número de servidores lotados no Corpo de Bombeiros:", servidores_bombeiros)

dados_bombeiros = df_servidores[df_servidores['ÓRGÃO'] == 'CORPO DE BOMBEIRO MILITAR DO DISTRITO FEDERAL - SIAPE']

servidores_bombeiros_calculado = len(dados_bombeiros)

if servidores_bombeiros_calculado == servidores_bombeiros:
    print("A validação foi bem-sucedida. O número de servidores lotados no Corpo de Bombeiros é consistente.")
else:
    print("A validação falhou. O número de servidores lotados no Corpo de Bombeiros não corresponde ao valor anteriormente calculado.")


print('3) Qual o órgão público com maior número de funcionários?') 
orgao_maior_numero = df_servidores['ÓRGÃO'].value_counts().idxmax()
print(orgao_maior_numero)


print('4) Qual a probabilidade de ao escolher uma linha ao acaso, ser de um funcionário que trabalha na secretaria de educação?')
print((66126/237125) * 100)



print('5) Liste todas as funções contidas na base.')
print(df_servidores['FUNÇÃO'].value_counts())

print('6) Qual órgão publico possui a maior média salarial?')
# Calculando a média salarial para cada orgão público
media_salarial_por_orgao = df_servidores.groupby('ÓRGÃO')['BRUTO'].mean()

# Identificando e exibindo o orgão público com maior média salarial
orgao_maior_media_salarial = media_salarial_por_orgao.idxmax()
print("ÓRGÃO COM MAIOR MÉDIA SALARIAL:", orgao_maior_media_salarial)

# Encontrando o órgão público com a maior média salarial
orgao_maior_media_salarial = media_salarial_por_orgao.idxmax()

# Filtrando os dados brutos para o órgão com a maior média salarial
dados_orgao_maior_media = df_servidores[df_servidores['ÓRGÃO'] == orgao_maior_media_salarial]

# Selecionar alguns servidores aleatórios do órgão com a maior média salarial
amostra_servidores = dados_orgao_maior_media.sample(n=5, random_state=1)

# Calculando a média salarial "manualmente"
media_manual = amostra_servidores['BRUTO'].mean()

# Comparando com a média calculada pelo código
print("Média salarial calculada manualmente:", media_manual)
print("Média salarial calculada pelo código:", media_salarial_por_orgao[orgao_maior_media_salarial])


print('7) O servidor com maior remuneração básica pertence a qual órgão?')
servidor_maior_remuneracao_basica = df_servidores[df_servidores['REMUNERAÇÃO BÁSICA'] == df_servidores['REMUNERAÇÃO BÁSICA'].max()]
print(servidor_maior_remuneracao_basica['ÓRGÃO'].iloc[0])


print('8) Qual o valor pago para todos os funcionários públicos? Pontuação (1 Ponto)')
print(f'R$ {df_servidores['BRUTO'].sum()}')

print('9) Elabore um gráfico de pizza com a remuneração bruta dos servidores por orgão.')
remuneracao_por_orgao = df_servidores.groupby('ÓRGÃO')['BRUTO'].sum()
remuneracao_por_orgao_sorted = remuneracao_por_orgao.sort_values(ascending=False)


plt.figure(figsize=(10, 8))
patches, texts, autotexts = plt.pie(remuneracao_por_orgao_sorted, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 10})
plt.title('Distribuição da Remuneração Bruta dos Servidores por Órgão', fontsize=14)
plt.axis('equal')

# Adicionar os nomes dos órgãos diretamente no gráfico
plt.legend(remuneracao_por_orgao_sorted.index, loc='center left', fontsize='small', bbox_to_anchor=(1, 0.5))

plt.show()


print('10) Elabore um gráfico de boxplot com a situação do servidor e sua remuneração liquida')
df_servidores.columns = df_servidores.columns.str.strip()
data_boxplot = df_servidores.copy()
data_boxplot['SITUAÇÃO'] = data_boxplot['SITUAÇÃO'].str.title()
plt.figure(figsize=(18, 6))
sns.boxplot(data=data_boxplot, x='SITUAÇÃO', y='LÍQUIDO', palette='Set3')
plt.title('Distribuição da Remuneração Líquida por Situação do Servidor')
plt.xlabel('Situação do Servidor')
plt.ylabel('Remuneração Líquida')
plt.xticks(rotation=45)
plt.show()

print('11) Identifique qual órgão possui salário liquido com menos variações, utilizando para isto medidas de dispersão.')
variancia_por_orgao = df_servidores.groupby('ÓRGÃO')['LÍQUIDO'].var()
orgao_menos_variacao = variancia_por_orgao.idxmin()
print("Órgão com menor variação salarial líquida:", orgao_menos_variacao)


print('12) Calcule o índice de correlação entre o IRRF e os salários liquido e bruto. Em qual dos casos o índice de correlação foi maior?')
correlacao_irrf_salario_bruto = df_servidores['IRRF'].corr(df_servidores['BRUTO'])
correlacao_irrf_salario_liquido = df_servidores['IRRF'].corr(df_servidores['LÍQUIDO'])
print("Correlação entre IRRF e salário bruto:", correlacao_irrf_salario_bruto)
print("Correlação entre IRRF e salário líquido:", correlacao_irrf_salario_liquido)

if abs(correlacao_irrf_salario_bruto) > abs(correlacao_irrf_salario_liquido):
    print("A correlação entre IRRF e salário bruto é maior.")
else:
    print("A correlação entre IRRF e salário líquido é maior.")



print('13) Adicione uma nova coluna que irá conter a diferença entre o salario bruto e liquido, e responda as seguintes questões;\n * Qual a correlação entre o IRRF pago e esta nova coluna?\n * Qual órgão apresenta índice de correlação entre IRRF e diferença salarial maior?')
#Adicione uma nova coluna que irá conter a diferença entre o salario bruto e liquido, e responda as seguintes questões;

df_servidores['DIFERENÇA'] = df_servidores['BRUTO'] - df_servidores['LÍQUIDO']

# a) Calculando a correlação entre o IRRF e a diferença salarial
correlacao_irrf_diferenca = df_servidores['IRRF'].corr(df_servidores['DIFERENÇA'])
print("Correlação entre IRRF e diferença salarial:", correlacao_irrf_diferenca)

# b) Calculando a correlação entre IRRF e a diferença salarial por órgão
correlacao_irrf_diferenca_por_orgao = df_servidores.groupby('ÓRGÃO').apply(lambda x: x['IRRF'].corr(x['DIFERENÇA']))
orgao_maior_correlacao_irrf_diferenca = correlacao_irrf_diferenca_por_orgao.idxmax()
print("Órgão com maior correlação entre IRRF e diferença salarial:", orgao_maior_correlacao_irrf_diferenca)


