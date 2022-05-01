# Importando as bibliotecas
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# Funções
# Função inicial: Fica sempre de olho se há alguém novo conectando ao servidor.
def inicial():
    while True:
        client, endereco = SERVER.accept()
        print("%s:%s está online." % endereco)
        client.send(bytes("Qual o seu nome ?", "utf8"))
        addresses[client] = endereco
        Thread(target=handle, args=(client,)).start()


# Função handle: Verifica o nome do usuário para dar boas vindas. Caso não seja boas vindas, a função ficará de olho para verificar se o usuário enviou uma mensagem ou se ele se desconectou
def handle(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = "Bem vindo "
    client.send(bytes(welcome + name + "!", "utf8"))
    client.send(bytes("Agora você poderá enviar mensagens !", "utf8"))
    msg = "%s entrou no chat!" % name
    transmissao(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        try:
            msg = client.recv(BUFSIZ)
            transmissao(msg, name + "")
        except:
            client.close()
            del clients[client]
            transmissao(bytes("%s saiu do chat" % name, "utf8"))
            break


# Função transmissão: envia a mensagem para todos os usuários ativos no momento.
def transmissao(msg, prefix=""):
    if prefix != "":
        prefix = prefix + ": "
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}


# Faz a criação do servidor e inicia a função inicial usando thread
HOST = "26.177.236.7"
PORT = 55555
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Aguardando conexões...")
    ACCEPT_THREAD = Thread(target=inicial)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()
