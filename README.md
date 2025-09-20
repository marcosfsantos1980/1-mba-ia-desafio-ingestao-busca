# 1o Desafio MBA Engenharia de Software com IA - Full Cycle
## ?? Descreva abaixo como executar a sua solu��o.

### Pr�-requisitos
- **Python 3.8+** 
- **Docker Desktop**

### Passo a passo para execu��o


## 1. **Clone e configure o ambiente**
```bash
git clone https://github.com/marcosfsantos1980/1-mba-ia-desafio-ingestao-busca.git
cd 1-mba-ia-desafio-ingestao-busca

# Criar ambiente virtual
python -m venv venv


# Instalar depend�ncias
pip install -r requirements.txt
```
## 2. **Configure as vari�veis de ambiente  (API key OpenAI)etc **
- Configure o arquivo `.env`:
```env
OPENAI_MODEL='text-embedding-3-small'
OPENAI_API_KEY='[SUA API KEY]'
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME='gpt5_collection'
PDF_PATH='./document.pdf'
```

## 3. **Suba o Container do banco de dados postgres/pgvector**
```bash
docker compose up -d
```

## 4. **Verifique se o PDF esta na raiz do projeto **
- Fa�a o ingest�o do arquivo atraves do  `ingest.py` (somente uma vez) para carregar os dados do PDF
no banco de dados
```bash
  python src\ingest.py

```

## 5. **Execute o chat**
```bash
   python src\chat.py
```
- Fa�a sua pergunta
## 6.  **FUNCIONAMENTO**

**Exemplo pr�tico:**
- Modelos de perguntas treinadas 
```
?? Pergunta: "Qual o valor de faturamento da empresa Zenith Papel e Celulose?"
?? Resposta: "O valor de faturamento da empresa Zenith Papel e Celulose � de R$ 225.460,35"

?? Pergunta: "Qual foi o menor valor de faturamento?"
?? Resposta: "O menor valor de faturamento � de R$ 225.460,35 da empresa Zenith Papel e Celulose EPP, fundada em 1931"

?? Pergunta: "Qual � a capital do Amap�?" (fora do contexto)
?? Resposta: "N�o tenho informa��es necess�rias para responder sua pergunta."
```

## boa divers�o
