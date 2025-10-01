#!/usr/bin/env python3
"""
Arquivo principal para executar o Sistema de Gerenciamento de Livraria
"""

from sistema_livraria import SistemaLivraria

def main():
    """Função principal"""
    try:
        # Criar e executar o sistema (usando diretório atual)
        sistema = SistemaLivraria(".")
        sistema.executar()
    except Exception as e:
        print(f"Erro ao iniciar o sistema: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()