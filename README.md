Predição de Blast Loading em Chapas de Aço A36 usando MLP e Active Learning
Repositório companion do artigo submetido ao SIGE: "Predição para Chapas de Aço A36 em Blast Loading: uma abordagem integrando calibração experimental, Redes Neurais e Amostragem Adaptativa".

📋 Visão Geral
Este projeto implementa um modelo substituto (Surrogate Model) baseado em Redes Neurais do tipo Multilayer Perceptron (MLP) para prever a integridade estrutural e a flecha máxima de chapas de aço ASTM A36 submetidas a detonações esféricas livres. O pipeline metodológico integra:

Calibração FEM: Modelo Abaqus/Explicit calibrado com ensaios de campo reais.
Amostragem Adaptativa (Active Learning): Geração de 1500 simulações em 3 fases, direcionando o esforço computacional para a fronteira de incerteza da ruptura (45%-80% e 47.5%-52.5%).
Arquitetura Bifurcada MLP: Um classificador (ruptura) e um regressor (flecha) independentes.

📂 Estrutura do Repositório
Abaqus_Scripts/: Scripts Python para automação das simulações no Abaqus 6.14 (Fase 1: LHS, Fases 2 e 3: Fronteiras).
MLP_Training_Pipeline.ipynb: Jupyter Notebook contendo o pré-processamento, treinamento bifurcado, validação K-Fold (10 folds) e a rotina de geração de novos DoEs (Active Learning).
Datasets/: Arquivos .csv com os 1500 cenários simulados (Ground Truth numérico).
Models/: Arquivos .pkl com os modelos MLP e scalers já treinados, prontos para inferência imediata.

⚙️ Requisitos (Ambiente Python)
Para executar o notebook de Machine Learning, instale as dependências:

pip install pandas numpy scikit-learn matplotlib seaborn plotly gdown

🚀 Como Reproduzir
Simulação: Execute os scripts na pasta Abaqus_Scripts/ dentro do software Abaqus para gerar os arquivos de saída (ou utilize os CSVs já fornecidos).
Treinamento: Execute o MLP_Training_Pipeline.ipynb no Google Colab ou localmente. O script fará a carga dos dados, filtragem física, treinamento das redes e validação cruzada.
Inferência: Carregue os modelos .pkl salvos para prever novos cenários balísticos instantaneamente.

## 🔬 Notas Metodológicas e Limitações

**1. Parâmetros de Iniciação de Dano (Johnson-Cook)**
O modelo numérico no Abaqus engloba a dependência da triaxialidade de tensões e da taxa de deformação na iniciação do dano ($D_1$ a $D_5$). Dada a escassez de parâmetros dinâmicos de ruptura exatos para o lote específico de Aço A36 e a impraticabilidade de ensaios destrutivos dedicados, adotou-se um conjunto de constantes de dano fenomenológicas para aços estruturais (D1=0.14, D2=0.54, D3=-1.5, D4=0.014, D5=1.12) e um deslocamento à falha de $u_f = 0.0025$ m. O foco deste trabalho é a viabilidade do *pipeline* de *Active Learning*, utilizando um *Ground Truth* sintético com comportamentos não-lineares severos, e não a caracterização metalográfica do aço.

**2. Matriz de Confusão vs. Validação Cruzada (K-Fold)**
A matriz de confusão disponibilizada reflete o panorama global agregando todo o *dataset* (1500 amostras), evidenciando os 23 Falsos Negativos totais. A validação `StratifiedKFold` (10 partições) foi utilizada rigorosamente no treinamento para assegurar a consistência das métricas num domínio artificialmente enriquecido na fronteira de falha (devido ao *Active Learning*).

**3. A Contagem de Fraturas no Active Learning**
Na Fase 3, embora a rede preliminar previsse 50% de chance de ruptura para os novos casos selecionados, a simulação em Elementos Finitos resultou em uma proporção menor de falhas confirmadas (apenas 62 rupturas). Esse comportamento não é uma inconsistência, mas a própria justificativa do método: a injeção desses cenários limítrofes corrigiu o viés conservador da MLP inicial, forçando-a a retrair seu hiperplano e aprender o limite exato calculado pelo Abaqus.

📄 Licença
Este projeto está licenciado sob a Licença MIT — veja o arquivo LICENSE para detalhes.
