# 1o Desafio MBA Engenharia de Software com IA - Full Cycle

## :: Descreva abaixo como executar a sua solução

### Pré-requisitos

- **Python 3.8+**
- **Docker Desktop**

##

### Passo a passo para execução

## 1. **Clone e configure o ambiente**

```bash
git clone https://github.com/marcosfsantos1980/1-mba-ia-desafio-ingestao-busca.git
cd 1-mba-ia-desafio-ingestao-busca

# Criar ambiente virtual
python -m venv venv

venv\Scripts\activate    # para Windows 

source venv/bin/activate # para Linux/Mac


# Instalar dependências
pip install -r requirements.txt
```

## 2. **Configure as variáveis de ambiente  (API key OpenAI)etc**

-Configure o arquivo `.env`:

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

## 4. **Verifique se o PDF esta na raiz do projeto**

- Faça a ingestão do arquivo atraves do  `ingest.py` (somente uma vez) para carregar os dados do PDF
no banco de dados

```bash
  python src\ingest.py

```

## 5. **Execute o chat**

```bash
   python src\chat.py

```

- Faça sua pergunta

## 6.  **Funcionamento**

-Caso tenha instalado tudo corretamente o Chat será inicializado e você poderá começara fazer sua pergunta.

**Exemplo prático:**
-Modelos de perguntas treinadas:

```bash

 :: Pergunta: "Qual o valor de faturamento da empresa Zenith Papel e Celulose?"
 :: Resposta: "O valor de faturamento da empresa Zenith Papel e Celulose � de R$ 225.460,35"

 :: Pergunta: "Qual foi o menor valor de faturamento?"
 :: Resposta: "O menor valor de faturamento é de R$ 225.460,35 da empresa Zenith Papel e Celulose EPP, fundada em 1931"

 :: Pergunta: "Qual é a capital do Amapá?" (fora do contexto)
 :: Resposta: "Não tenho informaçõe necessárias para responder sua pergunta."

```

## Boa Diversão
