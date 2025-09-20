from search import search_prompt

def print_header():
    print("*" * 60)
    print("                       CHAT - LangChain")
    print("-" * 60)
    print("          Use:  'nt', 'cls' ou 'clear' para limpar a tela")
    print("          Use:  'sair', 'end' ou 'quit' para encerrar")
    print("*" * 60)

def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear') 

def main():
    print_header()
    
    # Inicializar sistema de busca (como importar um service)
    print("Carregando contexto inicial...")
    search_system = search_prompt()
       
    print("Informações carregadas com sucesso!\n")
    
    while True:
        try:
            # Input 
            pergunta = input("\nPor favor, faça sua pergunta: ").strip()            
    
            if pergunta.lower() in ['sair','end', 'quit', 'exit']:
                print("\n Chat finalizado com sucesso")
                break  # sair do loop
                        
            elif pergunta.lower() in ['limpar', 'cls', 'nt','clear']:
                clear_screen()
                print_header()
                continue    
              
            elif not pergunta:
                print("Faça sua pergunta para continuar")
                continue
            
            # Processar pergunta
            print("\nPensando...")
            resposta = search_system.generate_answer(pergunta)
    
            print("\n" + "=" * 60)
            print(f"PERGUNTA: {pergunta}")
            print("=" * 60)
            print(f"RESPOSTA: {resposta}")
            print("=" * 60)
            
        except KeyboardInterrupt:            
            print("\n\nChat finalizado!")
            break
        
        except Exception as e:
            print(f"\nErro inesperado: {str(e)}")
            print("Tente novamente ou digite 'sair' para encerrar")

if __name__ == "__main__":
    main()