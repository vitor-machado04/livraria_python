import sqlite3
import csv
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class ValidationError(Exception):
    """Exceção personalizada para erros de validação"""
    pass


class Validador:
    @staticmethod
    def validar_titulo(titulo: str) -> str:
        if not titulo or not titulo.strip():
            raise ValidationError("O título não pode estar vazio")
        titulo = titulo.strip()
        if len(titulo) > 200:
            raise ValidationError("O título não pode ter mais de 200 caracteres")
        return titulo
    
    @staticmethod
    def validar_autor(autor: str) -> str:
        if not autor or not autor.strip():
            raise ValidationError("O nome do autor não pode estar vazio")
        autor = autor.strip()
        if len(autor) > 100:
            raise ValidationError("O nome do autor não pode ter mais de 100 caracteres")
        return autor
    
    @staticmethod
    def validar_ano(ano: str) -> int:
        try:
            ano_int = int(ano)
            if ano_int < 1000 or ano_int > datetime.now().year + 1:
                raise ValidationError(f"Ano deve estar entre 1000 e {datetime.now().year + 1}")
            return ano_int
        except ValueError:
            raise ValidationError("Ano deve ser um número inteiro válido")
    
    @staticmethod
    def validar_preco(preco: str) -> float:
        try:
            # Substitui vírgula por ponto para aceitar formato brasileiro
            preco = preco.replace(',', '.')
            preco_float = float(preco)
            if preco_float < 0:
                raise ValidationError("O preço não pode ser negativo")
            if preco_float > 999999.99:
                raise ValidationError("O preço não pode ser maior que R$ 999.999,99")
            return round(preco_float, 2)
        except ValueError:
            raise ValidationError("Preço deve ser um número válido (ex: 29.90 ou 29,90)")


class GerenciadorArquivos:
    def __init__(self, diretorio_base: str):
        self.diretorio_base = Path(diretorio_base)
        self.diretorio_data = self.diretorio_base / "data"
        self.diretorio_backups = self.diretorio_base / "backups"
        self.diretorio_exports = self.diretorio_base / "exports"
        self.arquivo_db = self.diretorio_data / "livraria.db"
        
        # Criar diretórios se não existirem
        self._criar_diretorios()
    
    def _criar_diretorios(self):
        for diretorio in [self.diretorio_data, self.diretorio_backups, self.diretorio_exports]:
            diretorio.mkdir(parents=True, exist_ok=True)
    
    def criar_backup(self) -> str:
        if not self.arquivo_db.exists():
            raise FileNotFoundError("Banco de dados não encontrado para backup")
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_backup = f"backup_livraria_{timestamp}.db"
        caminho_backup = self.diretorio_backups / nome_backup
        
        shutil.copy2(self.arquivo_db, caminho_backup)
        
        # Limpar backups antigos após criar o novo
        self._limpar_backups_antigos()
        
        return str(caminho_backup)
    
    def _limpar_backups_antigos(self):
        backups = list(self.diretorio_backups.glob("backup_livraria_*.db"))
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Remove backups além dos 5 mais recentes
        for backup_antigo in backups[5:]:
            backup_antigo.unlink()
            print(f"Backup antigo removido: {backup_antigo.name}")
    
    def exportar_csv(self, dados: List[Tuple], nome_arquivo: str = "livros_exportados.csv") -> str:
        caminho_csv = self.diretorio_exports / nome_arquivo
        
        with open(caminho_csv, 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            # Cabeçalho
            writer.writerow(['ID', 'Título', 'Autor', 'Ano de Publicação', 'Preço'])
            # Dados
            writer.writerows(dados)
        
        return str(caminho_csv)
    
    def importar_csv(self, nome_arquivo: str) -> List[Dict]:
        caminho_csv = self.diretorio_exports / nome_arquivo
        
        if not caminho_csv.exists():
            raise FileNotFoundError(f"Arquivo {nome_arquivo} não encontrado no diretório exports")
        
        livros = []
        with open(caminho_csv, 'r', encoding='utf-8') as arquivo:
            reader = csv.DictReader(arquivo)
            for row in reader:
                livros.append({
                    'titulo': row['Título'],
                    'autor': row['Autor'],
                    'ano_publicacao': int(row['Ano de Publicação']),
                    'preco': float(row['Preço'])
                })
        
        return livros


class DatabaseManager:
    def __init__(self, caminho_db: str):
        self.caminho_db = caminho_db
        self._criar_tabela()
    
    def _criar_tabela(self):
        with sqlite3.connect(self.caminho_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS livros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    ano_publicacao INTEGER NOT NULL,
                    preco REAL NOT NULL
                )
            ''')
            conn.commit()
    
    def adicionar_livro(self, titulo: str, autor: str, ano_publicacao: int, preco: float) -> int:
        with sqlite3.connect(self.caminho_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO livros (titulo, autor, ano_publicacao, preco)
                VALUES (?, ?, ?, ?)
            ''', (titulo, autor, ano_publicacao, preco))
            conn.commit()
            return cursor.lastrowid
    
    def obter_todos_livros(self) -> List[Tuple]:
        with sqlite3.connect(self.caminho_db) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM livros ORDER BY titulo')
            return cursor.fetchall()
    
    def buscar_livros_por_autor(self, autor: str) -> List[Tuple]:
        with sqlite3.connect(self.caminho_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM livros 
                WHERE LOWER(autor) LIKE LOWER(?) 
                ORDER BY titulo
            ''', (f'%{autor}%',))
            return cursor.fetchall()
    
    def atualizar_preco_livro(self, id_livro: int, novo_preco: float) -> bool:
        with sqlite3.connect(self.caminho_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE livros SET preco = ? WHERE id = ?
            ''', (novo_preco, id_livro))
            conn.commit()
            return cursor.rowcount > 0
    
    def remover_livro(self, id_livro: int) -> bool:
        with sqlite3.connect(self.caminho_db) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM livros WHERE id = ?', (id_livro,))
            conn.commit()
            return cursor.rowcount > 0
    
    def obter_livro_por_id(self, id_livro: int) -> Optional[Tuple]:
        with sqlite3.connect(self.caminho_db) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM livros WHERE id = ?', (id_livro,))
            return cursor.fetchone()


class SistemaLivraria:
    def __init__(self, diretorio_base: str = "meu_sistema_livraria"):
        self.gerenciador_arquivos = GerenciadorArquivos(diretorio_base)
        self.db_manager = DatabaseManager(str(self.gerenciador_arquivos.arquivo_db))
        self.validador = Validador()
    
    def _fazer_backup_automatico(self):
        try:
            backup_path = self.gerenciador_arquivos.criar_backup()
            print(f"✓ Backup criado automaticamente: {Path(backup_path).name}")
        except Exception as e:
            print(f"Aviso: Não foi possível criar backup: {e}")
    
    def adicionar_livro(self):
        print("\n=== ADICIONAR NOVO LIVRO ===")
        
        try:
            titulo = input("Título do livro: ")
            titulo = self.validador.validar_titulo(titulo)
            
            autor = input("Autor: ")
            autor = self.validador.validar_autor(autor)
            
            ano = input("Ano de publicação: ")
            ano = self.validador.validar_ano(ano)
            
            preco = input("Preço (R$): ")
            preco = self.validador.validar_preco(preco)
            
            # Fazer backup antes da modificação
            self._fazer_backup_automatico()
            
            # Adicionar livro
            id_livro = self.db_manager.adicionar_livro(titulo, autor, ano, preco)
            
            print(f"\n✓ Livro adicionado com sucesso! ID: {id_livro}")
            print(f"  Título: {titulo}")
            print(f"  Autor: {autor}")
            print(f"  Ano: {ano}")
            print(f"  Preço: R$ {preco:.2f}")
            
        except ValidationError as e:
            print(f"\nErro de validação: {e}")
        except Exception as e:
            print(f"\nErro ao adicionar livro: {e}")
    
    def exibir_todos_livros(self):
        print("\n=== TODOS OS LIVROS CADASTRADOS ===")
        
        try:
            livros = self.db_manager.obter_todos_livros()
            
            if not livros:
                print("Nenhum livro cadastrado.")
                return
            
            print(f"\nTotal de livros: {len(livros)}\n")
            print(f"{'ID':<5} {'Título':<30} {'Autor':<25} {'Ano':<6} {'Preço':<10}")
            print("-" * 80)
            
            for livro in livros:
                id_livro, titulo, autor, ano, preco = livro
                titulo_truncado = titulo[:29] + "..." if len(titulo) > 30 else titulo
                autor_truncado = autor[:24] + "..." if len(autor) > 25 else autor
                print(f"{id_livro:<5} {titulo_truncado:<30} {autor_truncado:<25} {ano:<6} R$ {preco:<7.2f}")
            
        except Exception as e:
            print(f"Erro ao exibir livros: {e}")
    
    def atualizar_preco_livro(self):
        print("\n=== ATUALIZAR PREÇO DE LIVRO ===")
        
        try:
            id_livro = input("ID do livro: ")
            try:
                id_livro = int(id_livro)
            except ValueError:
                print("ID deve ser um número inteiro")
                return
            
            # Verificar se o livro existe
            livro = self.db_manager.obter_livro_por_id(id_livro)
            if not livro:
                print(f"Livro com ID {id_livro} não encontrado")
                return
            
            # Exibir informações atuais
            _, titulo, autor, ano, preco_atual = livro
            print(f"\nLivro encontrado:")
            print(f"  Título: {titulo}")
            print(f"  Autor: {autor}")
            print(f"  Ano: {ano}")
            print(f"  Preço atual: R$ {preco_atual:.2f}")
            
            novo_preco = input("\nNovo preço (R$): ")
            novo_preco = self.validador.validar_preco(novo_preco)
            
            # Fazer backup antes da modificação
            self._fazer_backup_automatico()
            
            # Atualizar preço
            if self.db_manager.atualizar_preco_livro(id_livro, novo_preco):
                print(f"\n✓ Preço atualizado com sucesso!")
                print(f"  Preço anterior: R$ {preco_atual:.2f}")
                print(f"  Novo preço: R$ {novo_preco:.2f}")
            else:
                print(f"Erro ao atualizar preço")
            
        except ValidationError as e:
            print(f"\nErro de validação: {e}")
        except Exception as e:
            print(f"\nErro ao atualizar preço: {e}")
    
    def remover_livro(self):
        print("\n=== REMOVER LIVRO ===")
        
        try:
            id_livro = input("ID do livro a ser removido: ")
            try:
                id_livro = int(id_livro)
            except ValueError:
                print("ID deve ser um número inteiro")
                return
            
            # Verificar se o livro existe
            livro = self.db_manager.obter_livro_por_id(id_livro)
            if not livro:
                print(f"Livro com ID {id_livro} não encontrado")
                return
            
            # Exibir informações do livro
            _, titulo, autor, ano, preco = livro
            print(f"\nLivro a ser removido:")
            print(f"  ID: {id_livro}")
            print(f"  Título: {titulo}")
            print(f"  Autor: {autor}")
            print(f"  Ano: {ano}")
            print(f"  Preço: R$ {preco:.2f}")
            
            confirmacao = input("\nTem certeza que deseja remover este livro? (s/N): ").lower()
            if confirmacao != 's' and confirmacao != 'sim':
                print("Operação cancelada.")
                return
            
            # Fazer backup antes da modificação
            self._fazer_backup_automatico()
            
            # Remover livro
            if self.db_manager.remover_livro(id_livro):
                print(f"\n✓ Livro removido com sucesso!")
            else:
                print(f"Erro ao remover livro")
            
        except Exception as e:
            print(f"\nErro ao remover livro: {e}")
    
    def buscar_livros_por_autor(self):
        print("\n=== BUSCAR LIVROS POR AUTOR ===")
        
        try:
            autor = input("Nome do autor (busca parcial): ").strip()
            if not autor:
                print("Nome do autor não pode estar vazio")
                return
            
            livros = self.db_manager.buscar_livros_por_autor(autor)
            
            if not livros:
                print(f"Nenhum livro encontrado para o autor '{autor}'")
                return
            
            print(f"\nLivros encontrados para '{autor}': {len(livros)}\n")
            print(f"{'ID':<5} {'Título':<30} {'Autor':<25} {'Ano':<6} {'Preço':<10}")
            print("-" * 80)
            
            for livro in livros:
                id_livro, titulo, autor_livro, ano, preco = livro
                titulo_truncado = titulo[:29] + "..." if len(titulo) > 30 else titulo
                autor_truncado = autor_livro[:24] + "..." if len(autor_livro) > 25 else autor_livro
                print(f"{id_livro:<5} {titulo_truncado:<30} {autor_truncado:<25} {ano:<6} R$ {preco:<7.2f}")
            
        except Exception as e:
            print(f"Erro ao buscar livros: {e}")
    
    def exportar_dados_csv(self):
        print("\n=== EXPORTAR DADOS PARA CSV ===")
        
        try:
            livros = self.db_manager.obter_todos_livros()
            
            if not livros:
                print("Nenhum livro cadastrado para exportar.")
                return
            
            nome_arquivo = input("Nome do arquivo CSV (pressione Enter para usar padrão): ").strip()
            if not nome_arquivo:
                nome_arquivo = "livros_exportados.csv"
            elif not nome_arquivo.endswith('.csv'):
                nome_arquivo += '.csv'
            
            caminho_arquivo = self.gerenciador_arquivos.exportar_csv(livros, nome_arquivo)
            
            print(f"\n✓ Dados exportados com sucesso!")
            print(f"  Arquivo: {caminho_arquivo}")
            print(f"  Total de livros exportados: {len(livros)}")
            
        except Exception as e:
            print(f"Erro ao exportar dados: {e}")
    
    def importar_dados_csv(self):
        print("\n=== IMPORTAR DADOS DE CSV ===")
        
        try:
            # Listar arquivos CSV disponíveis
            arquivos_csv = list(self.gerenciador_arquivos.diretorio_exports.glob("*.csv"))
            
            if not arquivos_csv:
                print("Nenhum arquivo CSV encontrado no diretório exports.")
                return
            
            print("Arquivos CSV disponíveis:")
            for i, arquivo in enumerate(arquivos_csv, 1):
                print(f"  {i}. {arquivo.name}")
            
            nome_arquivo = input("\nNome do arquivo CSV ou número: ").strip()
            
            # Se for número, usar o arquivo correspondente
            if nome_arquivo.isdigit():
                indice = int(nome_arquivo) - 1
                if 0 <= indice < len(arquivos_csv):
                    nome_arquivo = arquivos_csv[indice].name
                else:
                    print("Número inválido")
                    return
            elif not nome_arquivo.endswith('.csv'):
                nome_arquivo += '.csv'
            
            livros = self.gerenciador_arquivos.importar_csv(nome_arquivo)
            
            print(f"\nDados carregados do arquivo: {len(livros)} livros")
            
            # Mostrar preview dos dados
            print("\nPreview dos dados:")
            for i, livro in enumerate(livros[:3], 1):
                print(f"  {i}. {livro['titulo']} - {livro['autor']} ({livro['ano_publicacao']}) - R$ {livro['preco']:.2f}")
            
            if len(livros) > 3:
                print(f"  ... e mais {len(livros) - 3} livros")
            
            confirmacao = input(f"\nImportar {len(livros)} livros? (s/N): ").lower()
            if confirmacao != 's' and confirmacao != 'sim':
                print("Importação cancelada.")
                return
            
            # Fazer backup antes da modificação
            self._fazer_backup_automatico()
            
            # Importar livros
            livros_importados = 0
            livros_erro = 0
            
            for livro in livros:
                try:
                    # Validar dados
                    titulo = self.validador.validar_titulo(livro['titulo'])
                    autor = self.validador.validar_autor(livro['autor'])
                    ano = livro['ano_publicacao']
                    preco = livro['preco']
                    
                    # Adicionar ao banco
                    self.db_manager.adicionar_livro(titulo, autor, ano, preco)
                    livros_importados += 1
                    
                except Exception as e:
                    livros_erro += 1
                    print(f"Erro ao importar livro '{livro.get('titulo', 'N/A')}': {e}")
            
            print(f"\n✓ Importação concluída!")
            print(f"  Livros importados: {livros_importados}")
            if livros_erro > 0:
                print(f"  Livros com erro: {livros_erro}")
            
        except FileNotFoundError as e:
            print(f"Arquivo não encontrado: {e}")
        except Exception as e:
            print(f"Erro ao importar dados: {e}")
    
    def fazer_backup_manual(self):
        print("\n=== FAZER BACKUP DO BANCO DE DADOS ===")
        
        try:
            backup_path = self.gerenciador_arquivos.criar_backup()
            print(f"\n✓ Backup criado com sucesso!")
            print(f"  Arquivo: {Path(backup_path).name}")
            print(f"  Localização: {backup_path}")
            
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
    
    def executar(self):
        print("="*60)
        print("    SISTEMA DE GERENCIAMENTO DE LIVRARIA")
        print("="*60)
        print("Bem-vindo ao sistema de gerenciamento da livraria!")
        print("Todos os dados são salvos automaticamente.")
        print("Backups são criados automaticamente antes de modificações.")
        
        while True:
            try:
                print("\n" + "="*50)
                print("MENU PRINCIPAL")
                print("="*50)
                print("1. Adicionar novo livro")
                print("2. Exibir todos os livros")
                print("3. Atualizar preço de um livro")
                print("4. Remover um livro")
                print("5. Buscar livros por autor")
                print("6. Exportar dados para CSV")
                print("7. Importar dados de CSV")
                print("8. Fazer backup do banco de dados")
                print("9. Sair")
                print("-"*50)
                
                opcao = input("Escolha uma opção (1-9): ").strip()
                
                if opcao == '1':
                    self.adicionar_livro()
                elif opcao == '2':
                    self.exibir_todos_livros()
                elif opcao == '3':
                    self.atualizar_preco_livro()
                elif opcao == '4':
                    self.remover_livro()
                elif opcao == '5':
                    self.buscar_livros_por_autor()
                elif opcao == '6':
                    self.exportar_dados_csv()
                elif opcao == '7':
                    self.importar_dados_csv()
                elif opcao == '8':
                    self.fazer_backup_manual()
                elif opcao == '9':
                    print("\n" + "="*50)
                    print("Obrigado por usar o Sistema de Livraria!")
                    print("Até logo!")
                    print("="*50)
                    break
                else:
                    print("\nOpção inválida. Por favor, escolha uma opção de 1 a 9.")
                
                # Pausa para o usuário ler a saída
                if opcao in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    input("\nPressione Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\nSistema interrompido pelo usuário.")
                print("Até logo!")
                break
            except Exception as e:
                print(f"\nErro inesperado: {e}")
                input("Pressione Enter para continuar...")


if __name__ == "__main__":
    # Caminho relativo ao diretório atual
    sistema = SistemaLivraria()
    sistema.executar()