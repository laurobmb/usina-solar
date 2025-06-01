import matplotlib.pyplot as plt
import pandas as pd
import os

def geragrafico(MEU_ARQUIVO):
    file_path = 'csv/' + MEU_ARQUIVO
    data = pd.read_csv(file_path, delimiter=',')

    if 'CÓDIGO_DO_CLIENTE' not in data.columns:
        print("Coluna 'CÓDIGO_DO_CLIENTE' não encontrada.")
        return

    # Cria a pasta 'photos' se não existir
    os.makedirs('photos', exist_ok=True)

    # Agrupa por CÓDIGO_DO_CLIENTE
    for codigo_cliente, df_cliente in data.groupby('CÓDIGO_DO_CLIENTE'):
        print(f'Gerando gráfico para o cliente: {codigo_cliente}')

        plt.figure(figsize=(10, 6))

        for coluna, label in [
            ('ENERGIA_CONSUMIDA', 'Energia Consumida'),
            ('ENERGIA_INJETADA', 'Energia Injetada'),
            ('ENERGIA_FATURADA', 'Energia Faturada'),
            ('KWh_Compensado', 'kWh Compensado'),
        ]:
            if coluna in df_cliente.columns:
                plt.plot(
                    df_cliente['SITUAÇÃO_MENSAL'], 
                    df_cliente[coluna], 
                    marker='o', 
                    label=label
                )

                for i, valor in enumerate(df_cliente[coluna]):
                    plt.text(
                        i, valor, f'{valor}', 
                        fontsize=9, ha='center', va='bottom'
                    )

        plt.title(f'Energia por Mês - Cliente {codigo_cliente}', fontsize=16)
        plt.xlabel('Mês', fontsize=12)
        plt.ylabel('Energia (kWh)', fontsize=12)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)

        output_filename = MEU_ARQUIVO.replace('.csv', f'_{codigo_cliente}.png')
        output_path = os.path.join('photos', output_filename)

        plt.tight_layout()
        plt.savefig(output_path, format='png', dpi=300)
        plt.close()

        print(f'Gráfico salvo em: {output_path}')

if __name__ == '__main__':
    input_folder = 'csv'
    for file in os.listdir(input_folder):
        if file.endswith('.csv'):
            file_path = file
            print(f'Processando: {file_path}')
            geragrafico(file_path)
