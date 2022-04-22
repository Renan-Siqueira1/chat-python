import threading
import socket

host = input('Escolha o servidor que irá conectar: ')
porta = int(input('Porta do servidor: '))
nick = input('Escolha o seu nome de usuário: ')

usuario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
usuario.connect((host, porta))


def recebendo():
    while True:
        try:
            mensagem = usuario.recv(1024).decode('utf-8')
            if mensagem == 'NICK':
                usuario.send(nick.encode('utf-8'))
            else:
                print(mensagem)
        except:
            print('Ocorreu um erro no programa. Por favor tente novamente mais tarde.')
            usuario.close()
            break


def escrever():
    while True:
        mensagem = f'{nick} : {input("")}'
        usuario.send(mensagem.encode('utf-8'))


recebendo_thread = threading.Thread(target=recebendo)
recebendo_thread.start()

escrevendo_thread = threading.Thread(target=escrever)
escrevendo_thread.start()
