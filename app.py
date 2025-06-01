from flask import Flask, render_template, request
import pandas as pd
import os
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

CSV_DIR = 'csv'
OUTPUT_DIR = 'photos'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def listar_anos():
    arquivos = os.listdir(CSV_DIR)
    anos = sorted({arq.replace('.csv', '') for arq in arquivos if arq.endswith('.csv')})
    return anos


def listar_clientes(ano):
    caminho = os.path.join(CSV_DIR, f'{ano}.csv')
    if not os.path.exists(caminho):
        return []
    df = pd.read_csv(caminho, encoding='utf-8')
    # Converter para string para evitar problemas de comparação
    clientes = df['CÓDIGO_DO_CLIENTE'].astype(str).unique().tolist()
    return clientes


def gerar_grafico(ano, cliente):
    caminho = os.path.join(CSV_DIR, f'{ano}.csv')
    df = pd.read_csv(caminho, encoding='utf-8')

    df['CÓDIGO_DO_CLIENTE'] = df['CÓDIGO_DO_CLIENTE'].astype(str)
    df_cliente = df[df['CÓDIGO_DO_CLIENTE'] == cliente]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_cliente['SITUAÇÃO_MENSAL'],
        y=df_cliente['ENERGIA_CONSUMIDA'],
        mode='lines+markers+text',
        name='Energia Consumida (kWh)',
        text=df_cliente['ENERGIA_CONSUMIDA'].astype(str),
        textposition='top center'
    ))

    fig.add_trace(go.Scatter(
        x=df_cliente['SITUAÇÃO_MENSAL'],
        y=df_cliente['ENERGIA_INJETADA'],
        mode='lines+markers+text',
        name='Energia Injetada (kWh)',
        text=df_cliente['ENERGIA_INJETADA'].astype(str),
        textposition='top center'
    ))

    fig.add_trace(go.Scatter(
        x=df_cliente['SITUAÇÃO_MENSAL'],
        y=df_cliente['KWh_Compensado'],
        mode='lines+markers+text',
        name='KWh Compensado',
        text=df_cliente['KWh_Compensado'].astype(str),
        textposition='top center'
    ))

    fig.update_layout(
        title=f'Energia - Cliente {cliente} - {ano}',
        xaxis_title='Mês',
        yaxis_title='kWh',
        template='plotly_dark',            # template moderno e escuro
        font=dict(family="Arial, sans-serif", size=14, color="white"),
        legend=dict(font=dict(size=12)),
        hovermode='x unified'              # tooltip unificado ao passar mouse
    )

    # Salvar gráfico como PNG no diretório OUTPUT_DIR (opcional)
    output_path = os.path.join(OUTPUT_DIR, f'{ano}_{cliente}.png')
    pio.write_image(fig, output_path, format='png', scale=2, width=1000, height=600)

    grafico_html = pio.to_html(fig, full_html=False)
    return grafico_html

def gerar_tabela(ano, cliente):
    caminho = os.path.join(CSV_DIR, f'{ano}.csv')
    if not os.path.exists(caminho):
        return [], 0.0

    df = pd.read_csv(caminho)
    df.columns = df.columns.str.strip()
    df['CÓDIGO_DO_CLIENTE'] = df['CÓDIGO_DO_CLIENTE'].astype(str)

    if 'SITUAÇÃO_MENSAL' not in df.columns:
        return [], 0.0

    df_cliente = df[df['CÓDIGO_DO_CLIENTE'] == str(cliente)]

    if df_cliente.empty:
        return [], 0.0

    valor_kwh = 0.90

    for coluna in ['ENERGIA_CONSUMIDA', 'ENERGIA_FATURADA']:
        if coluna not in df_cliente.columns:
            return [], 0.0

    df_cliente['CUSTO_SEM_GERACAO_DISTRIBUIDA'] = df_cliente['ENERGIA_CONSUMIDA'] * valor_kwh
    df_cliente['CUSTO_COM_GERACAO_DISTRIBUIDA'] = df_cliente['ENERGIA_FATURADA'] * valor_kwh
    df_cliente['ECONOMIA'] = df_cliente['CUSTO_SEM_GERACAO_DISTRIBUIDA'] - df_cliente['CUSTO_COM_GERACAO_DISTRIBUIDA']

    tabela = df_cliente[['SITUAÇÃO_MENSAL', 'CUSTO_SEM_GERACAO_DISTRIBUIDA', 'CUSTO_COM_GERACAO_DISTRIBUIDA', 'ECONOMIA']].round(2)
    tabela = tabela.sort_values(by='SITUAÇÃO_MENSAL')

    total_economia = tabela['ECONOMIA'].sum().round(2)

    print("Tabela: ", tabela)
    print("Total Economia do Ano: R$", total_economia)

    return tabela.to_dict(orient='records'), total_economia


@app.route('/', methods=['GET', 'POST'])
def index():
    anos = listar_anos()
    clientes = []
    grafico = None
    tabela = None
    ano_selecionado = None
    cliente_selecionado = None
    total_economia = 0
    
    if request.method == 'POST':
        ano_selecionado = request.form.get('ano')
        cliente_selecionado = request.form.get('cliente')

        if ano_selecionado:
            clientes = listar_clientes(ano_selecionado)

        if ano_selecionado and cliente_selecionado:
            grafico = gerar_grafico(ano_selecionado, cliente_selecionado)
            tabela, total_economia = gerar_tabela(ano_selecionado, cliente_selecionado)
            print(total_economia)
        else:
            total_economia = 0

    return render_template('index.html',
                           anos=anos,
                           clientes=clientes,
                           grafico=grafico,
                           tabela=tabela,
                           total_economia=total_economia,
                           ano_selecionado=ano_selecionado,
                           cliente_selecionado=cliente_selecionado)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0" )
