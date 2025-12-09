import sqlite3
import pandas as pd
import customtkinter as ctk
from tkinter import ttk
from datetime import date
from tkinter import ttk, messagebox

# ctk
ctk.set_appearance_mode('light') 
app = ctk.CTk()
app.title('Mostrar Passageiros')
app.geometry('300x300')

DB_PATH = "crud.db"

def ensure_schema():
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

def load_passageiros():
    """Retorna um DataFrame atualizado de passageiros."""
    con = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT id, nome, empresa, email, data_cadastro FROM passageiros ORDER BY nome ASC", con)
        return df
    finally:
        con.close()

ensure_schema()

def showUsers():
    df = load_passageiros()

    win = ctk.CTkToplevel(app)
    win.title('Passageiros')
    win.geometry('800x450')

    container = ctk.CTkFrame(win)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    columns = list(df.columns) if not df.empty else ["id", "nome", "empresa", "email", "data_cadastro"]

    tree = ttk.Treeview(container, columns=columns, show="headings")

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

    if not df.empty:
        for _, row in df.iterrows():
            tree.insert("", "end", values=[row[c] for c in columns])
            
    vscroll = ctk.CTkScrollbar(container, orientation="vertical", command=tree.yview)
    vscroll.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vscroll.set)

    hscroll = ctk.CTkScrollbar(container, orientation="horizontal", command=tree.xview)
    hscroll.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=hscroll.set)

    # Posiciona a tabela
    tree.pack(side="left", fill="both", expand=True)
    
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

def delete_by_id(id_):
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM passageiros WHERE id = ?", (id_,))
        con.commit()
        return cur.rowcount  # 1 se deletou; 0 se não encontrou
    finally:
        con.close()

def deleteUsers():
    df = load_passageiros()
    delete = ctk.CTkToplevel(app)
    delete.title('Remover Passageiros')
    delete.geometry('800x450')
    
    container = ctk.CTkFrame(delete)
    container.pack(fill="both", expand=True, padx=10, pady=10)
    filter_frame = ctk.CTkFrame(container)
    filter_frame.pack(fill='x', padx=0, pady=(0, 8))
    entry_filter = ctk.CTkEntry(filter_frame, width=300, placeholder_text="Filtrar por nome/email...")
    entry_filter.pack(side="left", padx=(0, 8), pady=6)
    btn_apply_filter = ctk.CTkButton(filter_frame, text="Aplicar filtro")
    btn_apply_filter.pack(side="left", pady=6)
    
    columns = ["id", "nome", "empresa", "email", "data_cadastro"]
    tree = ttk.Treeview(container, columns=columns, show="headings", selectmode="browse")

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

    # Scrollbars
    vscroll = ctk.CTkScrollbar(container, orientation="vertical", command=tree.yview)
    vscroll.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vscroll.set)

    hscroll = ctk.CTkScrollbar(container, orientation="horizontal", command=tree.xview)
    hscroll.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=hscroll.set)

    tree.pack(side="left", fill="both", expand=True)

    # --- Estilo mais claro (se quiser manter dark, remova este bloco) ---
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#ffffff",
                    foreground="#000000",
                    fieldbackground="#ffffff",
                    rowheight=26,
                    borderwidth=1)
    style.configure("Treeview.Heading",
                    background="#e6e6e6",
                    foreground="#000000",
                    font=("Segoe UI", 10, "bold"),
                    relief="solid")

    # --- Helpers para popular/refresh ---
    def populate_tree(df: pd.DataFrame):
        tree.delete(*tree.get_children())
        if df.empty:
            return
        for i, (_, row) in enumerate(df.iterrows()):
            tree.insert("", "end", values=[row[c] for c in columns],
                        tags=("even",) if i % 2 == 0 else ("odd",))
        tree.tag_configure("odd", background="#ffffff")   # zebra clara
        tree.tag_configure("even", background="#f2f2f2")

    def reload_data():
        df = load_passageiros()
        populate_tree(df)

    # --- Filtro ---
    def apply_filter():
        term = entry_filter.get().strip().lower()
        df = load_passageiros()
        if term:
            df = df[df.apply(
                lambda r: term in str(r["nome"]).lower() or term in str(r["email"]).lower(),
                axis=1
            )]
        populate_tree(df)

    btn_apply_filter.configure(command=apply_filter)

    # --- Deletar item selecionado ---
    def delete_selected():
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Atenção", "Selecione um passageiro na tabela.")
            return
        values = tree.item(sel[0], "values")
        id_ = values[0]  # primeira coluna é id
        nome = values[1]
        # Confirmação
        if not messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover:\n\nID {id_} — {nome}?"):
            return
        deleted = delete_by_id(id_)
        if deleted:
            messagebox.showinfo("OK", f"Passageiro ID {id_} removido.")
            reload_data()
        else:
            messagebox.showerror("Erro", "Não foi possível remover. Registro não encontrado.")

    # --- Duplo clique também deleta (opcional; pode comentar se achar perigoso) ---
    def on_double_click(event):
        delete_selected()
    tree.bind("<Double-1>", on_double_click)

    # --- Barra inferior com ações ---
    actions = ctk.CTkFrame(delete)
    actions.pack(fill="x", padx=10, pady=(6, 10))

    btn_delete = ctk.CTkButton(actions, text="Deletar selecionado", command=delete_selected)
    btn_delete.pack(side="left", padx=(0, 8), pady=4)

    btn_refresh = ctk.CTkButton(actions, text="Atualizar", command=reload_data)
    btn_refresh.pack(side="left", pady=4)

    btn_close = ctk.CTkButton(actions, text="Fechar", command=delete.destroy)
    btn_close.pack(side="right", pady=4)

    # Carrega inicialmente
    reload_data()
    
# INTERFACE
label_passageiros = ctk.CTkLabel(app, text='Passageiros')
label_passageiros.pack(pady=10)

botao = ctk.CTkButton(app, text='Mostrar mais', command=showUsers)
botao.pack(pady=10)

botao_add = ctk.CTkButton(app, text='Adicionar', command=addUsers)
botao_add.pack(pady=10)

botao_del = ctk.CTkButton(app, text='Remover', command=deleteUsers)
botao_del.pack(pady=10)

app.mainloop()