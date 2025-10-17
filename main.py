import tkinter as tk
from tkinter import ttk, messagebox
from Program.cliente import Cliente, GerenciadorClientes
import re

class ModernOficinaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoMaster - Sistema de Controle")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Configurar tema moderno
        self.setup_styles()
        
        # Inicializa o gerenciador de clientes
        self.gerenciador = GerenciadorClientes()
        
        # Cliente selecionado para edição
        self.cliente_selecionado = None
        self.indice_selecionado = -1
        
        self.criar_interface()
        self.atualizar_lista()
    
    def setup_styles(self):
        """Configura estilos modernos para a aplicação"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores modernas
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'dark': '#2c3e50',
            'light': '#ecf0f1',
            'gray': '#bdc3c7',
            'success': '#27ae60'
        }
        
        # Configurar estilos
        style.configure('Modern.TFrame', background=self.colors['light'])
        style.configure('Card.TFrame', background='white', relief='solid', borderwidth=0)
        style.configure('Title.TLabel', background=self.colors['dark'], foreground='white', font=('Arial', 18, 'bold'))
        style.configure('Section.TLabel', background='white', foreground=self.colors['dark'], font=('Arial', 12, 'bold'))
        
        # Botões modernos
        style.configure('Primary.TButton', background=self.colors['primary'], foreground='white', 
                       borderwidth=0, focuscolor='none', font=('Arial', 10, 'bold'))
        style.map('Primary.TButton', 
                 background=[('active', '#2980b9'), ('pressed', '#21618c')])
        
        style.configure('Success.TButton', background=self.colors['success'], foreground='white',
                       borderwidth=0, focuscolor='none', font=('Arial', 10, 'bold'))
        style.map('Success.TButton',
                 background=[('active', '#229954'), ('pressed', '#1e8449')])
        
        style.configure('Danger.TButton', background=self.colors['danger'], foreground='white',
                       borderwidth=0, focuscolor='none', font=('Arial', 10, 'bold'))
        style.map('Danger.TButton',
                 background=[('active', '#cb4335'), ('pressed', '#a93226')])
        
        # Treeview moderno
        style.configure('Modern.Treeview', 
                       background='white',
                       fieldbackground='white',
                       foreground=self.colors['dark'],
                       rowheight=25,
                       font=('Arial', 10))
        
        style.configure('Modern.Treeview.Heading', 
                       background=self.colors['primary'],
                       foreground='white',
                       relief='flat',
                       font=('Arial', 11, 'bold'))
        
        style.map('Modern.Treeview.Heading',
                 background=[('active', self.colors['primary'])])
    
    def formatar_telefone(self, event=None):
        """Formata o telefone automaticamente durante a digitação"""
        entry = self.entries['telefone']
        texto = entry.get().replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
        
        # Remove qualquer caractere não numérico, exceto o +
        texto = ''.join(filter(str.isdigit, texto))
        
        if len(texto) == 0:
            entry.delete(0, tk.END)
            return
        
        # Limita a 11 dígitos (DDD + 9 dígitos)
        if len(texto) > 11:
            texto = texto[:11]
        
        # Formatação baseada no tamanho
        if len(texto) <= 2:
            formato = f"({texto}"
        elif len(texto) <= 7:
            formato = f"({texto[:2]}) {texto[2:]}"
        elif len(texto) <= 11:
            formato = f"({texto[:2]}) {texto[2:7]}-{texto[7:]}"
        else:
            formato = f"({texto[:2]}) {texto[2:7]}-{texto[7:11]}"
        
        # Atualiza o campo sem trigger recursivo
        entry.unbind('<KeyRelease>')
        entry.delete(0, tk.END)
        entry.insert(0, formato)
        entry.bind('<KeyRelease>', self.formatar_telefone)
        
        # Posiciona o cursor no final
        entry.icursor(tk.END)
    
    def validar_tecla_telefone(self, event):
        """Valida as teclas pressionadas no campo de telefone"""
        # Permite: números, backspace, delete, tab, setas
        if event.keysym in ['BackSpace', 'Delete', 'Tab', 'Left', 'Right', 'Home', 'End']:
            return
        
        # Permite Ctrl+A (selecionar tudo), Ctrl+C, Ctrl+V, Ctrl+X
        if event.state & 0x4 and event.keysym in ['a', 'c', 'v', 'x']:
            return
        
        # Se não for número, impede a digitação
        if not event.char.isdigit():
            return "break"
    
    def criar_interface(self):
        # Header
        self.criar_header()
        
        # Frame principal
        main_frame = ttk.Frame(self.root, style='Modern.TFrame', padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid responsivo
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Frame do formulário
        self.criar_formulario(main_frame)
        
        # Frame da lista de clientes
        self.criar_lista_clientes(main_frame)
    
    def criar_header(self):
        """Cria o cabeçalho moderno"""
        header_frame = ttk.Frame(self.root, style='Title.TLabel')
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = ttk.Label(header_frame, 
                               text="🏠 AutoMaster - Controle de Clientes", 
                               style='Title.TLabel',
                               padding=(20, 15))
        title_label.pack(side=tk.LEFT)
        
        # Estatísticas rápidas
        stats_frame = ttk.Frame(header_frame, style='Title.TLabel')
        stats_frame.pack(side=tk.RIGHT, padx=20)
        
        self.stats_label = ttk.Label(stats_frame, 
                                    text="Clientes: 0", 
                                    style='Title.TLabel',
                                    font=('Arial', 12))
        self.stats_label.pack(side=tk.RIGHT, padx=10)
    
    def criar_formulario(self, parent):
        # Frame do formulário com aparência de card
        form_frame = ttk.Frame(parent, style='Card.TFrame', padding="25")
        form_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 15))
        
        # Título da seção
        title = ttk.Label(form_frame, text="📝 Cadastro de Cliente", style='Section.TLabel')
        title.pack(anchor=tk.W, pady=(0, 20))
        
        # Campos do formulário com labels modernos
        campos = [
            ("👤 Nome do Cliente:", "nome"),
            ("📅 Data de Entrada:", "data_entrada"),
            ("📞 Telefone:", "telefone"),
            ("🏙️ Cidade:", "cidade"),
            ("🚗 Placa do Veículo:", "placa"),
            ("🎨 Cor do Veículo:", "cor"),
            ("🚙 Modelo do Veículo:", "modelo"),
            ("🔧 Serviço Prestado:", "servico")
        ]
        
        self.entries = {}
        
        for i, (label, campo) in enumerate(campos):
            # Frame para cada campo
            field_frame = ttk.Frame(form_frame, style='Card.TFrame')
            field_frame.pack(fill=tk.X, pady=8)
            
            # Label estilizada
            lbl = ttk.Label(field_frame, text=label, style='Section.TLabel',
                           font=('Arial', 10), foreground='#555555')
            lbl.pack(anchor=tk.W, pady=(0, 5))
            
            if campo == "data_entrada":
                from datetime import datetime
                entry = ttk.Entry(field_frame, width=30, font=('Arial', 11))
                entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
            elif campo == "servico":
                entry = ttk.Combobox(field_frame, width=28, font=('Arial', 11),
                                   values=[
                    "Troca de óleo", "Revisão geral", "Freios", "Suspensão",
                    "Motor", "Transmissão", "Ar condicionado", "Elétrica",
                    "Pintura", "Funilaria", "Pneus", "Outros"
                ])
                entry.set("Selecione o serviço")
            elif campo == "telefone":
                # Campo de telefone com formatação automática
                entry = ttk.Entry(field_frame, width=30, font=('Arial', 11))
                # Bind events para formatação
                entry.bind('<KeyRelease>', self.formatar_telefone)
                entry.bind('<KeyPress>', self.validar_tecla_telefone)
                # Tooltip de ajuda
                self.criar_tooltip(entry, "Digite o telefone com DDD. Ex: 11999999999")
            else:
                entry = ttk.Entry(field_frame, width=30, font=('Arial', 11))
            
            entry.pack(fill=tk.X, pady=2)
            self.entries[campo] = entry
        
        # Frame dos botões com espaçamento moderno
        btn_frame = ttk.Frame(form_frame, style='Card.TFrame')
        btn_frame.pack(fill=tk.X, pady=25)
        
        # Botões principais
        ttk.Button(btn_frame, text="✅ Adicionar Cliente", 
                  command=self.adicionar_cliente, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✏️ Atualizar Cliente", 
                  command=self.atualizar_cliente, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🧹 Limpar Campos", 
                  command=self.limpar_campos, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
    
    def criar_tooltip(self, widget, text):
        """Cria um tooltip para o widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(tooltip, text=text, background="#ffffe0", 
                            relief='solid', borderwidth=1, padding=(5, 2))
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def criar_lista_clientes(self, parent):
        # Frame da lista com aparência de card
        list_frame = ttk.Frame(parent, style='Card.TFrame', padding="25")
        list_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        
        # Cabeçalho da lista
        header_frame = ttk.Frame(list_frame, style='Card.TFrame')
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        title = ttk.Label(header_frame, text="📋 Lista de Clientes", style='Section.TLabel')
        title.pack(side=tk.LEFT)
        
        # Frame de busca moderno
        search_frame = ttk.Frame(header_frame, style='Card.TFrame')
        search_frame.pack(side=tk.RIGHT)
        
        ttk.Label(search_frame, text="🔍 Buscar:", style='Section.TLabel',
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.buscar_clientes)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, 
                                width=20, font=('Arial', 11))
        search_entry.pack(side=tk.LEFT)
        
        # Treeview moderna
        columns = ('Nome', 'Data', 'Telefone', 'Cidade', 'Placa', 'Cor', 'Modelo', 'Serviço')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', 
                                height=18, style='Modern.Treeview')
        
        # Configurar colunas com larguras otimizadas
        column_widths = [140, 90, 110, 110, 90, 80, 120, 130]
        for i, (col, width) in enumerate(zip(columns, column_widths)):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, minwidth=60)
        
        # Scrollbars modernas
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid da treeview e scrollbars
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        # Bind para seleção
        self.tree.bind('<<TreeviewSelect>>', self.selecionar_cliente)
        
        # Frame dos botões de ação
        action_frame = ttk.Frame(list_frame, style='Card.TFrame')
        action_frame.grid(row=3, column=0, pady=15)
        
        ttk.Button(action_frame, text="✏️ Editar Selecionado", 
                  command=self.editar_cliente, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="🗑️ Excluir Selecionado", 
                  command=self.excluir_cliente, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="🔄 Atualizar Lista", 
                  command=self.atualizar_lista, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
    
    def atualizar_estatisticas(self):
        """Atualiza as estatísticas no header"""
        total_clientes = len(self.gerenciador.clientes)
        self.stats_label.config(text=f"Clientes: {total_clientes}")
    
    def validar_campos(self):
        """Valida os campos do formulário"""
        erros = []
        
        campos_obrigatorios = ['nome', 'telefone', 'cidade', 'placa', 'modelo', 'servico']
        for campo in campos_obrigatorios:
            if not self.entries[campo].get().strip():
                erros.append(f"O campo {campo.replace('_', ' ').title()} é obrigatório")
        
        data = self.entries['data_entrada'].get().strip()
        if data and not re.match(r'\d{2}/\d{2}/\d{4}', data):
            erros.append("Data deve estar no formato DD/MM/AAAA")
        
        placa = self.entries['placa'].get().strip().upper()
        if placa and not re.match(r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$', placa):
            erros.append("Placa deve estar no formato ABC1234 ou ABC1D23")
        
        telefone = self.entries['telefone'].get().strip()
        # Remove formatação para validar
        telefone_limpo = telefone.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
        if telefone_limpo and not re.match(r'^\d{10,11}$', telefone_limpo):
            erros.append("Telefone deve ter 10 ou 11 dígitos (com DDD)")
        
        return erros
    
    def adicionar_cliente(self):
        """Adiciona um novo cliente"""
        erros = self.validar_campos()
        if erros:
            messagebox.showerror("Erro de Validação", "\n".join(erros))
            return
        
        try:
            # Pega o telefone já formatado automaticamente
            telefone = self.entries['telefone'].get().strip()
            
            cliente = Cliente(
                nome=self.entries['nome'].get().strip(),
                telefone=telefone,  # Já vem formatado
                cidade=self.entries['cidade'].get().strip(),
                placa=self.entries['placa'].get().strip(),
                cor=self.entries['cor'].get().strip(),
                modelo=self.entries['modelo'].get().strip(),
                servico=self.entries['servico'].get().strip(),
                data_entrada=self.entries['data_entrada'].get().strip()
            )
            
            if self.gerenciador.adicionar_cliente(cliente):
                messagebox.showinfo("Sucesso", "✅ Cliente adicionado com sucesso!")
                self.limpar_campos()
                self.atualizar_lista()
                self.atualizar_estatisticas()
            else:
                messagebox.showerror("Erro", "❌ Já existe um cliente com esta placa!")
        
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Erro ao adicionar cliente: {str(e)}")
    
    def atualizar_cliente(self):
        """Atualiza o cliente selecionado"""
        if self.indice_selecionado == -1:
            messagebox.showwarning("Aviso", "⚠️ Selecione um cliente para atualizar!")
            return
        
        erros = self.validar_campos()
        if erros:
            messagebox.showerror("Erro de Validação", "\n".join(erros))
            return
        
        try:
            telefone = self.entries['telefone'].get().strip()
            
            cliente_atualizado = Cliente(
                nome=self.entries['nome'].get().strip(),
                telefone=telefone,
                cidade=self.entries['cidade'].get().strip(),
                placa=self.entries['placa'].get().strip(),
                cor=self.entries['cor'].get().strip(),
                modelo=self.entries['modelo'].get().strip(),
                servico=self.entries['servico'].get().strip(),
                data_entrada=self.entries['data_entrada'].get().strip()
            )
            
            if self.gerenciador.editar_cliente(self.indice_selecionado, cliente_atualizado):
                messagebox.showinfo("Sucesso", "✅ Cliente atualizado com sucesso!")
                self.limpar_campos()
                self.atualizar_lista()
                self.atualizar_estatisticas()
                self.indice_selecionado = -1
            else:
                messagebox.showerror("Erro", "❌ Erro ao atualizar cliente ou placa já existe!")
        
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Erro ao atualizar cliente: {str(e)}")
    
    def selecionar_cliente(self, event):
        """Seleciona um cliente da lista"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            nome = values[0]
            placa = values[4]
            
            for i, cliente in enumerate(self.gerenciador.clientes):
                if cliente.nome == nome and cliente.placa == placa:
                    self.indice_selecionado = i
                    self.cliente_selecionado = cliente
                    break
    
    def editar_cliente(self):
        """Carrega os dados do cliente selecionado no formulário"""
        if self.indice_selecionado == -1:
            messagebox.showwarning("Aviso", "⚠️ Selecione um cliente para editar!")
            return
        
        cliente = self.cliente_selecionado
        
        self.entries['nome'].delete(0, tk.END)
        self.entries['nome'].insert(0, cliente.nome)
        
        self.entries['data_entrada'].delete(0, tk.END)
        self.entries['data_entrada'].insert(0, cliente.data_entrada)
        
        # Telefone já vem formatado do banco de dados
        self.entries['telefone'].delete(0, tk.END)
        self.entries['telefone'].insert(0, cliente.telefone)
        
        self.entries['cidade'].delete(0, tk.END)
        self.entries['cidade'].insert(0, cliente.cidade)
        
        self.entries['placa'].delete(0, tk.END)
        self.entries['placa'].insert(0, cliente.placa)
        
        self.entries['cor'].delete(0, tk.END)
        self.entries['cor'].insert(0, cliente.cor)
        
        self.entries['modelo'].delete(0, tk.END)
        self.entries['modelo'].insert(0, cliente.modelo)
        
        self.entries['servico'].delete(0, tk.END)
        self.entries['servico'].insert(0, cliente.servico)
    
    def excluir_cliente(self):
        """Exclui o cliente selecionado"""
        if self.indice_selecionado == -1:
            messagebox.showwarning("Aviso", "⚠️ Selecione um cliente para excluir!")
            return
        
        cliente = self.cliente_selecionado
        resposta = messagebox.askyesno("Confirmar Exclusão", 
                                     f"🗑️ Deseja realmente excluir o cliente {cliente.nome}?")
        
        if resposta:
            if self.gerenciador.remover_cliente(self.indice_selecionado):
                messagebox.showinfo("Sucesso", "✅ Cliente excluído com sucesso!")
                self.limpar_campos()
                self.atualizar_lista()
                self.atualizar_estatisticas()
                self.indice_selecionado = -1
            else:
                messagebox.showerror("Erro", "❌ Erro ao excluir cliente!")
    
    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        for campo, entry in self.entries.items():
            entry.delete(0, tk.END)
            if campo == 'data_entrada':
                from datetime import datetime
                entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
            elif campo == 'servico':
                entry.set("Selecione o serviço")
        
        self.indice_selecionado = -1
        self.cliente_selecionado = None
    
    def buscar_clientes(self, *args):
        """Busca clientes conforme o texto digitado"""
        termo = self.search_var.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if termo:
            resultados = self.gerenciador.buscar_cliente(termo)
            for indice, cliente in resultados:
                self.tree.insert('', 'end', values=(
                    cliente.nome, cliente.data_entrada, cliente.telefone,
                    cliente.cidade, cliente.placa, cliente.cor,
                    cliente.modelo, cliente.servico
                ))
        else:
            self.atualizar_lista()
    
    def atualizar_lista(self):
        """Atualiza a lista de clientes"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for indice, cliente in self.gerenciador.obter_todos_clientes():
            self.tree.insert('', 'end', values=(
                cliente.nome, cliente.data_entrada, cliente.telefone,
                cliente.cidade, cliente.placa, cliente.cor,
                cliente.modelo, cliente.servico
            ))
        
        self.atualizar_estatisticas()

def main():
    root = tk.Tk()
    app = ModernOficinaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()