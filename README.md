# Sistema de Gerenciamento de Livraria

## Descrição

Este é um sistema completo de gerenciamento de livraria que combina diversos conceitos de programação Python, incluindo:

- **SQLite**: Banco de dados para armazenar informações dos livros
- **Manipulação de Arquivos**: Organização e backup de dados
- **CSV**: Importação e exportação de dados
- **Validação de Dados**: Validação robusta de entradas do usuário
- **Pathlib e OS**: Gerenciamento de diretórios e arquivos

## Estrutura do Projeto

```
meu_sistema_livraria/
├── main.py                    # Arquivo principal para execução
├── sistema_livraria.py        # Sistema completo com todas as classes
├── README.md                  # Este arquivo
├── data/
│   └── livraria.db           # Banco de dados SQLite (criado automaticamente)
├── backups/
│   └── backup_livraria_*.db  # Backups automáticos (máximo 5)
└── exports/
    └── *.csv                 # Arquivos CSV exportados/importados
```

## Funcionalidades

### 1. Operações CRUD
- ✅ Adicionar novo livro
- ✅ Exibir todos os livros
- ✅ Atualizar preço de um livro
- ✅ Remover um livro
- ✅ Buscar livros por autor

### 2. Importação/Exportação
- ✅ Exportar dados para CSV
- ✅ Importar dados de CSV

### 3. Backup e Segurança
- ✅ Backup automático antes de modificações
- ✅ Backup manual
- ✅ Limpeza automática (mantém apenas 5 backups)

### 4. Validação de Dados
- ✅ Validação de título (não vazio, máximo 200 caracteres)
- ✅ Validação de autor (não vazio, máximo 100 caracteres)
- ✅ Validação de ano (entre 1000 e ano atual + 1)
- ✅ Validação de preço (número positivo, formato brasileiro aceito)

## Como Executar

### Passo 1: Verificar Python
Certifique-se de ter Python 3.6 ou superior instalado:
```bash
python --version
```

### Passo 2: Executar o Sistema
Navegue até o diretório do projeto e execute:

#### Opção 1: Arquivo principal (recomendado)
```bash
python main.py
```

#### Opção 2: Sistema completo
```bash
python sistema_livraria.py
```

#### Opção 3: Demonstração com dados de exemplo
```bash
python demo.py
```
Este script irá popular o banco com 15 livros clássicos brasileiros para demonstração.

### Passo 3: Usar o Sistema
Siga o menu interativo com 9 opções disponíveis.

## Requisitos

- Python 3.6 ou superior
- Bibliotecas padrão do Python:
  - sqlite3
  - csv
  - os
  - pathlib
  - shutil
  - datetime
  - typing

## Menu do Sistema

Ao executar o sistema, você verá o seguinte menu:

```
1. Adicionar novo livro
2. Exibir todos os livros
3. Atualizar preço de um livro
4. Remover um livro
5. Buscar livros por autor
6. Exportar dados para CSV
7. Importar dados de CSV
8. Fazer backup do banco de dados
9. Sair
```

## Características Especiais

### Backup Automático
- Backup é criado automaticamente antes de qualquer modificação (adicionar, atualizar, remover)
- Sistema mantém apenas os 5 backups mais recentes
- Backups são nomeados com timestamp: `backup_livraria_YYYY-MM-DD_HH-MM-SS.db`

### Validação Robusta
- Campos obrigatórios não podem estar vazios
- Preços podem ser inseridos no formato brasileiro (vírgula) ou internacional (ponto)
- Anos devem estar em faixa realista
- Títulos e autores têm limites de caracteres para manter a organização

### Importação CSV
- Sistema mostra preview dos dados antes de importar
- Continua importação mesmo se alguns registros tiverem erro
- Relatório final mostra quantos foram importados com sucesso

### Interface Amigável
- Mensagens claras de sucesso e erro
- Confirmação para operações destrutivas
- Formatação organizada das listagens
- Truncamento inteligente de textos longos

## Exemplos de Uso

### Adicionar um Livro
```
Título do livro: Dom Casmurro
Autor: Machado de Assis
Ano de publicação: 1899
Preço (R$): 29,90
```

### Formato CSV para Importação
O arquivo CSV deve ter o seguinte formato:
```csv
ID,Título,Autor,Ano de Publicação,Preço
1,Dom Casmurro,Machado de Assis,1899,29.90
2,O Cortiço,Aluísio Azevedo,1890,25.50
```

## Tratamento de Erros

O sistema possui tratamento robusto de erros:
- Validação de dados de entrada
- Verificação de existência de arquivos
- Tratamento de erros de banco de dados
- Recuperação graciosa de erros

## Autor

Sistema desenvolvido para demonstrar conceitos de:
- Programação orientada a objetos
- Manipulação de banco de dados
- Gerenciamento de arquivos
- Validação de dados
- Interface de usuário em linha de comando