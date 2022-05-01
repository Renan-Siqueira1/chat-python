# Importando as bibliotecas
import socket
from threading import Thread
from tkinter import *

# Faz a conexão manual do Usuário com o Servidor
HOST = "26.177.236.7"
PORT = 55555
if not PORT:
    PORT = 55555
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

usuario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
usuario.connect(ADDR)


# Funções
# Função receber: fica de olho quando o servidor retorna mensagens para os usuários.
def receber():
    while True:
        try:
            mensagem = usuario.recv(BUFSIZ).decode('utf-8')
            msg_list.insert(END, mensagem)
        except:
            break


# Função enviar: envia a mensagem do usuário ao servidor.
def enviar():
    mensagem = message.get()
    message.set("")
    if mensagem != "":
        usuario.send(bytes(mensagem, "utf8"))
    else:
        msg_list.insert(END, "A Mensagem deve estar preenchida")


# Função quit: quando o usuário clicar em fechar a janela. Ele desliga a conexão do usuário com o servidor.
def quit(event=None):
    usuario.close()
    janela.quit()


# Variaveis de uso TKINTER
# Setando fontes, e cores
defaultFont = ("Roboto", "16", "bold")
secondaryFont = ("Roboto", "14")
bg1 = "#DCDCDC"
bg2 = "#2F4F4F"

# Iniciando a Janela e setando os labels, inputs e grids
janela = Tk()

# Configurações da janela
janela.title('Chat Python Socket')
janela.configure(bg=bg1)
janela.protocol("WM_DELETE_WINDOW", quit)

# Variaveis da Janela
message = StringVar()
messages_frame = Frame(janela)
scrollbar = Scrollbar(messages_frame)

# Box de Mensagens
msg_list = Listbox(janela, height=11, width=38, font=secondaryFont, fg=bg2, border=2, relief="groove", yscrollcommand=scrollbar.set)

# Inputs
input_message = Entry(janela, width=22, font=secondaryFont, fg=bg2, border=2, relief="groove", textvariable=message)
input_message.bind("<Return>", )

# Botões
button_send = Button(janela, text="Enviar", font=secondaryFont, fg=bg2, border=2, relief="groove", command=enviar)

# Grids
scrollbar.grid()
messages_frame.grid()
msg_list.grid(row=1, column=1, columnspan=2)

input_message.grid(row=2, column=1, sticky="w")
button_send.grid(row=2, column=2, sticky="n")

# Divisórias
l_divisoriac = Label(janela, width=1, height=1, bg=bg1)
l_divisorian = Label(janela, width=1, height=1, bg=bg2)
l_divisorias = Label(janela, width=1, height=1, bg=bg2)
l_divisoriae = Label(janela, width=1, height=1, bg=bg2)
l_divisoriaw = Label(janela, width=1, height=1, bg=bg2)

# Grids Divisórias
l_divisoriac.grid(row=8, column=1)
l_divisorian.grid(row=0, column=0, columnspan=3, sticky="e" + "w")
l_divisorias.grid(row=13, column=0, columnspan=3, sticky="e" + "w")
l_divisoriae.grid(row=0, column=0, rowspan=14, sticky="n" + "s")
l_divisoriaw.grid(row=0, column=3, rowspan=14, sticky="n" + "s")

receive_thread = Thread(target=receber)
receive_thread.start()

janela.mainloop()
