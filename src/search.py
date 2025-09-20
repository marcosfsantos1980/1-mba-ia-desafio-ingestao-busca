#from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from typing import List, Dict, Optional
import os 
from dotenv import load_dotenv

load_dotenv()

prompt = PromptTemplate.from_template(
"""
CONTEXTO:
{contexto}

RULES:
- Responda somente com base no CONTEXTO e utilize.
- O conteudo para resposta esta no CONTEXTO é esta seperado em colunas, iniciando
  pelo nome da EMPRESA, valor de FATURAMENTO e o ANO de FUNDAÇÃO da empresa.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

EXEMPLOS DE PERGUNTAS QUE VOCÊ DEVE RESPONDER:
Pergunta: "Qual o faturamento da empresa XXXX no ano de yyyy?"
Resposta: "O valor de faturamento da empresa XXXX é de 99999 no ano de yyyy"

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""
)
class LANGSearch:
    """
    Classe principal de busca - como um SearchService no TypeScript
    Responsável por implementar todo o fluxo RAG
    """
    def __init__(self):
        """Constructor - inicializa conexões"""        
        self.database_url = os.getenv("DATABASE_URL")
        self.collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME")
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        #text-embedding-ada-002
        #text-embedding-3-small
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """
        Inicializa conexão com banco vetorial        
        """
        try:
            self.vectorstore = PGVector(
                embeddings=self.embeddings,
                collection_name=self.collection_name,
                connection=self.database_url,
                use_jsonb=True,
            )
            print(" Conectado ao banco vetorial")
        except Exception as e:
            print(f" Erro ao conectar ao banco vetorial: {e}")
            raise e
    
    def search_documents(self, query: str, k: int = 10) -> List[Dict]:
        if not self.vectorstore:
            raise Exception("Banco vetorial não inicializado")
        
        try:
            # Busca por similaridade com score
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            
            # resultados
            formatted_results = []
            for document, score in results:
                formatted_results.append({
                    'content': document.page_content,    # texto do chunk
                    'metadata': document.metadata,       # informações extras
                    'score': score                       # quão similar (menor = mais similar)
                })
            
            return formatted_results
            
        except Exception as e:
            print(f" Erro na busca: {e}")
            return []  # lista vazia como fallback
    
    def generate_answer(self, query: str) -> str:
        try:            
            print("Buscando documentos relevantes...")
            documents = self.search_documents(query, k=10)
            
            if not documents: 
                return "Não tenho informações necessárias para responder sua pergunta."
            
            #conteúdo dos documentos
            context = "\n\n".join([doc['content'] for doc in documents])
            prompt_text = prompt.format(contexto=context, tool="", pergunta=query)
               
            # Processa resposta na LLM
            print(" Gerando resposta...")       
            messages = [
                SystemMessage(content=prompt_text),
                HumanMessage(content=query)
            ]
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
            
            response = llm.invoke(messages)
            
            return response.content.strip()  
            
        except Exception as e:
            print(f" Erro ao gerar resposta: {e}")
            return "Erro interno: Não foi possível processar sua pergunta."

def search_prompt(question: Optional[str] = None) -> Optional[LANGSearch]:
    try:
        lang_search = LANGSearch()
        return lang_search
    except Exception as e:
        print(f"Erro ao fazer a busca: {e}")
        return None

# Para testes rápidos (como export para usar em outros arquivos)
if __name__ == "__main__":
    # Teste básico - só executa se rodar python src/search.py
    search_system = search_prompt()
    if search_system:
        test_query = "Qual o valor do faturamento da emprea Roxo Imobiliaria" 
        result = search_system.generate_answer(test_query)
        print(f"\nPergunta: {test_query}")
        print(f"Resposta: {result}")
    else:
        print("Não foi possível inicializar sistema de busca")
    
    def search_prompt1(question=None):
        embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))

        store = PGVector(
            embeddings=embeddings,
            collection_name=os.getenv("PGVECTOR_COLLECTION_NAME"),
            connection=os.getenv("DATABASE_URL"),
            use_jsonb=True,
        )

        results = store.similarity_search_with_score(question, k=1)

        for i, (doc, score) in enumerate(results, start=1):
            return doc.page_content.strip()
    
        return "Não tenho informações necessárias para responder sua pergunta."
    def call_chat():       
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
        agent_chain = create_react_agent(llm, None, prompt)

        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent_chain, 
            tools=None, 
            verbose=True, 
            # max_iterations=5
        )
        #print(agent_executor.invoke({"pergunta": "What is the capital of Iran?","contexto":"conteudo do pdf" }))