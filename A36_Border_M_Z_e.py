# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
import job
import csv

# ==========================================
# 1. LEITURA DO ARQUIVO CSV DE FRONTEIRA
# ==========================================
arquivo_entrada_csv = 'DoE_Fronteira_Abaqus.csv'
massas_tnt = []
alturas_z = []
espessuras = []

print("Lendo pontos de fronteira do arquivo: " + arquivo_entrada_csv)
with open(arquivo_entrada_csv, 'r') as f:
    reader = csv.reader(f)
    header = next(reader) # Pula o cabeçalho
    for row in reader:
        # Colunas: Massa_TNT_kg, Distancia_Z_m, Espessura_m
        massas_tnt.append(float(row[0]))
        alturas_z.append(float(row[1]))
        espessuras.append(float(row[2]))

# ==========================================
# 2. PARÂMETROS DO ESPAÇO DE PROJETO
# ==========================================
N_SIMULACOES = len(massas_tnt)

model_name = 'Model_1' 
nome_rp = 'RP-1'
nome_interacao = 'Detonacao'
cae_name = 'A36_SIGE.cae' # ARQUIVO .CAE

openMdb(cae_name)

# ==========================================
# 3. EXECUÇÃO EM LOTE 
# ==========================================
with open('DoE_Fronteira_Resultados.csv', mode='w') as f:
    writer = csv.writer(f, delimiter=',', lineterminator='\n')
    writer.writerow(['Rodada', 'Job_Name', 'Massa_TNT_kg', 'Distancia_Z_m', 'Espessura_m', 'Status'])

    for i in range(N_SIMULACOES):
        
        w = massas_tnt[i]
        d = alturas_z[i]
        t = espessuras[i]
        
        massa_g = int(w * 1000)
        dist_mm = int(d * 1000)
        
        # Converte a espessura para mm, arredonda para 2 casas e troca '.' por 'p'
        esp_mm_float = round(t * 1000, 2)
        esp_str = str(esp_mm_float).replace('.', 'p')
        
        # O nome do job usará a string segura (ex: e2p75mm)
        nome_job = 'DoE_Front_{:03d}_M{}g_Z{}mm_e{}mm'.format(i+1, massa_g, dist_mm, esp_str)
        
        print("--- Processando Rodada {}/{} : {} ---".format(i+1, N_SIMULACOES, nome_job))
        
        try:
            # 1. Modificações do Modelo
            # ==========================================================
            # Alteração da espessura da chapa
            # ==========================================================
            mdb.models[model_name].sections['steel_profile'].setValues(thickness=t)
            # ==========================================================
            # 2. CORREÇÃO DA ALTURA DE DETONAÇÃO DO CONWEP (Dinâmica de Ponto RP-1)
            # ==========================================================
            a = mdb.models[model_name].rootAssembly
            novo_rp = a.ReferencePoint(point=(0.0, d, 0.0))
            rp_key = novo_rp.id
            regiao_conwep = a.Set(referencePoints=(a.referencePoints[rp_key],), name='Set_Explosivo_Temp')
            mdb.models[model_name].interactions[nome_interacao].setValues(sourcePoint=regiao_conwep)
            # ==========================================================
            # 2.5 CÁLCULO DINÂMICO DO TEMPO DE SIMULAÇÃO
            # ==========================================================
            # Tempo = (Distância / Velocidade do Som) + 3 ms de resposta estrutural
            tempo_analise = (d / 340.0) + 0.003
            
            # ATENÇÃO: Coloque o nome exato do seu Step aqui (ex: 'Step-1')
            nome_do_step = 'Detonacao' 
            mdb.models[model_name].steps[nome_do_step].setValues(timePeriod=tempo_analise)
            # ==========================================================
            # 3. Alteração da massa equivalente de TNT
            # ==========================================================
            mdb.models[model_name].interactionProperties[nome_interacao].setValues(massTNT=w)
            
            # 2. Execução no Solver
            if nome_job in mdb.jobs.keys(): 
                del mdb.jobs[nome_job]
            
            # Submissão do Job mantida EXATAMENTE como no seu script original
            mdb.Job(name=nome_job, model=model_name)
            mdb.jobs[nome_job].submit()
            mdb.jobs[nome_job].waitForCompletion()
            
            # MODIFICAÇÃO: Bloco "3. EXTRAÇÃO IMEDIATA DO PRINT SCREEN (.PNG)" integralmente removido.
            
            writer.writerow([i+1, nome_job, w, d, t, 'Sucesso'])
            
            # ==========================================================
            # 4. LIMPEZA DA ÁRVORE (Impede o acúmulo de RPs do CONWEP)
            # ==========================================================
            del a.features[novo_rp.name]
            del a.sets['Set_Explosivo_Temp']

        except Exception as e:
            print("Erro critico no job " + nome_job + ": " + str(e))
            writer.writerow([i+1, nome_job, w, d, t, 'Erro'])
            continue 

print("\n=== PROCESSO COMPLETO ===")