#!/usr/bin/env python3
from sistema_livraria import SistemaLivraria

def main():
    """Função principal"""
    try:
        sistema = SistemaLivraria(".")
        sistema.executar()
    except Exception as e:
        print(f"Erro ao iniciar o sistema: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()