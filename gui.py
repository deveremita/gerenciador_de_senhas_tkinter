import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import Database
import ctypes

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerenciador de Senhas")
        self.master.iconbitmap("./resources/cadeado.ico")
        
        self.db = Database()
        style = ttk.Style()
        
        style.configure("TLabel", foreground="black", font=("Helvetica", 18, "bold"))
        style.configure("TEntry", font=("Helvetica", 12), padding=5)
        style.configure("TButton", font=("Helvetica", 12), padding=5)

        self.senha_label = ttk.Label(self.master, text="Senha Mestra:", style="TLabel")
        self.senha_label.pack(pady=10)

        self.senha_entry = ttk.Entry(self.master, show="*", style="TEntry")
        self.senha_entry.pack(pady=10)

        self.entrar_button = ttk.Button(self.master, text="Entrar", command=self.validar_senha_mestra, style="TButton")
        self.entrar_button.pack(pady=10)
        self.definir_icone_barra_tarefas()

    def validar_senha_mestra(self):
        senha_digitada = self.senha_entry.get()
        if self.db.validate_master_password(senha_digitada):
            self.master.iconify()
            self.mostrar_senhas()
        else:
            messagebox.showerror("Erro", "Senha mestra incorreta!")

    def mostrar_senhas(self):
        senhas = self.db.get_activities_and_passwords()

        nova_janela = tk.Toplevel(self.master)
        nova_janela.title("Gerenciador de Senhas")
        nova_janela.iconbitmap("./resources/cadeado.ico")

        # Configurando o Notebook
        accordion = ttk.Notebook(nova_janela)
        accordion.pack(expand=True, fill="both")
        self.definir_icone_barra_tarefas()
        for atividade, data in senhas.items():
            passwords = data['senhas']

            tab_frame = ttk.Frame(accordion)
            accordion.add(tab_frame, text=atividade)

            text_widget = tk.Text(tab_frame, wrap=tk.WORD)
            text_widget.pack(expand=True, fill="both", side=tk.LEFT)

            scrollbar = tk.Scrollbar(tab_frame, command=text_widget.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            text_widget.config(yscrollcommand=scrollbar.set)

            text_content = f"{atividade}:\n\n"
            for senha in passwords:
                label_text = f"Nome: {senha[1]}\nE-mail: {senha[2]}\nSenha: {senha[3]}"
                if senha[4]:
                    label_text += f"\nOutros acessos: {senha[4]}"
                text_content += f"{label_text}\n\n"

            text_widget.insert(tk.END, text_content)

        nova_janela.protocol("WM_DELETE_WINDOW", lambda: self.fechar_nova_janela(nova_janela))

        nova_janela.mainloop()
        
    def definir_icone_barra_tarefas(self):
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Gerenciador de Senhas")
        except Exception as e:
            print(f"Erro ao definir ícone na barra de tarefas: {e}")
    
    def fechar_nova_janela(self, nova_janela):
        nova_janela.destroy()

# Exemplo de uso
root = tk.Tk()
app = GUI(root)
root.mainloop()