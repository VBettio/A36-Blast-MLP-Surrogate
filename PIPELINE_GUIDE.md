Guia de Reprodução do Pipeline (Active Learning)
Este repositório implementa o Active Learning em 3 fases. Como as Fases 2 e 3 dependem do treinamento prévio da rede, a alteração dos limiares de probabilidade deve ser feita manualmente pelo pesquisador no script MLP_Training_Pipeline.ipynb.

Siga os passos abaixo para reproduzir o experimento completo:

Fase 1: Amostragem Cega (LHS)
Execute o script A36_DoE_M_Z_e.py no Abaqus.
Extraia os resultados para o Dataset_1.csv.
Treine a MLP no Jupyter Notebook.

Fase 2: Fronteira Larga (40% a 80%)
No final do Jupyter Notebook, localize o bloco "AMOSTRAGEM ADAPTATIVA".
Altere os limiares para: >= 0.40 e <= 0.80.
Execute o bloco para gerar o arquivo DoE_Fronteira_Abaqus.csv.
Execute o script A36_Border_M_Z_e.py no Abaqus (lendo o CSV gerado).
Extraia os resultados, concatene com o Dataset 1 e retreine a MLP.

Fase 3: Fronteira Fina (45% a 55%)
No Jupyter Notebook, altere os limiares para: >= 0.45 e <= 0.55.
Gere o novo DoE_Fronteira_Abaqus.csv.
Execute o script A36_Border_M_Z_e.py no Abaqus novamente.
Concatene todos os dados e retreine o modelo final.
