# Automaster-Sistema_de_controle
Sistema de controle de oficina feito em python (WIP)

# 🏠 AutoMaster - Sistema de Controle de Oficina

Sistema moderno para gerenciamento de clientes e serviços em oficinas mecânicas.

## 📋 Sobre o Projeto

O AutoMaster é uma aplicação desktop desenvolvida em Python com interface Tkinter para controle completo de clientes e serviços em oficinas automotivas.

### ✨ Funcionalidades

- ✅ Cadastro completo de clientes
- 🔍 Sistema de busca em tempo real
- 📱 Formatação automática de telefone
- 🚗 Validação inteligente de placas
- 📊 Listagem organizada
- 💾 Armazenamento em JSON
- 🎨 Interface moderna

## 🛠️ Tecnologias

- Python 3.8+
- Tkinter
- JSON
- Expressões Regulares

## 📦 Estrutura do Projeto

AutoMaster/
├── main.py                 # Aplicação principal
├── cliente.py             # Classe Cliente e Gerenciador
├── clients.json           # Banco de dados
├── requirements.txt       # Dependências
└── README.md             # Documentação

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior

### Instalação
1. Baixe os arquivos do projeto
2. Execute no terminal:
   ```bash
   python main.py

   🎯 Como Usar
Cadastrando Cliente
Preencha o formulário à esquerda

Telefone formata automaticamente: 11999999999 → (11) 99999-9999

Data é preenchida automaticamente

Selecione o serviço na lista

Clique em "Adicionar Cliente"

Editando Cliente
Selecione na lista

Clique em "Editar Selecionado"

Faça alterações

Clique em "Atualizar Cliente"

Buscando
Use o campo "Buscar" para filtrar em tempo real

📄 Campos Obrigatórios
👤 Nome do Cliente

📞 Telefone (com DDD)

🏙️ Cidade

🚗 Placa do Veículo

🚙 Modelo do Veículo

🔧 Serviço Prestado

🎨 Personalização
Cores podem ser personalizadas no código:

Azul principal: #3498db

Verde sucesso: #2ecc71

Vermelho perigo: #e74c3c

📝 Serviços Disponíveis
- Troca de óleo

- Revisão geral

- Freios

- Suspensão

- Motor

- Transmissão

- Ar condicionado

- Elétrica

- Pintura

- Funilaria

- Pneus

- Outros

🔧 Desenvolvimento
Classes Principais
Cliente: Armazena dados do cliente

GerenciadorClientes: Gerencia CRUD e arquivo JSON

ModernOficinaApp: Interface gráfica

Validações
Telefone: (11) 99999-9999

Placa: Formato Mercosul (ABC1D23) ou antigo (ABC1234)

Data: DD/MM/AAAA

💾 Persistência
Dados salvos automaticamente em clients.json:
{
  "clientes": [
    {
      "nome": "João Silva",
      "telefone": "(11) 99999-9999",
      "cidade": "São Paulo",
      "placa": "ABC1234",
      "cor": "Preto",
      "modelo": "Fiat Uno",
      "servico": "Troca de óleo",
      "data_entrada": "15/01/2024"
    }
  ]
}

🐛 Solução de Problemas
Erro comum: ModuleNotFound
Certifique-se de que todos os arquivos estão na mesma pasta:

main.py

cliente.py

clients.json (será criado automaticamente)

Requisitos
Python 3.8+

Tkinter (já vem com Python)

📞 Suporte
Em caso de problemas:

Verifique se todos os arquivos estão na mesma pasta

Certifique-se de ter Python 3.8+

Execute como administrador se necessário
