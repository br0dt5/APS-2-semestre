import tkinter
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import criptografia


# Definindo funções
def callEncrypt():
    """
    Verifica o tipo de dado de entrada e chama a função para encriptar os dados. O conteúdo de retorno é armazenado
    na variável 'retorno'.
    """
    global retorno

    # Verifica o tipo de dado, realiza a encriptação e atribui a mensagem de retorno à variável 'retorno'
    if tipo.get() == 'Texto':
        retorno.set(criptografia.encrypt(password=senha.get(), plain_text=s_ent.get('1.0', 'end-1c')))
        btn3.grid()
    else:
        retorno.set(criptografia.encrypt(password=senha.get(), filename=dados.get()))


def callDecrypt():
    """
    Verifica o tipo de dado de entrada e chama a função para encriptar os dados. O conteúdo de retorno é armazenado
    na variável 'retorno'.
    """
    global retorno

    # Verifica o tipo de dado, realiza a decriptação e atribui a mensagem de retorno à variável 'retorno'
    if tipo.get() == 'Texto':
        retorno.set(criptografia.decrypt(password=senha.get(), cipher_text=s_ent.get('1.0', 'end-1c')))
    else:
        retorno.set(criptografia.decrypt(password=senha.get(), filename=dados.get()))


def toggleEntry():
    """
    Controla qual caixa de entrada será mostrado na tela, dependendo da seleção do
    usuário sobre o tipo de entrada de dados
    """
    global s_ent
    global ent1

    # Verifica o tipo de dado e define qual widget é mostrado ou ocultado.
    if tipo.get() == 'Texto':
        ent1.grid_remove()
        s_ent.grid()
    elif tipo.get() == 'Arquivo':
        s_ent.grid_remove()
        ent1.grid()


def copy():
    """
    Copia o conteúdo da variável 'retorno' para a clipboard.
    """
    tk.withdraw()
    tk.clipboard_clear()
    tk.clipboard_append(retorno.get())


tk = tkinter.Tk()

# Características da janela
# 1 - Especifíca o tamanho da janela
w_width = 520
w_height = 180

# 2 - Adquire as medidas da tela do usuário
s_width = tk.winfo_screenwidth()
s_height = tk.winfo_screenheight()

# 3 - Define a posição da janela com base na tela do usuário e o tamanho da janela
x = (s_width / 2) - (w_width / 2)
y = (s_height / 2) - (w_height / 2)

# 4 - Características gerais
tk.title('~Insira um bom título aqui~')
tk.geometry(f'{w_width}x{w_height}+{int(x)}+{int(y)}')
tk.resizable(False, False)

# Variáveis
dados = tkinter.StringVar()
senha = tkinter.StringVar()
tipo = tkinter.StringVar()
tipo.set('Texto')
retorno = tkinter.StringVar()

# Define o estilo dos widgets
style = ttk.Style()
estilo = ('Roboto', 10, 'bold')
style.configure('Label', font=estilo, background='#fdeca6')
style.configure('Label.TButton', font=estilo, background='white')
style.configure('Label.TRadiobutton', font=estilo, background='#fdeca6')

# Widgets
frame = ttk.Frame(tk)
frame.pack(expand=True, fill='both', anchor='center')

image = tkinter.PhotoImage(file="fundo.png")
lblImg = ttk.Label(frame, image=image)
lblImg.place(x=0, y=0)

lbl1 = ttk.Label(frame, text='Dados:', style='Label')
lbl1.grid(row=0, column=0, padx=30, pady=30, sticky='n')

ent1 = ttk.Entry(frame, width=35, textvariable=dados)
ent1.grid(row=0, column=1, pady=20)
ent1.grid_remove()

s_ent = ScrolledText(frame, height=3, width=24, bd=2, relief='groove')
s_ent.grid(row=0, column=1, pady=10)

ttk.Radiobutton(frame,
                text='Texto',
                variable=tipo,
                value='Texto',
                style='Label.TRadiobutton',
                command=toggleEntry).grid(row=0, column=2)

ttk.Radiobutton(frame,
                text='Arquivo',
                variable=tipo,
                value='Arquivo',
                style='Label.TRadiobutton',
                command=toggleEntry).grid(row=0, column=3)

lbl2 = ttk.Label(frame, text='Senha:', style='Label').grid(row=1, column=0, padx=30, sticky='n')
ent2 = ttk.Entry(frame, width=35, show='*', textvariable=senha)
ent2.grid(row=1, column=1)

btn1 = ttk.Button(frame,
                  text='Encriptar',
                  width=10,
                  style='Label.TButton',
                  command=callEncrypt).grid(row=1, column=2, padx=(10, 0))

btn2 = ttk.Button(frame,
                  text='Decriptar',
                  width=10,
                  style='Label.TButton',
                  command=callDecrypt).grid(row=1, column=3, padx=(10, 0))

msg = tkinter.Message(frame, textvariable=retorno, width=250, font=estilo, bg='#fdeca6')
msg.grid(row=2, column=0, columnspan=2, pady=(15, 0))

btn3 = ttk.Button(frame, text='Copiar', style='Label.TButton', command=copy)
btn3.grid(row=2, column=2, columnspan=2, sticky='n', pady=(15, 0))
btn3.grid_remove()

tk.mainloop()
