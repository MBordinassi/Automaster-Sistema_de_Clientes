import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class Cliente:
    def __init__(self, nome: str, telefone: str, cidade: str, placa: str, 
                 cor: str, modelo: str, servico: str, data_entrada: str = None):
        self.nome = nome
        self.telefone = telefone
        self.cidade = cidade
        self.placa = placa.upper()  # Placa sempre em maiúsculo
        self.cor = cor
        self.modelo = modelo
        self.servico = servico
        self.data_entrada = data_entrada or datetime.now().strftime("%d/%m/%Y")
    
    def to_dict(self) -> Dict:
        """Converte o cliente para dicionário"""
        return {
            'nome': self.nome,
            'telefone': self.telefone,
            'cidade': self.cidade,
            'placa': self.placa,
            'cor': self.cor,
            'modelo': self.modelo,
            'servico': self.servico,
            'data_entrada': self.data_entrada
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Cliente':
        """Cria um cliente a partir de um dicionário"""
        return cls(
            nome=data['nome'],
            telefone=data['telefone'],
            cidade=data['cidade'],
            placa=data['placa'],
            cor=data['cor'],
            modelo=data['modelo'],
            servico=data['servico'],
            data_entrada=data['data_entrada']
        )

class GerenciadorClientes:
    def __init__(self, arquivo_dados: str = "clientes.json"):
        self.arquivo_dados = arquivo_dados
        self.clientes: List[Cliente] = []
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega os dados do arquivo JSON"""
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.clientes = [Cliente.from_dict(cliente_data) for cliente_data in dados]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Erro ao carregar dados: {e}")
                self.clientes = []
        else:
            self.clientes = []
    
    def salvar_dados(self):
        """Salva os dados no arquivo JSON"""
        try:
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                dados = [cliente.to_dict() for cliente in self.clientes]
                json.dump(dados, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False
    
    def adicionar_cliente(self, cliente: Cliente) -> bool:
        """Adiciona um novo cliente"""
        # Verifica se já existe cliente com a mesma placa
        if any(c.placa == cliente.placa for c in self.clientes):
            return False
        
        self.clientes.append(cliente)
        return self.salvar_dados()
    
    def editar_cliente(self, indice: int, cliente_atualizado: Cliente) -> bool:
        """Edita um cliente existente"""
        if 0 <= indice < len(self.clientes):
            # Verifica se a nova placa não conflita com outros clientes
            placa_original = self.clientes[indice].placa
            if (cliente_atualizado.placa != placa_original and 
                any(c.placa == cliente_atualizado.placa for c in self.clientes)):
                return False
            
            self.clientes[indice] = cliente_atualizado
            return self.salvar_dados()
        return False
    
    def remover_cliente(self, indice: int) -> bool:
        """Remove um cliente"""
        if 0 <= indice < len(self.clientes):
            del self.clientes[indice]
            return self.salvar_dados()
        return False
    
    def buscar_cliente(self, termo: str) -> List[tuple]:
        """Busca clientes por nome, placa ou telefone"""
        resultados = []
        termo = termo.lower()
        
        for i, cliente in enumerate(self.clientes):
            if (termo in cliente.nome.lower() or 
                termo in cliente.placa.lower() or 
                termo in cliente.telefone):
                resultados.append((i, cliente))
        
        return resultados
    
    def obter_todos_clientes(self) -> List[tuple]:
        """Retorna todos os clientes com seus índices"""
        return [(i, cliente) for i, cliente in enumerate(self.clientes)]