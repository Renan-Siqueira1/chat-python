# Importando as bibliotecas
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# Funções
# Função inicial: Fica sempre de olho se há alguém novo conectando ao servidor.
def inicial():
    while True:
        client, endereco = SERVIDOR.accept()
        print("%s:%s se conectou ao chat." % endereco)
        client.send(bytes("Qual o seu nome ?", "utf8"))
        enderecos[client] = endereco
        Thread(target=handle, args=(client,)).start()


# Função handle: Verifica o nome do usuário para dar boas vindas. Caso não seja boas vindas, a função ficará de olho para verificar se o usuário enviou uma mensagem ou se ele se desconectou
def handle(client):
    nome_cliente = client.recv(1024).decode("utf8")
    client.send(bytes("Bem vindo " + nome_cliente + "!", "utf8"))
    client.send(bytes("Agora você poderá enviar mensagens !", "utf8"))
    mensagem = "%s entrou no chat!" % nome_cliente
    transmissao(bytes(mensagem, "utf8"))
    clientes[client] = nome_cliente

    while True:
        try:
            mensagem = client.recv(1024)
            transmissao(mensagem, nome_cliente + "")
        except:
            client.close()
            del clientes[client]
            transmissao(bytes("%s saiu do chat" % nome_cliente, "utf8"))
            break


# Função transmissão: envia a mensagem para todos os usuários ativos no momento.
def transmissao(mensagem, prefixo=""):
    if prefixo != "":
        prefixo = prefixo + ": "
    for sock in clientes:
        sock.send(bytes(prefixo, "utf8") + mensagem)

clientes = {}
enderecos = {}

# Faz a criação do servidor e inicia a função inicial usando thread
HOST = "127.0.0.1"
PORTA = 59999
ENDERECO = (HOST, int(PORTA))

SERVIDOR = socket(AF_INET, SOCK_STREAM)
SERVIDOR.bind(ENDERECO)

if __name__ == "__main__":
    SERVIDOR.listen(5)
    print("Aguardando novas conexões...")
    ACCEPT_THREAD = Thread(target=inicial)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVIDOR.close()