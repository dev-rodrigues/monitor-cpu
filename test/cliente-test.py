import socket, time, pickle

# Função que imprime a lista formatada
def imprime(l):    
    print(l)

# Cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Tenta se conectar ao servidor
    s.connect((socket.gethostname(), 9999))
    msg = 'processo-2'
    print('{:>8}'.format('%CPU')+'{:>8}'.format('%MEM'))
    for i in range(10):
        # Envia mensagem vazia apenas para indicar a requisição
        s.send(msg.encode('ascii'))
        bytes = s.recv(1024)
        # Converte os bytes para lista
        lista = pickle.loads(bytes)
        imprime(lista)
        time.sleep(100)
except Exception as erro:
    print(str(erro))

# Fecha o socket
s.close()

input("Pressione qualquer tecla para sair...")