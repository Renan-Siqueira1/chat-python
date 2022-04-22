import threading
import socket

host = input('Digite o número do servidor que irá hostear a conexão do chat: ')
porta = int(input('Porta do servidor: '))

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, int(porta)))
servidor.listen()

usuarios = []
nicknames = []


def transmissao(mensagem):
    for usuario in usuarios:
        usuario.send(mensagem)


def handle(usuario):
    while True:
        try:
            mensagem = usuario.recv(1024)
            print(usuarios)
            transmissao(mensagem)
        except:
            index = usuarios.index(usuario)
            usuarios.remove(index)
            usuarios.close()
            nickname = nicknames[index]
            transmissao(f'O Usuário {nickname} deixou o chat.'.encode('utf-8'))
            nicknames.remove(nickname)
            print(f"Usuários Ativos no momento: {nicknames}".encode('utf-8'))
            break


def recebendo():
    while True:
        try:
            usuario, endereco = servidor.accept()
            print(f"Conectado com {str(endereco)}")

            usuario.send('NICK'.encode('utf-8'))
            nickname = usuario.recv(1024).decode('utf-8')
            nicknames.append(nickname)
            usuarios.append(usuario)

            print(f"O Nickname do usuário é {nickname}")
            transmissao(f'O Usuário {nickname} entrou no chat.'.encode('utf-8'))
            usuario.send("\nConectado ao servidor".encode('utf-8'))

            thread = threading.Thread(target=handle, args=(usuario,))
            thread.start()
        except:
            print("Ocorreu erro no servidor. Por favor reiniciar")
            break


print('Iniciando o chat TCP/IP')
recebendo()
