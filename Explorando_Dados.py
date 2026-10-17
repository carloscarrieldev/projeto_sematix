# Importando biblioteca para o Python
import pandas as pd

# Visualizando resultado
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Lendo arquivo
# Tive que muda o formato de leitura como também explicar que cada coluna tem ';'
df = pd.read_csv('sinistros_08-2026.csv', encoding='latin1', sep=';')

# Mostrando apenas 10 linhas do arquivo
print('Dados do arquivo:\n')
print(df.head(10))

# Verificando os tipos de dados entre as colunas
print('Tipos de Dados:\n')
print(df.dtypes.to_string())

# Mostrando nomes de todas as colunas para verificação
print('Nomes de colunas:\n')
print(df.columns)

# Criando uma copía para limpeza dos dados
df_limpo = df.copy()

# Verificando valores ausentes
print('Valores ausentes entre as colunas:\n')
print(df_limpo.isnull().sum().to_string())

# Verificando registros duplicados
print('Valores duplicados entre as colunas:\n')
print(df_limpo.duplicated().sum())

# Convertendo a coluna de texto para data
print('Após alteração da coluna:')
df_limpo['data_sinistro'] = pd.to_datetime(
    df_limpo['data_sinistro'], format='%d/%m/%Y', errors='coerce')
print(df_limpo['data_sinistro'].dtypes)

# Procurando colunas sem utilidade
colunas_vazia = df_limpo.columns[df_limpo.isna().all()]
print('Colunas vazias:', len(colunas_vazia))
print(colunas_vazia.tolist())

# Removendo colunas após visualização
df_limpo = df_limpo.drop(columns=['tp_sinistro_colisao_traseira'])
print("Quantidade de colunas restantes:", len(df_limpo.columns))

# Exibindo sinistros que acontecem bastante
print('Sinistros mais vistos:\n ')
print(df_limpo['tp_sinistro_primario'].value_counts().head(15))

# Visualizando sinistros nos dias da semana
print('Dias da semana:\n')
print(df_limpo['dia_da_semana'].value_counts())

# Visualização de sinistros por regiões
print('Regiões:\n')
print(df_limpo['regiao_administrativa'].value_counts().head(10))

# Visualizando por Munícipio
print('Municipios:\n')
print(df_limpo['municipio'].value_counts().head(10))

# Alterando colunas de texto para números é trocando ',' por '.'
for coluna in ['latitude', 'longitude']:
    df_limpo[coluna] = pd.to_numeric(
        df_limpo[coluna].str.replace(',', '.', regex=False),
        errors='coerce'
    )
# Alterando colunas de acidentes para números
for coluna in [
    'qtd_gravidade_fatal',
    'qtd_gravidade_grave',
    'qtd_gravidade_leve',
    'qtd_gravidade_ileso'
]:
    df_limpo[coluna] = pd.to_numeric(
        df_limpo[coluna], errors='coerce'
    )
# Criando uma coluna de apenas veiculos para visualização
veiculos = {
    'qtd_pedestre': 'Pedestres',
    'qtd_bicicleta': 'Bicicletas',
    'qtd_motocicleta': 'Motocicletas',
    'qtd_automovel': 'Automóveis',
    'qtd_onibus': 'Ônibus',
    'qtd_caminhao': 'Caminhões',
    'qtd_veic_outros': 'Outros veículos',
    'qtd_veic_nao_disponivel': 'Não disponível'
}

df_veiculos = df_limpo.melt(
    id_vars=['id_sinistro', 'regiao_administrativa'],
    value_vars=veiculos.keys(),
    var_name='Veículos',
    value_name='Quantidade'
)
df_veiculos['Veículos'] = \
    df_veiculos['Veículos'].map(veiculos)
df_veiculos['Quantidade'] = \
    pd.to_numeric(df_veiculos['Quantidade'], errors='coerce')

# Visualizando estrutura das colunas após alteração
print('Após alteração das colunas:')
print(df_limpo[['latitude', 'longitude']].dtypes)
print(df_limpo[['qtd_gravidade_fatal','qtd_gravidade_grave','qtd_gravidade_leve','qtd_gravidade_ileso']].dtypes)

# Analisando o percentual por tipo
analise_percentual = df_limpo['tp_sinistro_primario']\
                      .value_counts().to_frame()
# Calculando o percentual de cada tipo é deixando com duas casas decimais
analise_percentual['Percentual'] = df_limpo['tp_sinistro_primario']\
                    .value_counts(normalize=True).mul(100).round(2)
# Exibindo os resultados da análise
print('\nQuantidade e percentual por tipo:\n')
print(analise_percentual)

# Salvando arquivo
# Sem criar colunas extras
# Sem deixar colunas com caracteres extras
df_limpo.to_csv(
    'sinistros_tratados.csv',
    index=False,
    encoding='utf-8-sig'
)

# Salvando arquivo veiculos por região após limpeza.
df_veiculos.to_csv(
    'veiculos.csv',
    index=False,
    encoding='utf-8-sig'
)