Simulador de Impactos da Reforma Tributária
Este projeto realiza simulações e análises de impacto da Reforma Tributária com foco em tomada de crédito e impostos sobre vendas. O objetivo é proporcionar uma visão clara sobre como as mudanças tributárias afetam os resultados financeiros de empresas, com base em cenários reais.

📝 Descrição do Projeto
O simulador permite a análise de dados financeiros, considerando:

Tomada de Crédito: Avaliação de créditos disponíveis para abatimento de tributos.
Impostos sobre Vendas: Análise de mudanças no PIS, COFINS, ICMS e outros impostos relevantes.
Comparação de Cenários: Análise do antes e depois da reforma tributária.
Os resultados são apresentados em formato tabular e gráfico, facilitando a compreensão do impacto em diversas linhas da Demonstração de Resultados do Exercício (DRE).

💡 Funcionalidades
Entrada de Dados:

Importação de dados financeiros (Excel ou CSV).
Parâmetros configuráveis para diferentes cenários da reforma.
Análise Tributária:

Simulação de impacto por linhas específicas da DRE.
Comparação entre diferentes setores (exemplo: Suzano S.A para indústria e Fleury S.A para serviços).
Resultados Visuais:

Tabelas detalhadas por setor e empresa.
Gráficos com comparativos antes e depois da reforma.
Exportação:

Resultados salvos em Excel, com opções para download automático.
📊 Estrutura do Projeto
1. Entrada
Os dados de entrada devem conter:

Receita bruta, tributos incidentes, créditos tributários.
Custos e despesas operacionais.
2. Saída
Análise detalhada do impacto em linhas específicas da DRE.
Comparação gráfica e tabular dos cenários tributários.
🛠️ Tecnologias Utilizadas
Python: Para processamento e análise.
Pandas: Manipulação de dados tabulares.
Flask: Backend para disponibilizar o simulador como aplicação web.
Power BI: Relatórios interativos para apresentação dos dados.
Matplotlib/Plotly: Gráficos comparativos.
🚀 Como Executar
Pré-requisitos:

Python 3.9 ou superior.
Instale as dependências listadas no arquivo requirements.txt:
bash
Copiar código
pip install -r requirements.txt
Executar o Simulador:

Inicie o servidor Flask:
bash
Copiar código
python app.py
Acesse a aplicação no navegador:
arduino
Copiar código
http://127.0.0.1:5000
Importar Dados:

Faça o upload de um arquivo Excel ou CSV com os dados financeiros.
Visualizar Resultados:

Acompanhe a análise diretamente no sistema ou baixe os relatórios.
📂 Estrutura de Pastas
bash
Copiar código
reforma-tributaria/
│
├── data/               # Exemplos de dados de entrada
├── templates/          # Arquivos HTML para o frontend
├── static/             # Arquivos estáticos (CSS, JS, imagens)
├── app.py              # Arquivo principal do Flask
├── analysis.py         # Funções de análise tributária
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação do projeto
