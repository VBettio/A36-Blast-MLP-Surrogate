Predição de Blast Loading em Chapas de Aço A36 usando MLP e Active Learning
Repositório companion do artigo submetido ao SIGE: "Predição para Chapas de Aço A36 em Blast Loading: uma abordagem integrando calibração experimental, Redes Neurais e Amostragem Adaptativa".

📋 Visão Geral
Este projeto implementa um modelo substituto (Surrogate Model) baseado em Redes Neurais do tipo Multilayer Perceptron (MLP) para prever a integridade estrutural e a flecha máxima de chapas de aço ASTM A36 submetidas a detonações esféricas livres. O pipeline metodológico integra:

Calibração FEM: Modelo Abaqus/Explicit calibrado com ensaios de campo reais.
Amostragem Adaptativa (Active Learning): Geração de 1500 simulações em 3 fases, direcionando o esforço computacional para a fronteira de incerteza da ruptura (35%-65% e 45%-55%).
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
📄 Licença
Este projeto está licenciado sob a Licença MIT — veja o arquivo LICENSE para detalhes.
