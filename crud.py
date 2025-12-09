
import sqlite3
import pandas as pd
import customtkinter as ctk
from datetime import date

# ctk
ctk.set_appearance_mode('dark')  # defina uma vez
app = ctk.CTk()
app.title('Mostrar Passageiros')
app.geometry('300x300')

# --- Funções utilitárias de BD ---
DB_PATH = "crud.db"

def ensure_schema():
    """Cria a tabela 'passageiros' se não existir."""
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS passageiros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                empresa TEXT NOT NULL,
                email TEXT UNIQUE,
                data_cadastro TEXT DEFAULT (DATE('now'))
            );
        """)
        con.commit()
    finally:
        con.close()

def insert_seed_data():
    """Insere alguns registros de exemplo (só se quiser popular)."""
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        # Para evitar erro de UNIQUE, só insere se a tabela estiver vazia
        cur.execute("SELECT COUNT(*) FROM passageiros;")
        count = cur.fetchone()[0]
        if count == 0:
            cur.executescript("""
                INSERT INTO passageiros (nome, empresa, email, data_cadastro) VALUES
                    ('Simão Pedro', 'IBM', 'simao@ibm.com', '2025-12-09'),
                    ('André', 'IBM', 'andre@ibm.com', '2025-12-09'),
                    ('Tiago, filho de Zebedeu', 'IBM', 'tiago.zebedeu@ibm.com', '2025-12-09'),
                    ('João', 'IBM', 'joao@ibm.com', '2025-12-09'),
                    ('Filipe', 'IBM', 'filipe@ibm.com', '2025-12-09'),
                    ('Bartolomeu (Natanael)', 'IBM', 'bartolomeu@ibm.com', '2025-12-09'),
                    ('Mateus (Levi)', 'IBM', 'mateus@ibm.com', '2025-12-09'),
                    ('Tomé', 'IBM', 'tome@ibm.com', '2025-12-09'),
                    ('Tiago, filho de Alfeu', 'IBM', 'tiago.alfeu@ibm.com', '2025-12-09'),
                    ('Tadeu (Judas, filho de Tiago)', 'IBM', 'tadeu@ibm.com', '2025-12-09'),
                    ('Simão, o Zelote', 'IBM', 'simao.zelote@ibm.com', '2025-12-09'),
                    ('Judas Iscariotes', 'IBM', 'judas@ibm.com', '2025-12-09');
            """)
            con.commit()
    finally:
        con.close()

def load_passageiros():
    """Retorna um DataFrame atualizado de passageiros."""
    con = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM passageiros", con)
        return df
    finally:
        con.close()

# --- Inicialização do BD (ordem correta) ---
ensure_schema()
insert_seed_data()

# Carrega dados iniciais (opcional; a função showUsers também recarrega)
dados = load_passageiros()

# --- Funções da UI ---
def showUsers():
    """Abre uma nova janela com os passageiros (lendo do BD na hora)."""
    df = load_passageiros()  # ler atualizado
    win = ctk.CTkToplevel(app)
    win.title('Passageiros')
    win.geometry('500x400')

    textbox = ctk.CTkTextbox(win, width=480, height=320)
    textbox.pack(padx=10, pady=10, fill="both", expand=True)
    texto_df = df.to_string(index=False)
    textbox.insert("0.0", texto_df)
    textbox.configure(state="disabled")

    btn_close = ctk.CTkButton(win, text="Fechar", command=win.destroy)
    btn_close.pack(pady=8)

def addUsers():
    """Janela para adicionar um passageiro (layout básico)."""
    show = ctk.CTkToplevel(app)
    show.title('Adicionar Passageiros')
    show.geometry('300x300')

    label_nome = ctk.CTkLabel(show, text='Nome')
    label_nome.pack(pady=6)
    entry_nome = ctk.CTkEntry(show, placeholder_text='Nome completo')
    entry_nome.pack(pady=6)

    label_empresa = ctk.CTkLabel(show, text='Empresa')
    label_empresa.pack(pady=6)
    entry_empresa = ctk.CTkEntry(show, placeholder_text='Empresa')
    entry_empresa.pack(pady=6)

    label_email = ctk.CTkLabel(show, text='Email')
    label_email.pack(pady=6)
    entry_email = ctk.CTkEntry(show, placeholder_text='email@ibm.com')
    entry_email.pack(pady=6)

    def salvar():
        nome = entry_nome.get().strip()
        empresa = entry_empresa.get().strip()
        email = entry_email.get().strip()
        if not nome or not empresa or not email:
            ctk.CTkMessagebox(title="Atenção", message="Preencha todos os campos.", icon="warning")
            return
        # Inserir no BD
        con = sqlite3.connect(DB_PATH)
        try:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO passageiros (nome, empresa, email, data_cadastro) VALUES (?, ?, ?, ?)",
                (nome, empresa, email, date.today().isoformat())
            )
            con.commit()
            ctk.CTkMessagebox(title="OK", message="Passageiro adicionado.", icon="check")
        except sqlite3.IntegrityError as e:
            ctk.CTkMessagebox(title="Erro", message=f"Email duplicado ou dados inválidos:\n{e}", icon="cancel")
        finally:
            con.close()

    btn_salvar = ctk.CTkButton(show, text="Salvar", command=salvar)
    btn_salvar.pack(pady=10)

# --- UI principal ---
label_passageiros = ctk.CTkLabel(app, text='Passageiros')
label_passageiros.pack(pady=10)

botao = ctk.CTkButton(app, text='Mostrar mais', command=showUsers)
botao.pack(pady=10)

botao_add = ctk.CTkButton(app, text='Adicionar', command=addUsers)
botao_add.pack(pady=10)

app.mainloop()
