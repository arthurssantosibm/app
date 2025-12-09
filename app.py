import customtkinter as ctk

ctk.set_appearance_mode('dark')

#back end
#chamando a funcao la de baixo para validar o login
def validarLogin():
    usuario = campo_usuario.get()
    senha = campo_senha.get()
    
    if usuario == 'arthur' and senha == '123456':
        resultado_login.configure(text='Login feito com sucesso',
                                  text_color='green')
    else:
        resultado_login.configure(text='Tente novamente',
                                  text_color='red')
        
#definindo a variavel global e a tela
app = ctk.CTk()

app.title('Sistema de Login')
app.geometry('300x300')

# campo de usuario (label e entry(mesma coisa do input em php))
label_usuario = ctk.CTkLabel(app,text='Usuário')
label_usuario.pack(pady=10)

campo_usuario = ctk.CTkEntry(app,placeholder_text='Digite seu nome de usuario')
campo_usuario.pack(pady=5)

# campo de senha
label_senha = ctk.CTkLabel(app,text='Senha')
label_senha.pack(pady=10)

campo_senha = ctk.CTkEntry(app,placeholder_text='Digite sua senha',show='*')
campo_senha.pack(pady=5)

#button
botao = ctk.CTkButton(app,text='Login',command=validarLogin)
botao.pack()

#feedback
resultado_login = ctk.CTkLabel(app,text='')
resultado_login.pack(pady=10)

#sempre por ultimo
app.mainloop()