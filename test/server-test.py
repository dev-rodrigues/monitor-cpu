import socket, psutil, pickle

# Cria o socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# Obtem o nome da máquina
host = socket.gethostname()                         
porta = 9999
# Associa a porta
socket_servidor.bind((host, porta))
# Escutando...
socket_servidor.listen()
print("Servidor de nome", host, "esperando conexão na porta", porta)
# Aceita alguma conexão
(socket_cliente,addr) = socket_servidor.accept()
print("Conectado a:", str(addr))

while True:
    # Recebe pedido do cliente:
    msg = socket_cliente.recv(10)
    if msg.decode('ascii') == 'fim':
        break
    # Gera a lista de resposta
    resposta = []
    resposta.append(psutil.cpu_percent())
    mem = psutil.virtual_memory()
    mem_percent = mem.used/mem.total
    resposta.append(mem_percent)
    # Prepara a lista para o envio
    bytes_resp = pickle.dumps(resposta)
    # Envia os dados
    socket_cliente.send(bytes_resp)

# Fecha socket do servidor e cliente
socket_cliente.close()
socket_servidor.close()