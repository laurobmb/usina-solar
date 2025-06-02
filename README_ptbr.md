Claro, aqui está o `README.md` traduzido para o português, mantendo a formatação e as informações originais:

-----

# ⚡🌞🌞 Painel de Controle Solar de Geração de Energia Distribuída 🌞🌞⚡

Este projeto é um dashboard web interativo construído com **Flask** (Python) que permite visualizar e analisar dados de consumo, injeção e economia de energia para clientes de sistemas de geração de energia solar distribuída. Ele utiliza dados de arquivos CSV para gerar gráficos dinâmicos e tabelas de custos e economias.

## Visão Geral do Projeto

O objetivo principal deste dashboard é fornecer uma ferramenta intuitiva para que os usuários possam:

1.  **Selecionar um ano** para a análise.
2.  **Selecionar um cliente específico** dentro do ano escolhido.
3.  **Visualizar gráficos** de energia consumida, energia injetada e kWh compensados ao longo dos meses.
4.  **Analisar tabelas** comparativas de custos de energia com e sem geração distribuída, além da economia gerada.
5.  **Ver o total de economia acumulado** para o ano selecionado.

## Como Funciona

O projeto se compõe de três partes principais:

1.  **Backend (Python - Flask):**

      * Gerencia as rotas da aplicação web.
      * Lê os dados de arquivos CSV (localizados no diretório `csv/`). Cada arquivo CSV representa um ano e contém dados de múltiplos clientes.
      * Funções para `listar_anos()` e `listar_clientes()` disponíveis nos arquivos CSV.
      * **`gerar_grafico()`:** Utiliza a biblioteca `Plotly` para criar gráficos interativos de linhas que mostram o desempenho energético do cliente ao longo do tempo (Energia Consumida, Energia Injetada e kWh Compensados). Os gráficos são gerados em HTML para serem incorporados na página web e também podem ser salvos como imagens PNG.
      * **`gerar_tabela()`:** Processa os dados do cliente para calcular:
          * `CUSTO_SEM_GERACAO_DISTRIBUIDA`: Energia Consumida \* Valor do kWh (fixado em R$ 0.90).
          * `CUSTO_COM_GERACAO_DISTRIBUIDA`: Energia Faturada \* Valor do kWh.
          * `ECONOMIA`: A diferença entre os dois custos, mostrando o benefício da geração distribuída.
          * Calcula o `total_economia` acumulado para o ano do cliente selecionado.

2.  **Frontend (HTML/CSS com Bootstrap):**

      * Página única (`index.html`) que funciona como o dashboard.
      * Permite a seleção de ano e cliente através de campos `select` dinâmicos.
      * Mostra o gráfico gerado pelo backend.
      * Mostra a tabela de custos e economia, incluindo a soma total da economia anual.
      * O design é responsivo, utilizando a estrutura do Bootstrap.

3.  **Dados (CSV):**

      * Os dados de energia de cada cliente estão armazenados em arquivos CSV, nomeados por ano (ex: `2021.csv`, `2022.csv`, etc.).
      * O formato do CSV inclui colunas como `SITUACAO_MENSUAL` (mês/ano), `CODIGO_DO_CLIENTE`, `ENERGIA_CONSUMIDA`, `ENERGIA_INJETADA`, `ENERGIA_FATURADA`, `kWh_Compensado` e `CREDITO`.

## Estrutura de Pastas

├── app.py              \# Aplicação principal do Flask  
├── templates/  
│   └── index.html      \# Template HTML do dashboard  
├── static/  
│   └── style.css       \# (Assumido) Arquivo CSS para estilos personalizados  
├── csv/  
│   └── 2021.csv        \# Exemplo de arquivo de dados anuais  
│   └── 2022.csv  
│   └── ...  
└── photos/             \# Diretório para salvar as imagens dos gráficos (opcional)

## Como Executar o Projeto (Usando Podman)

1.  **Construir a imagem Docker/Podman:**
    ```bash
    podman build -t usina_solar:v1 .
    ```
2.  **Executar o contêiner:**
    ```bash
    podman run -it --rm --name usina \
        -p 5000:5000 \
        -v ${PWD}/csv:/app/csv:Z \
        -v ${PWD}/photos:/app/photos:Z \
        -e VALOR_KWH=0.87 \
        usina_solar:v1
    ```
      * `-it`: Modo interativo e TTY.
      * `--rm`: Remove o contêiner após sair.
      * `--name usina`: Define um nome para o contêiner.
      * `-p 5000:5000`: Mapeia a porta 5000 do contêiner para a porta 5000 da sua máquina.
      * `-v ${PWD}/csv:/app/csv:Z`: Monta o diretório `csv` local dentro do contêiner, permitindo que a aplicação acesse seus dados. O `:Z` é específico para SELinux, ajustando as etiquetas de segurança.

Uma vez executado, acesse `http://localhost:5000` no seu navegador para interagir com o dashboard.

## Dependências

As principais bibliotecas Python utilizadas são:

  * `Flask`: Para o desenvolvimento web.
  * `pandas`: Para manipulação e análise de dados CSV.
  * `plotly`: Para geração de gráficos interativos.
  * `os`: Para operações de sistema de arquivos.