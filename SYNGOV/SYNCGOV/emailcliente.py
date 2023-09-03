from populacao import obter_dados_ibge, calcular_populacao_total

dados_ibge_2020 = obter_dados_ibge('2020')
populacao_2020 = calcular_populacao_total(dados_ibge_2020)

dados_ibge_2021 = obter_dados_ibge('2021')
populacao_2021 = calcular_populacao_total(dados_ibge_2021)

diferenca = int(populacao_2021.replace('.', '')) - int(populacao_2020.replace('.', ''))

mensagem = (
    f'No Brasil, no ano de 2021, a população estimada era de {populacao_2021} habitantes.\n'
    f'No Brasil, no ano de 2020, a população estimada era de {populacao_2020} habitantes.\n'
    f'A diferença entre os anos de 2020 e 2021 é de {diferenca:,} habitantes.'
)

print(mensagem)
