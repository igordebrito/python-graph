import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.ticker import MultipleLocator, FuncFormatter

# Dados dos testes
testes = {
    "Messages Sent (messages/second)": [15, 150, 300, 450, 600, 750, 900, 1050, 1200, 1350, 1500, 1650],
    "First Message Time": [
        "11:35:47.180799", "12:37:23.852294", "12:48:14.344670", "12:54:37.922445",
        "12:57:23.224343", "12:59:59.193488", "13:03:50.860505", "13:07:53.139898",
        "13:11:03.335719", "13:14:58.009054", "13:19:13.659415", "13:23:47.414190"
    ],
    "Last Message Time": [
        "11:36:47.043503", "12:38:23.762812", "12:49:14.340754", "12:55:38.078926",
        "12:58:23.220469", "13:00:59.245610", "13:04:53.330387", "13:09:08.120041",
        "13:12:29.287032", "13:16:40.062185", "13:21:12.055642", "13:25:41.316941"
    ]
}

# Criar o DataFrame
df = pd.DataFrame(testes)

# Converter os tempos para o formato datetime
df['First Message Time'] = pd.to_datetime(df['First Message Time'], format='%H:%M:%S.%f').dt.time
df['Last Message Time'] = pd.to_datetime(df['Last Message Time'], format='%H:%M:%S.%f').dt.time

# Função para calcular o tempo de duração entre duas mensagens
def calcular_duracao_in_seconds(tempo_primeira, tempo_ultima):
    t1 = datetime.combine(datetime.today(), tempo_primeira)
    t2 = datetime.combine(datetime.today(), tempo_ultima)
    return (t2 - t1).total_seconds()

# Calcular a duração e a vazão
df['Duration (seconds)'] = df.apply(lambda x: calcular_duracao_in_seconds(x['First Message Time'], x['Last Message Time']), axis=1)
df['Throughput (messages/second)'] = df.apply(lambda x: x['Messages Sent (messages/second)'] * 60 / x['Duration (seconds)'], axis=1)

# Exibir o DataFrame
print(df)

# Salvar a tabela em um arquivo CSV
df.to_csv(r'C:\Users\igors\OneDrive\Área de Trabalho\Graph\throughput_table.csv', index=False)

# Criar o gráfico
fig, ax = plt.subplots()

# Cor da bolinha e borda
cor_bolinha = '#a265c2'  # Cor interna da bolinha
cor_borda = 'black'      # Cor da borda da bolinha

# Plotar a vazão como bolinhas com cor interna #a265c2 e borda preta
ax.plot(df['Messages Sent (messages/second)'], df['Throughput (messages/second)'], 
        'o', 
        markerfacecolor=cor_bolinha, 
        markeredgecolor=cor_borda, 
        markeredgewidth=1.5)

# Configurar rótulos
ax.set_xlabel('Messages Sent (messages/second)')
ax.set_ylabel('Throughput (messages/second)')

# Remover título do gráfico
# ax.set_title('Throughput of Messages per Second by Messages Sent')  # Remover ou comentar o título

# Configurar os valores do eixo x
ax.set_xticks(df['Messages Sent (messages/second)'])
ax.set_xticklabels(df['Messages Sent (messages/second)'], rotation=45)

# Configurar fundo branco e linhas de grade pretas (somente horizontais)
ax.set_facecolor('white')
ax.yaxis.grid(True, which='both', color='black', linestyle='-', linewidth=0.5)  # Linha sólida horizontal
ax.xaxis.grid(False)  # Desativar linhas verticais

# Ajustar os ticks do eixo Y para mostrar de 50 em 50 e exibir apenas a cada duas linhas
def custom_ticks(x, pos):
    # Mostra o valor a cada duas linhas
    if x is not None and x % 50 == 0:
        return f'{int(x)}'
    return ''

# Configurar o intervalo dos ticks do eixo Y
ax.yaxis.set_major_locator(MultipleLocator(50))
ax.yaxis.set_major_formatter(FuncFormatter(custom_ticks))

# Ajustar limite do eixo Y para 1000
ax.set_ylim(0, 1000)

# Remover linha azul e manter apenas bolinhas
ax.get_lines()[0].set_linestyle('None')

# Melhorar o layout
plt.tight_layout()

# Salvar o gráfico em um arquivo PNG
plt.savefig(r'C:\Users\igors\OneDrive\Área de Trabalho\Graph\throughput_messages_per_second.png', bbox_inches='tight')

# Mostrar o gráfico
plt.show()
