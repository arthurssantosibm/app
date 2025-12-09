
import sqlite3
import pandas as pd
import customtkinter as ctk
from tkinter import ttk  # <-- ADICIONE ESTA LINHA
from datetime import date

# ctk
ctk.set_appearance_mode('light')  # defina uma vez
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
        df = pd.read_sql_query("SELECT id, nome, empresa, email, data_cadastro FROM passageiros ORDER BY nome ASC", con)
        return df
    finally:
        con.close()

# --- Inicialização do BD ---
ensure_schema()
insert_seed_data()

# --- Funções da UI ---
def showUsers():
    """Abre uma nova janela com os passageiros em tabela (Treeview com rolagem e estilo)."""
    df = load_passageiros()  # ler atualizado

    win = ctk.CTkToplevel(app)
    win.title('Passageiros')
    win.geometry('800x450')

    container = ctk.CTkFrame(win)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    # Define colunas (se tabela vazia, usa estrutura padrão)
    columns = list(df.columns) if not df.empty else ["id", "nome", "empresa", "email", "data_cadastro"]

    # Cria tabela
    tree = ttk.Treeview(container, columns=columns, show="headings")

    # Cabeçalhos e largura por coluna
    for col in columns:
        tree.heading(col, text=col.upper())
        width = 120
        if col == "id":
            width = 60
        elif col in ("nome", "empresa"):
            width = 180
        elif col == "email":
            width = 240
        elif col == "data_cadastro":
            width = 120
        tree.column(col, width=width, anchor="w")

    # Insere linhas
    if not df.empty:
        for _, row in df.iterrows():
            tree.insert("", "end", values=[row[c] for c in columns])

    # Scrollbars (CustomTkinter) ligadas ao Treeview
    vscroll = ctk.CTkScrollbar(container, orientation="vertical", command=tree.yview)
    vscroll.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vscroll.set)

    hscroll = ctk.CTkScrollbar(container, orientation="horizontal", command=tree.xview)
    hscroll.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=hscroll.set)

    # Posiciona a tabela
    tree.pack(side="left", fill="both", expand=True)

    # ===== Estilo para sensação de “grades” =====
    style = ttk.Style()
    style.theme_use("default")

    # Altura de linha, borda e seleção
    style.configure("Treeview",
                    rowheight=28,
                    borderwidth=1)
    style.map("Treeview",
              background=[("selected", "#1f6aa5")],
              foreground=[("selected", "white")])

    # Cabeçalho mais evidente
    style.configure("Treeview.Heading",
                    font=("Segoe UI", 10, "bold"),
                    relief="groove")

    # Zebra (linhas alternadas)
    for i, item in enumerate(tree.get_children()):
        tree.item(item, tags=("even",) if i % 2 == 0 else ("odd",))
    tree.tag_configure("odd", background="#ffffff")
    tree.tag_configure("even", background="#ffffff")

    # Botão fechar
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
            # Se não tiver CTkMessagebox, use um label ou print
            print("Atenção: Preencha todos os campos.")
            return
        con = sqlite3.connect(DB_PATH)
        try:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO passageiros (nome, empresa, email, data_cadastro) VALUES (?, ?, ?, ?)",
                (nome, empresa, email, date.today().isoformat())
            )
            con.commit()
            print("OK: Passageiro adicionado.")
        except sqlite3.IntegrityError as e:
            print(f"Erro: Email duplicado ou dados inválidos: {e}")
        finally:
            con.close()

    btn_salvar = ctk.CTkButton(show, text="Salvar", command=salvar)
    btn_salvar.pack(pady=10)

# INTERFACE
label_passageiros = ctk.CTkLabel(app, text='Passageiros')
label_passageiros.pack(pady=10)

botao = ctk.CTkButton(app, text='Mostrar mais', command=showUsers)
botao.pack(pady=10)

botao_add = ctk.CTkButton(app, text='Adicionar', command=addUsers)
botao_add.pack(pady=10)

app.mainloop()
