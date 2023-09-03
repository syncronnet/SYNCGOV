import requests
import pandas as pd
import locale
# Configurar o locale para o formato brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def obter_dados_ibge(ano):
    url = f'https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/{ano}/variaveis/9324?localidades=N1[all]'

    response = requests.get(url)
    data = response.json()

    resultado = data[0]['resultados']
    table_data = []

    for result in resultado:
        for series in result['series']:
            localidade = series['localidade']['nome']
            for ano, valor in series['serie'].items():
                table_data.append((localidade, ano, valor))
    
    df = pd.DataFrame(table_data, columns=['localidade', 'ano', 'valor'])
    return df

def calcular_populacao_total(df):
    populacao_total = df['valor'].astype(int).sum()
    populacao_em_milhar = f'{populacao_total:,}'.replace(',', '.')
    return populacao_em_milhar

def calcular_diferenca(df_2020, df_2021):
    populacao_2020 = df_2020[df_2020['ano'] == '2020']['valor'].astype(int).sum()
    populacao_2021 = df_2021[df_2021['ano'] == '2021']['valor'].astype(int).sum()
    diferenca = populacao_2021 - populacao_2020
    diferenca_formatada = locale.format_string('%d', diferenca, grouping=True)
    return f'{diferenca_formatada} habitantes'


'''
# Exemplo de uso para testar o código
if __name__ == "__main__":
    dados_ibge_2020 = obter_dados_ibge('2020')
    populacao_2020 = calcular_populacao_total(dados_ibge_2020)
    print(f'No Brasil no ano de 2020 a população total era de {populacao_2020} habitantes.')

    dados_ibge_2021 = obter_dados_ibge('2021')
    populacao_2021 = calcular_populacao_total(dados_ibge_2021)
    print(f'No Brasil no ano de 2021 a população total era de {populacao_2021} habitantes.')
'''