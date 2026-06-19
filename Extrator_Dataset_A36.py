# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
import visualization
import csv
import os
import re

csv_name = 'Dataset_DoE1000_Final_Extraido.csv'

with open(csv_name, mode='w') as f:
    writer = csv.writer(f, delimiter=',', lineterminator='\n')
    
    # CABEÇALHO ATUALIZADO (Mantendo a nomenclatura padrão da indústria: Z)
    writer.writerow([
        'Arquivo_Origem', 
        'Massa_TNT_kg', 
        'Espessura_mm', 
        'Distancia_Z_mm', 
        'Max_Desloc_U_m', 
        'Max_PEEQ', 
        'Max_Tensao_VonMises_Pa', 
        'Status_Ruptura',
        'Max_Tensao_Principal_Pa',
        'Desloc_Eixo_Z_m' # Rótulo corrigido 
    ])

    print("=== INICIANDO EXTRAÇÃO DE DADOS (1000 CASOS) ===")

    # Identifica os arquivos novos pelo prefixo correto
    arquivos_odb = [arq for arq in os.listdir('.') if arq.endswith('.odb') and arq.startswith('DoE_A36_')]
    
    if not arquivos_odb:
        print("Nenhum arquivo DoE_A36_ encontrado. Verifique a pasta.")

    for odb_name in arquivos_odb:
        nome_base = odb_name.replace('.odb', '')
        
        # Expressão regular para extrair os parâmetros do nome do arquivo com segurança
        # Exemplo suportado: DoE_A36_001_M4455g_Z1456mm_e2p7mm
        match = re.search(r'_M(\d+)g_Z(\d+)mm_e([\dp]+)mm', nome_base)
        
        if match:
            massa_kg = float(match.group(1)) / 1000.0
            z_mm = float(match.group(2))
            # Substitui o 'p' por '.' e converte para float
            esp_mm = float(match.group(3).replace('p', '.'))
        else:
            print("Aviso: Formato de nome nao reconhecido para " + nome_base)
            continue

        print("Extraindo resultados de: " + nome_base)
        
        try:
            odb = visualization.openOdb(path=odb_name)
            step = odb.steps.values()[0]
            frame = step.frames[-1] # Último frame = deformação/dano máximo
            
            # Variáveis Globais Máximas
            max_u = max([val.magnitude for val in frame.fieldOutputs['U'].values]) if 'U' in frame.fieldOutputs.keys() else 0.0
            max_peeq = max([val.data for val in frame.fieldOutputs['PEEQ'].values]) if 'PEEQ' in frame.fieldOutputs.keys() else 0.0
            max_mises = max([val.mises for val in frame.fieldOutputs['S'].values]) if 'S' in frame.fieldOutputs.keys() else 0.0
            max_principal = max([val.maxPrincipal for val in frame.fieldOutputs['S'].values]) if 'S' in frame.fieldOutputs.keys() else 0.0
            
            # ---------------------------------------------------------
            # FLECHA EXATA (EIXO Y)
            # U.data é um array [U1, U2, U3]. Pegamos o valor absoluto do eixo Y (índice 1).
            # ---------------------------------------------------------
            max_u2 = max([abs(val.data[1]) for val in frame.fieldOutputs['U'].values]) if 'U' in frame.fieldOutputs.keys() else 0.0

            # ---------------------------------------------------------
            # STATUS DE RUPTURA (0 = Intacta, 1 = Rompeu)
            # ---------------------------------------------------------
            rompeu = 0
            if 'STATUS' in frame.fieldOutputs.keys():
                if 0.0 in [val.data for val in frame.fieldOutputs['STATUS'].values]:
                    rompeu = 1
            
            odb.close()
            
            # Escreve a linha no CSV
            writer.writerow([nome_base, massa_kg, esp_mm, z_mm, max_u, max_peeq, max_mises, rompeu, max_principal, max_u2])
            
        except Exception as e:
            print("Erro ao processar " + odb_name + ": " + str(e))
            # Salva a linha indicando erro para não perder o rastreio do arquivo
            writer.writerow([nome_base, massa_kg, esp_mm, z_mm, 'ERRO', 'ERRO', 'ERRO', 'ERRO', 'ERRO', 'ERRO'])

print("\n=== EXTRAÇÃO CONCLUÍDA! Arquivo salvo como: " + csv_name + " ===")