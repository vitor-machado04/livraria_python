#!/usr/bin/env python3
from sistema_livraria import SistemaLivraria

def popular_banco_demonstracao():
    # Lista de livros clássicos brasileiros para demonstração
    livros_exemplo = [
        ("Dom Casmurro", "Machado de Assis", 1899, 29.90),
        ("O Cortiço", "Aluísio Azevedo", 1890, 25.50),
        ("Senhora", "José de Alencar", 1875, 24.90),
        ("O Guarani", "José de Alencar", 1857, 22.00),
        ("Memórias Póstumas de Brás Cubas", "Machado de Assis", 1881, 27.50),
        ("Quincas Borba", "Machado de Assis", 1891, 26.90),
        ("A Moreninha", "Joaquim Manuel de Macedo", 1844, 19.90),
        ("Iracema", "José de Alencar", 1865, 21.50),
        ("O Ateneu", "Raul Pompéia", 1888, 23.90),
        ("Lucíola", "José de Alencar", 1862, 20.90),
        ("Helena", "Machado de Assis", 1876, 25.90),
        ("A Escrava Isaura", "Bernardo Guimarães", 1875, 18.90),
        ("O Mulato", "Aluísio Azevedo", 1881, 24.50),
        ("Casa Velha", "Machado de Assis", 1885, 22.90),
        ("Til", "José de Alencar", 1872, 21.90)
    ]
    
    print("="*60)
    print("    SCRIPT DE DEMONSTRAÇÃO - SISTEMA LIVRARIA")
    print("="*60)
    print("Este script irá popular o banco de dados com livros de exemplo")
    print("para demonstrar as funcionalidades do sistema.\n")
    
    resposta = input("Deseja continuar? (s/N): ").lower()
    if resposta not in ['s', 'sim']:
        print("Operação cancelada.")
        return
    
    try:
        # Inicializar sistema
        sistema = SistemaLivraria(".")
        
        print(f"\nAdicionando {len(livros_exemplo)} livros ao banco de dados...")
        
        livros_adicionados = 0
        
        for titulo, autor, ano, preco in livros_exemplo:
            try:
                id_livro = sistema.db_manager.adicionar_livro(titulo, autor, ano, preco)
                livros_adicionados += 1
                print(f"✓ {livros_adicionados:2d}. {titulo} - {autor}")
            except Exception as e:
                print(f"Erro ao adicionar '{titulo}': {e}")
        
        print(f"\n✓ Demonstração concluída!")
        print(f"  Livros adicionados: {livros_adicionados}")
        
        # Mostrar estatísticas
        todos_livros = sistema.db_manager.obter_todos_livros()
        print(f"  Total no banco: {len(todos_livros)}")
        
        # Criar backup
        backup_path = sistema.gerenciador_arquivos.criar_backup()
        print(f"  Backup criado: {backup_path.split('\\')[-1]}")
        
        # Exportar para CSV
        csv_path = sistema.gerenciador_arquivos.exportar_csv(todos_livros, "demonstracao_completa.csv")
        print(f"  CSV exportado: demonstracao_completa.csv")
        
        print(f"\n✓ Sistema pronto para uso!")
        print(f"  Execute: python main.py")
        print(f"  Ou: python sistema_livraria.py")
        
    except Exception as e:
        print(f"Erro durante a demonstração: {e}")

if __name__ == "__main__":
    popular_banco_demonstracao()