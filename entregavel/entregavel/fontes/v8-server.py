import socket, psutil, pickle, cpuinfo, threading
import time, sched, os, platform, subprocess
import nmap, math

# controle aplicacao
variaveis = {
    'cpu': [],
    'memoria': [],
    'disco':[],
    'processo': [],
    'arquivos': [],
    'sched':[],
    'ips': [],
    'hosts_detalhado': [],
    'trafego' : [],
    'total_elementos_por_pagina': 5
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

    def to_map(self):
        return { 'pid': self.pid, 'nome' : self.nome, 'percentual_uso' : self.percentual_uso, 'memoria_usada' : self.memoria_usada, 'threads_processo' : self.threads_processo, 'tempo_usuario' : self.tempo_usuario, 'data_criacao' : self.data_criacao }

class Arquivo:
    def __init__(self, nome, tamanho, data_criacao, data_modificacao):
        self.nome = nome
        self.tamanho = tamanho
        self.data_criacao = data_criacao
        self.data_modificacao = data_modificacao
       
    def to_map(self):
        return { 
            'nome': self.nome
        ,   'tamanho': self.tamanho
        ,   'data_criacao': self.data_criacao
        ,   'data_modificacao': self.data_modificacao 
        #,   'diretorio': self.diretorio
    }

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
    
    def to_map(self):
        return { 'nome': self.nome, 'arquitetura': self.arquitetura, 'bits': self.bits, 'frequencia': self.frequencia, 'nucleos': self.nucleos, 'l_cpu_percent': self.l_cpu_percent, 'capacidade': self.capacidade, 'num_cpu': self.num_cpu}

class Memoria():
    def __init__(self, memoria, capacidade, disponivel):
        self.memoria = memoria
        self.capacidade = capacidade
        self.disponivel = disponivel
    
    def get_map(self):
        return { 'memoria': self.memoria, 'capacidade' : self.capacidade, 'disponivel' : self.disponivel}

class Disco():
    def __init__(self, disco, usado, total, livre):
        self.disco = disco
        self.usado = usado
        self.total = total
        self.livre = livre

    def to_map(self):
        return {'disco': self.disco, 'usado': self.usado, 'total': self.total, 'livre': self.livre}

class Trafego():
    def __init__(self, interface, enviados, recebidos, pacotes_enviados, pacotes_recebidos):
        self.interface = interface
        self.enviados = enviados
        self.recebidos = recebidos
        self.pacotes_enviados = pacotes_enviados
        self.pacotes_recebidos = pacotes_recebidos

    def to_map(self):
        return { 'interface' : self.interface, 'enviados': self.enviados, 'recebidos' : self.recebidos, 'pacotes_enviados' : self.pacotes_enviados, 'pacotes_recebidos': self.pacotes_recebidos }

class Resumo():
    def __init__(self, total_processos, memoria_capacidade, memoria_disponivel, cpu, disco):
        self.total_processos = total_processos
        self.memoria_capacidade = memoria_capacidade
        self.memoria_disponivel = memoria_disponivel
        self.ips = []
        self.cpu = cpu
        self.disco = disco

    def to_map(self):
        return { 
            'total_processos': self.total_processos,
            'ips': self.ips,
            'memoria_capacidade' : self.memoria_capacidade, 
            'memoria_disponivel': self.memoria_disponivel, 
            'cpu': self.cpu, 
            'disco': self.disco
        }
# fim classes

# inicio threads
class ThreadIps(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter      

    def run(self):
        while True:
            if len(variaveis['ips']) == 0:
                print ("Starting ThreadIps" + self.name)
                variaveis['ips'] = get_meus_ips()
                print ("Exiting ThreadIps" + self.name)
                time.sleep(30)
            else:
                break

class ThreadRede(threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter      

   def run(self):
       while True:
           print ("Starting scanning rede" + self.name)
           get_hosts()
           print ("Exiting scanning rede" + self.name)
           time.sleep(20)

class ThreadDisco(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    
    def run(self):
        while True:
            print ("Starting thread" + self.name)
            get_info_disco()
            print ("Sleeping..." + self.name)
            time.sleep(20)

class ThreadCpu(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    
    def run(self):
        while True:
            print ("Starting thread" + self.name)
            get_info_cpu()
            print ("Sleeping..." + self.name)
            time.sleep(20)

class ThreadSched(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    
    def run(self):
        while True:
            print ("Starting thread" + self.name)
            get_shed_sheduler_arquivos()
            print ("Sleeping..." + self.name)
            time.sleep(20)

class ThreadTrafegoRede(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    
    def run(self):
        while True:
            print ("Starting thread" + self.name)
            get_trafego_host()
            print ("Sleeping..." + self.name)
            time.sleep(100)

class ThreadMemoria(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    
    def run(self):
        while True:
            print ("Starting thread" + self.name)
            get_info_memoria()
            print ("Sleeping..." + self.name)
            time.sleep(2)

class ThreadProcesso(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    
    def run(self):
        while True:
            print ("Starting thread" + self.name)
            aux = get_processo()
            variaveis['processo'].clear
            variaveis['processo'] = aux
            print ("Sleeping..." + self.name)
            time.sleep(2)

class ThreadCollector(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    
    def run(self):
        while True:
            print ("Starting thread" + self.name)
            clear_cache()
            print ("Sleeping..." + self.name)
            time.sleep(2)
# fim threads

# inicia funcoes
def clear_cache():
    global variaveis
    
    cpu = variaveis['cpu']
    memoria = variaveis['memoria']
    disco = variaveis['disco']

    apply_cleaning(cpu,'[CPU]')
    apply_cleaning(memoria,'[MEM]')
    apply_cleaning(disco,'[DISC]')

def apply_cleaning(list, tag):
    if len(list)>2:
        print('limpando cache -', tag)
        del(list[0])
        del(list[1])

def get_info_disco():
    """ RESPONSAVEL POR OBTER AS INFORMACOES DO DISCO """
    disco = psutil.disk_usage('.')
    usado = round((disco.total - disco.free)  / 1024**3, 2)
    total = round(disco.total / (1024**3), 2)
    livre = round(disco.free/(1024**3),2)

    disco_aux = Disco(disco, usado, total, livre)
    variaveis['disco'].append(disco_aux)

def get_info_cpu():
    """ RESPONSAVEL POR OBTER AS INFORMACOES DA CPU """
    
    nome_cpu = str(info_cpu['brand_raw'])
    arquitetura_cpu = str(info_cpu['arch'])
    bits_cpu = str(info_cpu['bits'])
    frq_cpu = str(info_cpu['hz_actual_friendly'])
    nucleos = str(info_cpu['count'])

    l_cpu_percent = psutil.cpu_percent(percpu=True)
    capacidade = psutil.cpu_percent(interval=1)
    num_cpu = len(l_cpu_percent)

    cpu = CPU(nome_cpu, arquitetura_cpu, bits_cpu, frq_cpu, nucleos, l_cpu_percent, capacidade, num_cpu)
    variaveis['cpu'].append(cpu)

def get_arquivos():
    """ RESPONSAVEL POR OBTER OS ARQUIVOS """
    arquivos = os.listdir()
    diretorio = os.getcwd()

    arquivo_response = []
    for arquivo in arquivos:
        tamanho = os.stat(arquivo).st_size
        criacao = os.stat(arquivo).st_ctime
        modificacao = os.stat(arquivo).st_mtime
        
        arquivo_aux = Arquivo(arquivo, tamanho, criacao, modificacao)
        arquivo_response.append(arquivo_aux.to_map())
        
    variaveis['arquivos'].clear()
    variaveis['arquivos'].append(arquivo_response)

def get_shed_sheduler_arquivos():
    """ RESPONSAVEL POR OBTER TEMPO DA OBTENCAO DE ARQUIVOS """
    inicio = time.time()
    inicioClock = time.process_time()
    sched_ = sched.scheduler(time.time, time.sleep)

    sched_.enter(3, 1, get_arquivos())

    tempoFinal = 'TEMPO FINAL: %s | CLOCK FINAL: %0.2f' % (time.ctime(), time.process_time())

    final = time.time() - inicio
    finalClock = time.process_time() - inicioClock

    tempoUsado = 'TEMPO USADO NESSA CHAMADA: %0.3f segundos | CLOCK USADO NESSA CHAMADA: %0.2f' % (final, finalClock)
    variaveis['sched'].append((tempoFinal, tempoUsado))    

def getNewIp(sistema):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == sistema:
                yield (interface, snic.address, snic.netmask)
                
def get_meus_ips():
    return list(getNewIp(socket.AF_INET))

def retorna_codigo_ping(hostname):
    """Usa o utilitario ping do sistema operacional para encontrar   o host. ('-c 5') indica, em sistemas linux, que deve mandar 5   pacotes. ('-W 3') indica, em sistemas linux, que deve esperar 3   milisegundos por uma resposta. Esta funcao retorna o codigo de   resposta do ping """

    plataforma = platform.system()
    args = []
    if plataforma == "Windows":
        args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]

    else:
        args = ['ping', '-c', '1', '-W', '1', hostname]
    
    ret_cod = subprocess.call(args, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
    return ret_cod

def get_hosts_rede(ip_base):
    """Verifica todos os host com a base_ip entre 1 e 255 retorna uma lista com todos os host que tiveram resposta 0 (ativo)"""

    host_validos = []
    return_codes = dict()
    for i in range(1, 255):
    
        return_codes[ip_base + '{0}'.format(i)] = retorna_codigo_ping(ip_base + '{0}'.format(i))
        if i %20 ==0:
            print(".", end = "")

        if return_codes[ip_base + '{0}'.format(i)] == 0:
            host_validos.append(ip_base + '{0}'.format(i))

    return host_validos

def detalhar_host(host_validos):
    """Obtendo nome do host"""
    nm = nmap.PortScanner()
    for host in host_validos:
        try:            
            nm.scan(host)

            host_ = Host(host, nm[host].hostname())            
            ## host_ = Host(host, 'carlos-MS-7a38')            

            for proto in nm[host].all_protocols():
                print('----------')
                print('Protocolo : %s' % proto)

            lport = nm[host][proto].keys()
            for port in lport:
                port_ = Porta(port, nm[host][proto][port]['state'])
                host_.ports.append(port_)

        except:
            pass
        
        portas = []

        for porta in host_.ports:
            portas.append({ 'porta': porta.port, 'estado': porta.state})

        retorno = { 'ip' : host_.ip, 'nome': host_.name, 'portas': portas}

        variaveis['hosts_detalhado'].append(retorno)

def get_hosts():
    meus_ips = variaveis['ips']

    if len(meus_ips) > 0:
        meu_ip_principal = meus_ips[0][1]
    
        # trata ip broadcast
        if meu_ip_principal == '127.0.0.1':
            meu_ip_principal = meus_ips[1][1]

        print('Ip que será utilizado como base', meu_ip_principal)
        ip_string = meu_ip_principal

        ip_lista = ip_string.split('.')
        base_ip = ".".join(ip_lista[0:3]) + '.'
        print("A busca será realizada na sub rede: ", base_ip)

        hosts_localizados = get_hosts_rede(base_ip) #['192.168.0.12', '192.168.0.13', '192.168.0.14']
        
        print('Verificar nomes dos hosts', hosts_localizados, '\r')
        detalhar_host(hosts_localizados)

def get_trafego_host():
    io_status = psutil.net_io_counters(pernic=True)
    hosts = variaveis['ips']

    trafego_interface = []

    if len(hosts) > 0:
        for host in hosts:
            trafego = io_status[host[0]]
            enviado = trafego[0]
            recebido = trafego[1]
            pct_enviado = trafego[2]
            pct_recebido = trafego[3]

            trafego_aux = Trafego(host[0], enviado, recebido, pct_enviado, pct_recebido)
            trafego_interface.append(trafego_aux.to_map())
        
        variaveis['trafego'].append(trafego_interface)

def get_info_memoria():
    memoria = psutil.virtual_memory()
    capacidade = round(memoria.total/(1024**3), 2)
    disponivel = round(memoria.available/(1024**3), 2)
    memoria_aux = Memoria(memoria, capacidade, disponivel)

    variaveis['memoria'].append(memoria_aux.get_map())

def get_processo():
    pids = psutil.pids()

    processos_coletados = []
    for pid in pids:
        try:
            nome = psutil.Process(pid).name()

            percent_uso = psutil.Process(pid).memory_percent()
            memoria_usada = psutil.Process(pid).memory_info().rss / 1024/1024
            threads_usadas = psutil.Process(pid).num_threads()
            tempo_usuario = str(psutil.Process(pid).cpu_times().user) + ' s'
            data_criacao = time.ctime(psutil.Process(pid).create_time())

            processo_aux = Processo(pid, nome, percent_uso, memoria_usada, threads_usadas, tempo_usuario, data_criacao)

            processos_coletados.append(processo_aux.to_map())
        except:
            print('>>> Erro ao obter informações sobre o processo de pid: ', pid)

    return processos_coletados

def get_processos_pagina(pagina, processos):
    total_de_processo = len(processos)

    total_paginas = math.ceil(total_de_processo / variaveis['total_elementos_por_pagina'])

    limite = int(pagina) * variaveis['total_elementos_por_pagina']
    inicio = limite - variaveis['total_elementos_por_pagina']
    paginado = processos[inicio:limite]

    return { 
        'elementos': paginado,
        'pagina_atual': pagina,
        'total_paginas': total_paginas,
        'total_elementos_por_pg': variaveis['total_elementos_por_pagina'],
        'total_processos': total_de_processo,
    }

def get_arquivos_paginado(pagina, arquivos):
    
    total_de_arquivos = len(arquivos)

    total_paginas = math.ceil(total_de_arquivos / variaveis['total_elementos_por_pagina'])

    limite = int(pagina) * variaveis['total_elementos_por_pagina']
    inicio = limite - variaveis['total_elementos_por_pagina']
    paginado = arquivos[inicio : limite]

    return {
        'elementos': paginado,
        'pagina_atual': pagina,
        'total_paginas': total_paginas,
        'total_elementos_por_pg': variaveis['total_elementos_por_pagina'],
        'total_arquivos': total_de_arquivos,
    }

# fim funcoes

# inicia thread
thread_disco = ThreadDisco(1, 'Thread-Disco', 1)
thread_disco.start()

thread_cpu = ThreadCpu(1, 'Thread-CPU', 1)
thread_cpu.start()

thread_sched = ThreadSched(1, 'Thread-sched', 1)
thread_sched.start()

thread_rede = ThreadIps(1, 'Thread-rede', 1)
thread_rede.start()

thread_scan_rede = ThreadRede(1, 'Thread-scan-rede', 1)
thread_scan_rede.start()

thread_scan_trafego_rede = ThreadTrafegoRede(1, 'Thread-trafego-rede', 1)
thread_scan_trafego_rede.start()

thread_memoria = ThreadMemoria(1, 'Thread-memoria', 1)
thread_memoria.start()

thread_processo = ThreadProcesso(1, 'Thread-processo', 1)
thread_processo.start()

thread_collector = ThreadCollector(2, 'ThreadCollector', 1)
thread_collector.start()

# inicio infra servidor
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname()                         
porta = 9999
socket_servidor.bind((host, porta))
socket_servidor.listen()

print("Servidor de nome:", host, " - Aguardando conexão na porta:", porta)
(socket_cliente,addr) = socket_servidor.accept()
print("Conectado a:", str(addr))
# fim infra servidor

while True:

    response = 'NoNe'
    try:
        msg = socket_cliente.recv(11)
    except:
        print('>>>> Coexão perdida')
        print("Servidor de nome:", host, " - Aguardando conexão na porta:", porta)
        (socket_cliente,addr) = socket_servidor.accept()


    decode = ''
    pagina = 1

    try:
        decode_aux = msg.decode('ascii')
        decode_aux = decode_aux.split('/')

        decode = decode_aux[0]
        pagina = decode_aux[1]
    except:
        decode = msg.decode('ascii')


    if decode == 'fim':
        break

    elif decode == 'disco':
        disco_aux = variaveis['disco'][len(variaveis['disco']) - 1]
        response = disco_aux.to_map()
    
    elif decode == 'cpu':
        cpu_aux = variaveis['cpu'][len(variaveis['cpu']) - 1]
        response = cpu_aux.to_map()

    elif decode == 'arquivos':
        response = []
        sched_aux = variaveis['sched'][len(variaveis['sched']) - 1]
        arquivos_aux = variaveis['arquivos'][len(variaveis['arquivos']) - 1]
        result = get_arquivos_paginado(pagina, arquivos_aux)

        diretorio = os.getcwd()
        
        response.append(diretorio)
        response.append(sched_aux)
        response.append(result)
    
    elif decode == 'ips':
        response = variaveis['ips']
    
    elif decode == 'rede':
        if len(variaveis['hosts_detalhado']) > 0:
            response = variaveis['hosts_detalhado']
    
    elif decode == 'trafego':
        if len(variaveis['trafego']) > 0:
            response = variaveis['trafego']
    
    elif decode == 'memoria':
        if len(variaveis['memoria']) > 0:
            response = variaveis['memoria'][len(variaveis['memoria']) - 1]

    elif decode == 'processo':        
        processos = variaveis['processo']
        response = get_processos_pagina(pagina, processos)
    
    elif decode == 'resumo':
        total_processo = len(variaveis['processo'])

        memoria = variaveis['memoria'][len(variaveis['memoria']) - 1]

        cpu_aux = variaveis['cpu'][len(variaveis['cpu']) - 1]
        cpu_aux = cpu_aux.to_map()

        disco_aux = variaveis['disco'][len(variaveis['disco']) - 1]
        disco_aux = disco_aux.to_map()

        ips = variaveis['ips']

        resumo = Resumo(total_processo, memoria['capacidade'], memoria['disponivel'], cpu_aux, disco_aux)
        resumo.ips = ips

        response = resumo.to_map()
    
    bytes_resp = pickle.dumps(response)
    
    socket_cliente.send(bytes_resp)

# Fecha socket do servidor e cliente
socket_cliente.close()
socket_servidor.close()