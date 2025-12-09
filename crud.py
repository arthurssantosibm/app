import sqlite3
import pandas as pd
import customtkinter as ctk
from datetime import date

# ctk
app = ctk.CTk()
app.title('Mostrar Passageiros')
app.geometry('300x300')
ctk.set_appearance_mode('dark')

# sql
con = sqlite3.connect("crud.db")
cur = con.cursor()  # opcional; não é usado abaixo
query = "SELECT * FROM passageiros"
add_sql = "INSERT INTO passageiros (nome, empresa, email, data_cadastro) VALUES (?, ?, ?, ?)"
dados = pd.read_sql_query(query, con)
con.close()  # bom prática: fechar a conexão após o SELECT

# funcao
def showUsers():
    print(dados)
    textbox = ctk.CTkTextbox(app, width=300, height=300)
    textbox.pack(padx=10, pady=10, fill="both", expand=True)
    texto_df = dados.to_string(index=False)
    textbox.insert("0.0", texto_df)
    textbox.configure(state="disabled")


def addUsers():
    show = ctk.CTkToplevel(app)
    show.title('Adicionar Passageiros')
    show.geometry('300x300')
    ctk.set_appearance_mode('dark')
    
    label_add = ctk.CTkLabel(show, text='Nome')
    label_add.pack(pady=10)
    
    campo_user = ctk.CTkEntry(show, placeholder_text='Nome completo')
    campo_user.pack(pady=5)


# passageiros (corrigido: passar 'app' e 'text')
label_passageiros = ctk.CTkLabel(app, text='Passageiros')
label_passageiros.pack(pady=10)

# button
botao = ctk.CTkButton(app, text='Mostrar mais', command=showUsers)
botao.pack(pady=10)

botao_add = ctk.CTkButton(app, text='Adicionar', command=addUsers)
botao_add.pack(pady=10)

app.mainloop()
