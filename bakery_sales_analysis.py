import pandas as pd
import matplotlib.pyplot as plt

file_path = 'bakery-sales-dataset.csv'

days_order = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]

day_translation = {
    'Monday': 'Segunda-feira',
    'Tuesday': 'Terça-feira',
    'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira',
    'Friday': 'Sexta-feira',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

def main():
    # Configurações de plot
    plt.rcParams.update({'font.size': 24})

    # Carregar e manipular dados
    data = pd.read_csv(file_path)
    data['datetime'] = pd.to_datetime(data['datetime'])
    data['total_price'] = data['unit_price'] * data['quantity']
    data['day_of_week'] = data['datetime'].dt.day_name()
    data['hour'] = data['datetime'].dt.hour

    # Análise exploratória
    describe_data(data)

    # Gráfico de produtos mais rentáveis
    top_products_by_revenue_graph(data)

    # Gráficos de vendas no período
    sales_over_time_graphs(data)

    # Gráficos do datetime
    day_and_hour_frequency_graphs(data)

    # Gráficos de quantidade e preço total por transação
    transaction_distribution_graphs(data)

    # Gráficos de distribuição de preço unitário
    unit_price_distribution_graph(data)

def describe_data(data):
    print("\n\n********** TABELA DE INTEIROS/FLOATS/DATA **********")
    print(data.describe(include=['float', 'int', 'datetime64[ns]']).transpose())

    print("\n\n********** TABELA DE STRINGS **********")
    print(data.describe(include=['object']).transpose())

def top_products_by_revenue_graph(data):
    # Quantidade de produtos a serem plotados
    n = 10

    # Agrupar por artigo e somar as receitas
    revenue_per_article = data.groupby('article')['total_price'].sum()

    # Ordenar os artigos pela receita e pegar os top n
    top_articles_by_revenue = revenue_per_article.sort_values(ascending=False).head(n)

    # Plotar
    top_articles_by_revenue.plot(kind='bar', color='mediumseagreen', figsize=(20,9))
    plt.title(f'Os {n} Produtos Mais Rentáveis')
    plt.xlabel('Tipo do Produto')
    plt.ylabel('Receita Total (€)')
    plt.xticks(rotation=45)
    plt.show()

def sales_over_time_graphs(data):
    # Gráfico de quantidade vendida ao longo do tempo
    sales_over_time = data.set_index('datetime').resample('D')['quantity'].sum()
    plt.subplot(1, 2, 1)
    sales_over_time.plot(kind='line', color='cornflowerblue', figsize=(20,9))
    plt.title('Quantidade Vendida no Período')
    plt.xlabel('')
    plt.ylabel('Quantidade Vendida')
    plt.grid(True)

    # Gráfico de receita ao longo do tempo
    revenue_over_time = data.set_index('datetime').resample('D')['total_price'].sum()
    plt.subplot(1, 2, 2)
    revenue_over_time.plot(kind='line', color='mediumseagreen', figsize=(20,9))
    plt.title('Receita no Período')
    plt.xlabel('')
    plt.ylabel('Receita (€)')
    plt.grid(True)

    # Plotar
    plt.tight_layout()
    plt.show()

def day_and_hour_frequency_graphs(data):
    plt.figure(figsize=(20,9))

    # Frequência de vendas por hora do dia
    plt.subplot(1, 2, 1)
    plt.hist(data['hour'], bins=12, color='mediumseagreen', edgecolor='black')
    plt.title('Vendas por Hora do Dia')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Vendas')
    plt.xticks(range(7, 20))

    # Frequência de vendas por dia da semana
    frequency_by_day_of_week = data['day_of_week'].value_counts().reindex(days_order)
    translated_labels = [day_translation[day] for day in frequency_by_day_of_week.index]

    plt.subplot(1, 2, 2)
    plt.bar(translated_labels, frequency_by_day_of_week, color='cornflowerblue', edgecolor='black')
    plt.title('Vendas por Dia da Semana')
    plt.xlabel('Dia da Semana')
    plt.ylabel('Vendas')
    plt.xticks(rotation=45, ticks=range(len(translated_labels)), labels=translated_labels)

    # Plotar
    plt.tight_layout()
    plt.show()

def transaction_distribution_graphs(data):
    plt.figure(figsize=(20,9))

    # Distribuição de quantidade vendida por transação
    plt.subplot(1, 2, 1)
    plt.hist(data['quantity'], bins=20, color='cornflowerblue', edgecolor='black')
    plt.title('Distribuição de Quantidade Vendida por Transação')
    plt.xlabel('Quantidade Vendida')
    plt.ylabel('Frequência')

    # Distruição de total por transação
    plt.subplot(1, 2, 2)
    plt.hist(data['total_price'], bins=20, color='mediumseagreen', edgecolor='black')
    plt.title('Distribuição de Total por Transação')
    plt.xlabel('Total (€)')
    plt.ylabel('Frequência')

    # Plotar
    plt.tight_layout()
    plt.show()

def unit_price_distribution_graph(data):
    plt.figure(figsize=(20,9))
    plt.hist(data['unit_price'], bins=20, color='mediumseagreen', edgecolor='black')
    plt.title('Distribuição de Preço Unitário')
    plt.xlabel('Preço Unitário (€)')
    plt.ylabel('Frequência')
    plt.show()

if __name__ == '__main__':
    main()
