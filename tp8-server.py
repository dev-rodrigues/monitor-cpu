import socket, psutil, pickle, cpuinfo, threading, time

# infra servidor
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname()                         
porta = 9999
socket_servidor.bind((host, porta))
socket_servidor.listen()
print("Servidor de nome:", host, " - Aguardando conexão na porta:", porta)
(socket_cliente,addr) = socket_servidor.accept()
print("Conectado a:", str(addr))

# controle aplicacao
variaveis = {
    'cpu': [],
    'memoria': [],
    'disco':[],
    'processo': [],
    'arquivos': []
}

# configuracao processador
info_cpu = cpuinfo.get_cpu_info()
psutil.cpu_percent(interval=1, percpu=True)

# inicio classes
class Host:
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name
        self.ports = []

class Porta:
    def __init__(self, port, state):
        self.port = port
        self.state = state

class Processo:
    def __init__(self, pid, nome, percentual_uso, memoria_usada, threads_processo, tempo_usuario, data_criacao):
        self.pid = pid
        self.nome = nome
        self.percentual_uso = percentual_uso
        self.memoria_usada = memoria_usada
        self.threads_processo = threads_processo
        self.tempo_usuario = tempo_usuario
        self.data_criacao = data_criacao

class CPU():
    def __init__(self, nome, arquitetura, bits, frequencia, nucleos, l_cpu_percent, capacidade, num_cpu):
        self.nome = nome
        self.arquitetura = arquitetura
        self.bits = bits
        self.frequencia = frequencia
        self.nucleos = nucleos
        self.l_cpu_percent = l_cpu_percent
        self.capacidade = capacidade
        self.num_cpu = num_cpu

class Memoria():
    def __init__(self, memoria, capacidade, disponivel):
        self.memoria = memoria
        self.capacidade = capacidade
        self.disponivel = disponivel

class Disco():
    def __init__(self, disco, usado, total, livre):
        self.disco = disco
        self.usado = usado
        self.total = total
        self.livre = livre

class Trafego():
    def __init__(self, interface, enviados, recebidos, pacotes_enviados, pacotes_recebidos):
        self.interface = interface
        self.enviados = enviados
        self.recebidos = recebidos
        self.pacotes_enviados = pacotes_enviados
        self.pacotes_recebidos = pacotes_recebidos
# fim classes

# inicio threads
class ThreadRede(threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter      

   def run(self):
      print ("Starting thread" + self.name)
      #get_hosts()
      print ("Exiting thread" + self.name)

class ThreadArquivos(threading.Thread):

   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter      

   def run(self):
      print ("Starting thread" + self.name)
      #variaveis['execucao_leitura_arquivos'] = get_sched_scheduler_arquivos()
      #print(variaveis['execucao_leitura_arquivos'])
      print ("Exiting thread" + self.name)

class ThreadDisco(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print ("Starting thread" + self.name)
        while True:
            get_info_disco()
            print ("Sleeping..." + self.name)
            time.sleep(20)
# fim threads

# inicia funcoes
def get_info_disco():
    disco = psutil.disk_usage('.')
    usado = round((disco.total - disco.free)  / 1024**3, 2)
    total = round(disco.total / (1024**3), 2)
    livre = round(disco.free/(1024**3),2)

    disco_aux = Disco(disco, usado, total, livre)
    variaveis['disco'].append(disco_aux)
# fim funcoes

# inicia thread
thread_disco = ThreadDisco(1, 'Thread-Disco', 1)
thread_disco.start()
# fim thread


while True:
    
    msg = socket_cliente.recv(10)
    if msg.decode('ascii') == 'fim':
        break

    elif msg.decode('ascii')=='disco':
        total_info_disco = len(variaveis['disco'])
        res
    
    resposta = []
    resposta.append(psutil.cpu_percent())
    mem = psutil.virtual_memory()
    mem_percent = mem.used/mem.total
    resposta.append(mem_percent)
    
    bytes_resp = pickle.dumps(resposta)
    
    socket_cliente.send(bytes_resp)

# Fecha socket do servidor e cliente
socket_cliente.close()
socket_servidor.close()