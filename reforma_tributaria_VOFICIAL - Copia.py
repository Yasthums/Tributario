import pandas as pd
import os

#definir pastas na maquina
# Define file paths
auditto_file_path = 
protheus_file_path =
iss_file_path = 
regime_tributario_file_path =
class_produtos_file_path = 
output_file_path = 

# Check if files exist
for file_path in [auditto_file_path, protheus_file_path, regime_tributario_file_path, class_produtos_file_path, iss_file_path]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")


    # Load the spreadsheets
    with pd.ExcelFile(auditto_file_path) as auditto_xls, \
         pd.ExcelFile(protheus_file_path) as protheus_xls, \
         pd.ExcelFile(regime_tributario_file_path) as regime_tributario_xls, \
         pd.ExcelFile(class_produtos_file_path) as class_produtos_xls, \
         pd.ExcelFile(iss_file_path) as iss_xls:

        auditto_df = pd.read_excel(auditto_xls)
        protheus_df = pd.read_excel(protheus_xls)
        regime_tributario_df = pd.read_excel(regime_tributario_xls)
        class_produtos_df = pd.read_excel(class_produtos_xls)
        iss_df = pd.read_excel(iss_xls)  # Load the ISS data

    
        # Verificar se as colunas necessárias estão presentes
        required_auditto_columns = ['Referência', 'Nº/Série', 'CNPJ Emitente', 'Frete', 'Bc ICMS', 'Aliq ICMS', 'Valor ICMS', 'Bc IPI', 'Aliq. IPI', 'Valor IPI', 'Bc de PIS', 'Aliq. PIS', 'Valor PIS', 'Bc de COFINS', 'Aliq. COFINS', 'Valor COFINS']
        required_protheus_columns = ['Produto', 'Documento', 'Vlr.Total', 'Forn/Cliente']
        required_regime_tributario_columns = ['Forn/Cliente', 'Regime', 'PIS','COFINS']
        required_class_produtos_columns = ['Produto', 'Tipo']

        # Validar as colunas em cada dataframe
        missing_auditto_columns = [col for col in required_auditto_columns if col not in auditto_df.columns]
        missing_protheus_columns = [col for col in required_protheus_columns if col not in protheus_df.columns]
        missing_regime_tributario_columns = [col for col in required_regime_tributario_columns if col not in regime_tributario_df.columns]
        missing_class_produtos_columns = [col for col in required_class_produtos_columns if col not in class_produtos_df.columns]

        if missing_auditto_columns:
            raise ValueError(f"Auditto file missing required columns: {missing_auditto_columns}")
        if missing_protheus_columns:
            raise ValueError(f"Protheus file missing required columns: {missing_protheus_columns}")
        if missing_regime_tributario_columns:
            raise ValueError(f"Regime Tributario file missing required columns: {missing_regime_tributario_columns}")
        if missing_class_produtos_columns:
            raise ValueError(f"Classificação de Produtos file missing required columns: {missing_class_produtos_columns}")

        # Criar a chave de junção em ambos os dataframes
        auditto_df['Nº/Série'] = auditto_df['Nº/Série'].astype(str).str.split('/').str[0]
        protheus_df['Documento'] = protheus_df['Documento'].astype(str).apply(lambda x: x.split('-')[0])
        auditto_df['Referência'] = auditto_df['Referência'].fillna(0).astype(int)

        auditto_df['chave1'] = auditto_df['Referência'].astype(str) + '-' + auditto_df['Nº/Série'].astype(str)
        protheus_df['chave1'] = protheus_df['Produto'].astype(str) + '-' + protheus_df['Documento'].astype(str)

        # Selecionar colunas relevantes do auditto dataframe junto com a chave de junção
        auditto_relevant = auditto_df[['chave1', 'CNPJ Emitente', 'Frete', 'Bc ICMS', 'Aliq ICMS', 'Valor ICMS', 'Bc IPI', 'Aliq. IPI', 'Valor IPI', 'Bc de PIS', 'Aliq. PIS', 'Valor PIS', 'Bc de COFINS', 'Aliq. COFINS', 'Valor COFINS']]

        # Realizar o merge dos dataframes com base na chave de junção
        merged_df = pd.merge(protheus_df, auditto_relevant, on='chave1', how='left')
        merged_temp = pd.merge(merged_df, class_produtos_df[['Produto', 'Tipo']], on='Produto', how='left')
        merged_df = pd.merge(merged_temp, regime_tributario_df, on='Forn/Cliente', how='left')

        # Criação da coluna 'id' em merged_df
        if all(col in merged_df.columns for col in ['Filial', 'CNPJ', 'Produto']):
            merged_df['id'] = merged_df['Filial'].astype(str) + merged_df['CNPJ'].astype(str) + merged_df['Produto'].astype(str)
        else:
            raise KeyError("As colunas necessárias para criar 'id' não estão presentes em merged_df.")

        # Realizar o merge com ISS
        merged_df = pd.merge(merged_df, iss_df, on='id', how='left')

        merged_df = merged_df.fillna(0)
        print(merged_df.columns)

        merged_df = merged_df[~merged_df['Razao Social_x'].str.contains('CORPOREOS', case=False, na=False)]
    

        
        def definir_tipo(row):
            # Extrai o primeiro caractere de 'C Contabil', se disponível
            primeiro_caractere = str(row['C Contabil'])[0] if pd.notna(row['C Contabil']) else ''
            
            # Verifica com base no primeiro caractere de 'C Contabil'
            if primeiro_caractere == '5' or primeiro_caractere == '4'  :
                if row['Valor Imp. 5'] != 0 or row['Valor Imp. 6'] != 0:
                    return 'Custos com créditos'
                else:
                    return 'Custos sem créditos'
            
            elif primeiro_caractere == '1':
                if row['Valor Imp. 5'] != 0 or row['Valor Imp. 6'] != 0:
                    return 'Ativo com créditos'
                else:
                    return 'Ativo sem créditos'
            
            elif primeiro_caractere == '6':
                if row['Valor Imp. 5'] != 0 or row['Valor Imp. 6'] != 0:
                    return 'Despesas com créditos'
                else:
                    return 'Despesas sem créditos'
            
            # Verifica se a descrição contém palavras-chave específicas e retorna 'Despesas com créditos'
            if row['Descricao'] in ['PAGAMENTO VALE TRANSPORTE', 'PAGAMENTO VALE REFEICAO', 'PAGAMENTO VALE ALIMENTACAO', 'SERVICO COBERTURA PLANO SAUDE']:
                return 'Despesas com créditos'
            
            # Se 'C Contabil' for 0, concatenar com base no valor de 'Valor Imp. 5' ou 'Valor Imp. 6'
            # Se 'C Contabil' for 0, concatenar com base no valor de 'Valor Imp. 5' ou 'Valor Imp. 6'
            if row['C Contabil'] == 0:
                tipo = str(row['Tipo']) if pd.notna(row['Tipo']) else 'Desconhecido'
                
                if row['Valor Imp. 5'] != 0 or row['Valor Imp. 6'] != 0:
                    return tipo + ' com créditos'
                else:
                    return tipo + ' sem créditos'
            


        # Aplicar a função ao DataFrame
        merged_df['Tipo'] = merged_df.apply(definir_tipo, axis=1)

        # Cálculos ICMS, IPI, ISS, PIS, COFINS, e outros
        merged_df['ICMS Calculated'] = merged_df['Bc ICMS'] * (merged_df['Aliq ICMS'] / 100)
        merged_df['IPI Calculated'] = merged_df['Bc IPI'] * (merged_df['Aliq. IPI'] / 100)
        merged_df['ISS Calculated'] = merged_df['Vlr.Total'] * (merged_df['iss'] / 100)
        def definir_aliquotas(row):
            # Nova regra: Se 'Aliq. PIS' ou 'Aliq. COFINS' forem zero, mantêm-se os valores atuais ou aplicam regra de negócio, se necessário
            if row['Aliq. PIS'] == 0:
                row['Aliq. PIS'] = row['PIS']  # Ou outra lógica apropriada se 'pis' já estiver em merged_df

            if row['Aliq. COFINS'] == 0:
                row['Aliq. COFINS'] = row['COFINS']  # Ou outra lógica apropriada se 'cofins' já estiver em merged_df

            return row

        # Função para calcular PIS
        def calculate_pis(row):
            if (row['Valor PIS']) != 0 :
                return (row['Bc de PIS']) * (row['Aliq. PIS'] / 100)
            else:
                return row['Vlr.Total'] * (row['Aliq. PIS'] / 100)

        # Função para calcular COFINS
        def calculate_cofins(row):
            if (row['Valor COFINS'])!=0 :
                return (row['Bc de COFINS'])* (row['Aliq. COFINS'] / 100)
            else:
                return row['Vlr.Total'] * (row['Aliq. COFINS'] / 100)

        # Aplicando a regra de definir alíquotas
        merged_df = merged_df.apply(definir_aliquotas, axis=1)

        # Calculando PIS e COFINS com as novas alíquotas
        merged_df['PIS Calculated'] = merged_df.apply(calculate_pis, axis=1)
        merged_df['COFINS Calculated'] = merged_df.apply(calculate_cofins, axis=1)
        merged_df['CTA'] = merged_df['COFINS Calculated'] + merged_df['ICMS Calculated'] + merged_df['IPI Calculated'] + merged_df['PIS Calculated']+ merged_df['ISS Calculated']
        merged_df['lucro_liquido'] = merged_df['Vlr.Total'] - merged_df['CTA']

         # Ajustar valores se PIS ou IPI forem diferentes do esperado
        def ajustar_valores(row):
            if row['PIS Calculated'] != row['Valor PIS']:
                 row['Valor PIS'] = row['PIS Calculated'] 
            if row['COFINS Calculated'] != row['Valor COFINS']:
                 row['Valor COFINS'] = row['COFINS Calculated'] 
            if row['IPI Calculated'] != row['Valor IPI']:
                row['Valor IPI']=  row['IPI Calculated'] 
            if row['ICMS Calculated'] != row['Valor ICMS']:
                row['Valor ICMS']=  row['ICMS Calculated']     
            return row

        # Aplicar a função de ajuste de valores
        merged_df = merged_df.apply(ajustar_valores, axis=1)

        def calculate_ctn(row):
            if row['Descricao'] in ['SERVICO ALUGUEL PJ', 'SERVICO ALUGUEL PF', 'PAGAMENTO ALUGUEL COMPLEMENTAR']:
                return row['lucro_liquido'] * 0.106
            
            # Verifica o regime tributário e calcula o valor de acordo com as regras definidas
            if row['Regime'] in ['Lucro Real', 'Regime Especial', 'Lucro Presumido']:
                return float(row['lucro_liquido']) * 0.265
                        
            return row['CTA']

        merged_df['ctn'] = merged_df.apply(calculate_ctn, axis=1)
        merged_df['Novo valor de caixa'] = merged_df['lucro_liquido'] + merged_df['ctn']
        merged_df['Variação % Valor Caixa'] = 1 - merged_df['Novo valor de caixa'] / merged_df['Vlr.Total']

        merged_df['Credito Atual'] = merged_df['Valor Imp. 5'] + merged_df['Valor Imp. 6']

        def calculate_novo_credito(row):
            # Check if 'Tipo' is exactly 'Despesas sem créditos'
            if row['Tipo'] == 'Despesas sem créditos':
                    return 0.0
            else:
                # If 'Tipo' is not 'Despesas sem créditos', return 'ctn' value
                return row['ctn']

        # Apply the function to create 'novo_credito' column
        merged_df['novo_credito'] = merged_df.apply(calculate_novo_credito, axis=1)

        # Calculate 'valor resultado atual' and 'Novo valor resultado'
        merged_df['valor resultado atual'] = merged_df['Vlr.Total'] - merged_df['Credito Atual']
        merged_df['Novo valor resultado'] = merged_df['Novo valor de caixa'] - merged_df['novo_credito']
        merged_df['Variação % Valor Resultado'] = 1 - (merged_df['Novo valor resultado'] / merged_df['valor resultado atual'])

        merged_df = merged_df.drop_duplicates()


      # Exportar para Excel
    merged_df.to_excel(output_file_path, index=False)
    print(f"Arquivo exportado para: {output_file_path}")

