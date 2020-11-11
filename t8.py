import pygame, psutil, cpuinfo, platform, subprocess, os, time, socket, sched, nmap, threading, time

# variaveis globais

## controle aplicacao
variaveis = {
    'cpu': '',
    'memoria': '',
    'disco': '',
    'processos': [],
    'trafego': [],
    'arquivos': {},
    'execucao_leitura_arquivos': '',
    'hosts': [],
    'hosts_detalhado': [],
    'executou': False,
    'executando': False,
    'ips': [],
    'vermelho': (255, 0, 0),
    'azul': (0, 0, 255),
    'preto': (0, 0, 0),
    'branco': (255, 255, 255),
    'cinza': (100, 100, 100),
    'grafite': (105,105,105),
    'posicionamento-instrucao': (250, 560),
    'tamanho-minimo-palavra': 15
}

# inicio configuracoes pygame
#
largura_tela = 800
altura_tela = 600

terminou = False
count = 60
meu_ip = ''
lista_de_processos = []
posicao_atual = 0

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Projeto de bloco - Carlos Henrique")
pygame.display.init()

pygame.font.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)
#
# fim configuracoes pygame

# inicio superficies
#
superficie_info_cpu = pygame.surface.Surface((largura_tela, int(altura_tela/3)))
#
# fim classes

# configuracao processador
info_cpu = cpuinfo.get_cpu_info()
psutil.cpu_percent(interval=1, percpu=True)

# inicio classes
#
class Host:
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name
        self.ports = []   

class Port:
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

#
# fim classes

# inicio threads
#
class ThreadRede(threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter      

   def run(self):
      print ("Starting thread" + self.name)
      get_hosts()
      print ("Exiting thread" + self.name)

class ThreadArquivos(threading.Thread):

   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter      

   def run(self):
      print ("Starting thread" + self.name)
      variaveis['execucao_leitura_arquivos'] = get_sched_scheduler_arquivos()
      print(variaveis['execucao_leitura_arquivos'])
      print ("Exiting thread" + self.name)
# 
# fim threads

# inicio obtenção de dados
#

def get_nova_string(palavra):
    ''' Responsavel por padronizar o tamanho das string a serem exibidas em tela '''
    palavra_aux = palavra

    tamanho_minimo = variaveis['tamanho-minimo-palavra']
    tamanho_palavra = len(palavra_aux)

    if tamanho_palavra > tamanho_minimo:
        # recorta a string
        palavra_aux = '{:.10}'.format(palavra)
    else:
        # adiciona espacos
        while tamanho_palavra != tamanho_minimo:
            palavra_aux = palavra_aux + " "
            tamanho_palavra = len(palavra_aux)

    return palavra_aux

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
    return cpu


def get_arquivos():
    arquivos_aux = os.listdir()

    for arquivo in arquivos_aux:
        variaveis['arquivos'][arquivo] = []
        variaveis['arquivos'][arquivo].append(os.stat(arquivo).st_size)
        variaveis['arquivos'][arquivo].append(os.stat(arquivo).st_ctime)
        variaveis['arquivos'][arquivo].append(os.stat(arquivo).st_mtime)


def get_sched_scheduler_arquivos():
    inicio = time.time()
    inicioClock = time.process_time()

    sched_ = sched.scheduler(time.time, time.sleep)

    sched_.enter(3, 1, get_arquivos())

    tempoFinal = 'TEMPO FINAL: %s | CLOCK FINAL: %0.2f' % (time.ctime(), time.process_time())

    final = time.time() - inicio
    finalClock = time.process_time() - inicioClock

    tempoUsado = 'TEMPO USADO NESSA CHAMADA: %0.3f segundos | CLOCK USADO NESSA CHAMADA: %0.2f' % (final, finalClock)

    return tempoFinal, tempoUsado

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
                port_ = Port(port, nm[host][proto][port]['state'])
                host_.ports.append(port_)

            #for i in range(0, 5):
            #    port_ = Port(i, 'open')
            #    host_.ports.append(port_)

        except:
            pass
        
        variaveis['hosts_detalhado'].append(host_)        

def get_hosts():
    meus_ips = variaveis['hosts']
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
    hosts = variaveis['hosts']

    trafego_interface = []

    for host in hosts:
        trafego = io_status[host[0]]
        enviado = trafego[0]
        recebido = trafego[1]
        pct_enviado = trafego[2]
        pct_recebido = trafego[3]

        trafego_aux = Trafego(host[0], enviado, recebido, pct_enviado, pct_recebido)
        trafego_interface.append(trafego_aux)
        

    variaveis['trafego'].append(trafego_interface)

def get_trafego_da_interface(interface):
    trafego_coletado = variaveis['trafego']
    trafego_exibir = trafego_coletado[len(trafego_coletado) - 1]
    retorno = ''

    for trafego in trafego_exibir:
        if trafego.interface == interface:
            retorno = trafego
            break

    return retorno

def get_info_memoria():
    if len(variaveis['memoria']) == 0:
        variaveis['memoria'] = []
        memoria = psutil.virtual_memory()
        capacidade = round(memoria.total/(1024**3), 2)
        disponivel = round(memoria.available/(1024**3), 2)

        memoria_aux = Memoria(memoria, capacidade, disponivel)
        variaveis['memoria'].append(memoria_aux)

def get_info_disco():
    if len(variaveis['disco']) == 0:
        variaveis['disco'] = []

        disco = psutil.disk_usage('.')
        usado = round((disco.total - disco.free)  / 1024**3, 2)
        total = round(disco.total / (1024**3), 2)
        livre = round(disco.free/(1024**3),2)

        disco_aux = Disco(disco, usado, total, livre)
        variaveis['disco'].append(disco_aux)

def get_processos():
    pids = psutil.pids()

    pids.reverse()

    total_de_processos_obtidos = 0

    for pid in pids:
        try:
            nome = psutil.Process(pid).name()
            tamanho_do_nome = len(nome)

            if tamanho_do_nome <= 15 and pid != 1:

                percent_uso = psutil.Process(pid).memory_percent()
                memoria_usada = psutil.Process(pid).memory_info().rss / 1024/1024
                threads_usadas = psutil.Process(pid).num_threads()
                tempo_usuario = str(psutil.Process(pid).cpu_times().user) + ' s'
                data_criacao = time.ctime(psutil.Process(pid).create_time())

                processo_aux = Processo(pid, nome, percent_uso, memoria_usada, threads_usadas, tempo_usuario, data_criacao)

                variaveis['processos'].append(processo_aux)
                total_de_processos_obtidos += 1
        except:
            print('Erro ao obter informações do processo: ', pid)
        
        if total_de_processos_obtidos == 10:
            break

def get_trafego_processo():
    processos = variaveis['processos']

    # conexao = ''

    # for processo in processos:
    #     try:
    #         process = psutil.Process(processo.pid)
    #         conexao = process.connections()
    #     except:
    #         pass

    #     print(conexao)

#
# fim obtencao de dados

# inicio exibir informações em tela
#
def get_envolucro_cpu(cpu):
    """ RESPONSAVEL POR OBTER AS INFORMACOES DA CPU E EXIBIR EM TELA """
    superficie_info_cpu.fill(variaveis['grafite'])

    # obtem dados da cpu
    try:
        if len(cpu) == 0:
            variaveis['cpu'] = get_info_cpu()
    except:
        pass

    # apresenta em tela
    set_info_cpu(variaveis['cpu'])
    set_grafico_cpu(superficie_info_cpu)

def get_envolucro_rede():
    set_info_rede()
    set_info_hosts_rede()

def get_envolucro_memoria():
    set_info_memoria()
    set_grafico_memoria()

def get_envolucro_disco():
    set_info_disco()
    set_grafico_disco()

def get_envolucro_arquivo():
    set_info_arquivo()

def get_envolucro_processos():
    set_info_processo()

def get_envolucro_trafego_processo():
    get_trafego_processo()
    set_trafego_dados_processo()

def get_envolucro_resumo():
    set_info_resumo()

def get_envolucro(posicao):

    # prioridades de execucao
    get_info_disco()
    get_info_memoria()

    variaveis['hosts'] = get_meus_ips()
    get_trafego_host()

    if posicao == 0:
        get_envolucro_cpu(variaveis['cpu'])
        
        if len(variaveis['arquivos']) == 0:            
            thread1 = ThreadArquivos(1, "Thread-1 - Arquivos", 1)
            thread1.start()

        if len(variaveis['hosts_detalhado']) == 0 and not variaveis['executou']:
            thread2 = ThreadRede(1, "Thread-2", 1)
            thread2.start()

    elif posicao == 1:
        get_envolucro_memoria()

    elif posicao == 2:        
        get_envolucro_disco()

    elif posicao == 3:
        get_envolucro_rede()

    elif posicao == 4:
        get_envolucro_arquivo()

    elif posicao == 5:    
        if len(variaveis['processos']) == 0:
            get_processos()
        get_envolucro_processos()

    elif posicao == 6:
        get_envolucro_trafego_processo()

    elif posicao == 7:
        get_envolucro_resumo()

# 
def set_info_cpu(cpu):
    """ RESPONSAVEL POR EXIBIR EM TELA AS INFORMACOES DA CPU E """
    superficie_info_cpu.fill(variaveis['grafite'])

    # label
    text_arquitetura = font.render('Arquitetura:', True, (30, 0, 0))
    superficie_info_cpu.blit(text_arquitetura, (40, 30))
    # valor
    valor_arquitetura = font.render(cpu.arquitetura, True, (30, 0, 0))
    superficie_info_cpu.blit(valor_arquitetura, (180, 30))

    # label
    text_bits = font.render('Total Bits:', True, (30, 0, 0))
    superficie_info_cpu.blit(text_bits, (40, 50))
    # valor
    valor_bits = font.render(cpu.bits, True, (30, 0, 0))
    superficie_info_cpu.blit(valor_bits, (180, 50))

    # label
    text_frequencia = font.render('Frequência:', True, (30, 0, 0))
    superficie_info_cpu.blit(text_frequencia, (40, 70))
    # valor
    valor_frquencia = font.render(cpu.frequencia, True, (30, 0, 0))
    superficie_info_cpu.blit(valor_frquencia, (180, 70))

    # label
    text_nucleo = font.render('Núcleos (físico):', True, (30, 0, 0))
    superficie_info_cpu.blit(text_nucleo, (40, 90))
    # valor
    valor_nucleo = font.render(cpu.nucleos, True, (30, 0, 0))
    superficie_info_cpu.blit(valor_nucleo, (180, 90))

    # label
    texto_nome = font.render('Nome:', True, variaveis['preto'])
    superficie_info_cpu.blit(texto_nome, (40, 110))
    # valor
    valor_nome = font.render(cpu.nome, True, variaveis['preto'])
    superficie_info_cpu.blit(valor_nome, (180, 110))

    tela.blit(superficie_info_cpu, (0,0))

def set_grafico_cpu(s):
    # construcao do grafico
    l_cpu_percent = psutil.cpu_percent(percpu=True)

    s.fill(variaveis['grafite'])

    capacidade = psutil.cpu_percent(interval=1)
    num_cpu = len(l_cpu_percent)

    x = y = 10
    desl = 10
    
    alt = s.get_height() - 2*y
    larg = (s.get_width() - 2 * y - (num_cpu + 1) * desl) / num_cpu
    d = x + desl
    
    for i in l_cpu_percent:
        pygame.draw.rect(s, variaveis['azul'], (d, y + 20, larg, alt))
        pygame.draw.rect(s, variaveis['branco'], (d, y + 20, larg, (1 - i / 100) * alt))
        d = d + larg + desl

    text = font.render("Uso de CPU por núcleo total: " + str(capacidade) + "%", 1, variaveis['branco'])
    s.blit(text, (20, 5))

    # instrucao navegacao
    instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
    tela.blit(instrucao, variaveis['posicionamento-instrucao'])

    tela.blit(s, (0, 300))

def set_info_rede():
    tela.fill(variaveis['grafite'])

    titulo = font.render("** Informações de Rede **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 30))

    titulo = font.render("Interface                    IP                    Mascara                    Pct. Enviado              Pct. Recebido" , 1, variaveis['preto'])
    tela.blit(titulo, (15, 55))

    espacos = 100

    hosts_aux = variaveis['hosts']

    for host in hosts_aux:


        interface = host[0]
        trafego_da_interface = get_trafego_da_interface(interface)

        ip = str(host[1])

        if ip !='127.0.0.1':            

            pct_recebido = round(trafego_da_interface.pacotes_recebidos / (1024 ** 2), 2)
            pct_enviado = round(trafego_da_interface.pacotes_enviados / (1024 ** 2), 2)

            pct_enviado_formatado = '{:>25}'.format(str(pct_enviado)) + 'MB'
            pct_recebido_formatado = '{:>20}'.format(str(pct_recebido)) + 'MB'

            nome_interface_formatada = get_nova_string(str(host[0]))
            
            ip_formatada = get_nova_string(str(host[1]))
            ip_formatada_ = '{:>20}'.format(ip_formatada)

            mascara = get_nova_string(str(host[2]))
            mascara_formatada = '{:>20}'.format(mascara)

            texto = font.render(nome_interface_formatada + ip_formatada_ +  mascara_formatada + pct_enviado_formatado + pct_recebido_formatado, 1, variaveis['preto'])
            
            tela.blit(texto, (15, espacos))
            espacos += 25

    # exibir msg de informacao: escaneando rede
    if len(variaveis['hosts_detalhado']) == 0:
        texto_atencao = font.render('Lendo dados da rede. Aguarde...', 10, variaveis['vermelho'])
        tela.blit(texto_atencao, (260, 185))

def set_info_hosts_rede():

    espacos = 300

    for host in variaveis['hosts_detalhado']:
        host_name = ""

        if host.name != "":
            host_name = host.name

        else:
            host_name = "NÃO LOCALIZADO"

        cor = ""

        if host_name != "NÃO LOCALIZADO":
            cor = variaveis['vermelho']

        else:
            cor = variaveis['azul']

        texto = font.render(host.ip + ': Nome: ' + host_name, 1, variaveis['azul'])
        
        tela.blit(texto, (15, espacos + 5))
        espacos += 15

        for porta in host.ports:
            porta_label = font.render("Porta: ", 1, variaveis['branco'])            
            tela.blit(porta_label, (15, espacos + 10))

            porta_text = font.render(str(porta.port), 1, variaveis['branco'])
            tela.blit(porta_text, (70, espacos + 10))

            estado_label = font.render("Estado: ", 1, variaveis['branco'])            
            tela.blit(estado_label, (140, espacos + 10))
            
            estado = font.render(porta.state, 1, variaveis['branco'])            
            tela.blit(estado, (210, espacos + 10))

            espacos += 15

        espacos += 20

    # instrucao navegacao
    instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
    tela.blit(instrucao, variaveis['posicionamento-instrucao'])

def set_info_memoria():
    tela.fill(variaveis['grafite'])

    titulo = font.render("** Informações de Memória **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 30))

    # titulo
    texto = font.render('Capacidade', True, variaveis['preto'])
    tela.blit(texto, (15, 60))

    # valor
    tela.blit(font.render(str(variaveis['memoria'][0].capacidade) + 'GB', True, variaveis['preto']), (155, 60))

    #titulo
    texto = font.render('Disponível', True, variaveis['preto'])
    tela.blit(texto, (15, 80))

    # valor
    tela.blit(font.render(str(variaveis['memoria'][0].disponivel), True, variaveis['preto']), (155, 80))

def set_grafico_memoria():
    memoria = variaveis['memoria'][0].memoria

    largura = largura_tela - 2 * 20
    pygame.draw.rect(tela, variaveis['branco'], (15, 270, largura, 5))
    
    largura = largura * memoria.percent / 100
    pygame.draw.rect(tela, variaveis['azul'], (15, 270, largura, 5))
    
    total = round(memoria.total / (1024 * 1024 * 1024), 2)
    
    porcentagem = memoria.percent

    texto_da_barra = ('Percentual usado: {}% (Total: {} GB)'.format(porcentagem, total))
    text = font.render(texto_da_barra, 1, variaveis['branco'])
    tela.blit(text, (20, 240))

    # instrucao navegacao
    instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
    tela.blit(instrucao, variaveis['posicionamento-instrucao'])

def set_info_disco():
    tela.fill(variaveis['grafite'])

    titulo = font.render("** Informações do Disco **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 30))

    # titulo
    texto = font.render('Capacidade', True, variaveis['preto'])
    tela.blit(texto, (15, 60))

    # valor
    tela.blit(font.render(str(variaveis['disco'][0].total) + 'GB', True, variaveis['preto']), (155, 60))

    #titulo
    texto = font.render('Disponível', True, variaveis['preto'])
    tela.blit(texto, (15, 80))

    # valor
    tela.blit(font.render(str(variaveis['disco'][0].livre) + 'GB', True, variaveis['preto']), (155, 80))

    #titulo
    texto = font.render('Usado', True, variaveis['preto'])
    tela.blit(texto, (15, 100))

    # valor
    tela.blit(font.render(str(variaveis['disco'][0].usado) + 'GB', True, variaveis['preto']), (155, 100))

def set_grafico_disco():
    disco_aux = variaveis['disco'][0]

    total = disco_aux.total
    largura = largura_tela - 2 * 20

    pygame.draw.rect(tela, variaveis['branco'], (15, 270, largura, 5))
    
    consumo = largura * disco_aux.disco.percent / 100
    pygame.draw.rect(tela, variaveis['azul'], (15, 270, consumo, 5))

    texto_da_barra = ('Uso de Disco: {}% (Total: {} GB)'.format(consumo, total))
    texto = font.render(texto_da_barra, 1, variaveis['branco'])
    tela.blit(texto, (20, 240))

    # instrucao navegacao
    instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
    tela.blit(instrucao, variaveis['posicionamento-instrucao'])    

def set_info_arquivo():

    tela.fill(variaveis['grafite'])

    titulo = font.render("** Arquivos do diretório **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 30))

    arquivos = variaveis['arquivos']

    
    titulo = font.render("Nome                       Data Criacao                        Data Modificacao                                 Tamanho" , 1, variaveis['preto'])
    tela.blit(titulo, (15, 55))

    espacos = 100
    total_a_exibir = 0

    for arquivo in arquivos:        

        if total_a_exibir <= 10:

            tamanho_aux = len(arquivo)

            tamanho_arquivo = str(format(arquivos[arquivo][0] / 1024, '.2f')) + 'Kb'
                    
            nome_arquivo = get_nova_string(arquivo)
            texto_formatado = font.render(nome_arquivo , 1, variaveis['preto'])
            tela.blit(texto_formatado, (15, espacos))

            data_criacao = time.ctime(arquivos[arquivo][0])
            texto_formatado = font.render(data_criacao , 1, variaveis['preto'])
            tela.blit(texto_formatado, (140, espacos))

            
            data_modificacao = time.ctime(arquivos[arquivo][1])
            data_modificacao_formatado = font.render(data_modificacao , 1, variaveis['preto'])
            tela.blit(texto_formatado, (400, espacos))
            

            tamanho_arquivo_formatado = font.render(tamanho_arquivo, 1, variaveis['preto'])
            tela.blit(tamanho_arquivo_formatado, (700, espacos))
            
            espacos += 25
            total_a_exibir += 1

    time_leitura = variaveis['execucao_leitura_arquivos']

    tempoFinal = time_leitura[0]
    tempoUsado = time_leitura[1]

    informacao = font.render(tempoFinal, True, variaveis['branco'])
    tela.blit(informacao, (15, 480))

    informacao = font.render(tempoUsado, True, variaveis['branco'])
    tela.blit(informacao, (15, 500))

    


    
    # instrucao navegacao
    instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
    tela.blit(instrucao, variaveis['posicionamento-instrucao'])

def set_trafego_dados_processo():
    tela.fill(variaveis['grafite'])

    titulo = font.render("** Trafego de dados dos 10 últimos processos **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 30))

def set_info_processo():
    tela.fill(variaveis['grafite'])

    titulo = font.render("** Lista dos 10 últimos processos em execução **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 30))

    titulo = font.render("PID            % Uso        Mem. Usada     Threads Usada           Tempo                        Nome" , 1, variaveis['preto'])
    tela.blit(titulo, (15, 55))

    espacos = 100

    processos = variaveis['processos']

    for processo in processos:

        text_pid = '{:>0}'.format(str(processo.pid))

        if len(str(processo.pid)) == 1:
            text_percentual_uso = '{:>17}'.format(str(format(processo.percentual_uso, '.2f')))
        else:
            text_percentual_uso = '{:>15}'.format(str(format(processo.percentual_uso, '.2f')))

        text_memoria_usada = '{:>20}'.format(str(format(processo.memoria_usada, '.2f') ))
        text_threads_processo = '{:>20}'.format(str(format(processo.threads_processo, '.2f')))
        text_tempo_usuario = '{:>20}'.format(processo.tempo_usuario)
        text_nome = '{:>30}'.format(processo.nome)

        texto_formatado = text_pid + text_percentual_uso + text_memoria_usada + text_threads_processo #+ text_tempo_usuario + text_nome

        texto = font.render(text_tempo_usuario, 1, variaveis['preto'])
        tela.blit(texto, (410, espacos))

        texto = font.render(texto_formatado, 1, variaveis['preto'])
        tela.blit(texto, (15, espacos))

        texto = font.render(text_nome, 1, variaveis['preto'])
        tela.blit(texto, (530, espacos))

        espacos += 25
    
    # instrucao navegacao
    instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
    tela.blit(instrucao, variaveis['posicionamento-instrucao'])

def set_info_resumo():
    tela.fill(variaveis['grafite'])

    titulo = font.render("** Resumo dos dados coletados **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 30))

    titulo = font.render("CPU" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 60))

    processador = variaveis['cpu']
    disco = variaveis['disco'][0]
    memoria = variaveis['memoria'][0]

    # obtem o ip do usuario
    host = variaveis['hosts'][0][1]
    if host == '127.0.0.1':
        host = variaveis['hosts'][1][1]

    # titulo
    texto = font.render('Processador:', True, variaveis['preto'])
    tela.blit(texto, (15, 80))
    # valor
    tela.blit(font.render(processador.nome, True, variaveis['preto']), (155, 80))

    # titulo
    texto = font.render('Frequência:', True, variaveis['preto'])
    tela.blit(texto, (15, 100))
    # valor
    tela.blit(font.render(processador.frequencia, True, variaveis['preto']), (155, 100))

    # titulo
    texto = font.render('Bits:', True, variaveis['preto'])
    tela.blit(texto, (15, 120))
    # valor
    tela.blit(font.render(processador.bits, True, variaveis['preto']), (155, 120))
    
    #
    tela.blit(font.render('----------------------------------------------------------', True, variaveis['branco']), (180, 150))

    titulo = font.render("Disco" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 170))

    # titulo
    texto = font.render('Total:', True, variaveis['preto'])
    tela.blit(texto, (15, 190))
    # valor
    tela.blit(font.render(str(disco.total) + 'GB', True, variaveis['preto']), (155, 190))

    # titulo
    texto = font.render('Livre:', True, variaveis['preto'])
    tela.blit(texto, (15, 210))
    # valor
    tela.blit(font.render(str(disco.livre) + 'GB', True, variaveis['preto']), (155, 210))

    # titulo
    texto = font.render('Usado:', True, variaveis['preto'])
    tela.blit(texto, (15, 230))
    # valor
    tela.blit(font.render(str(disco.usado) + 'GB', True, variaveis['preto']), (155, 230))

    #
    tela.blit(font.render('----------------------------------------------------------', True, variaveis['branco']), (180, 260))

    titulo = font.render("Memória" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 280))

    # titulo
    texto = font.render('Total:', True, variaveis['preto'])
    tela.blit(texto, (15, 300))
    # valor
    tela.blit(font.render(str(memoria.capacidade) + 'GB', True, variaveis['preto']), (155, 300))

    # titulo
    texto = font.render('Livre:', True, variaveis['preto'])
    tela.blit(texto, (15, 320))
    # valor
    tela.blit(font.render(str(memoria.disponivel) + 'GB', True, variaveis['preto']), (155, 320))

    # titulo
    texto = font.render('Usado:', True, variaveis['preto'])
    tela.blit(texto, (15, 340))
    # valor
    tela.blit(font.render(str((format(float(memoria.capacidade) - float(memoria.disponivel), '.2f'))) + 'GB', True, variaveis['preto']), (155, 340))

    #
    tela.blit(font.render('----------------------------------------------------------', True, variaveis['branco']), (180, 370))

    titulo = font.render("Rede" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 390))

    # titulo
    texto = font.render('IP:', True, variaveis['preto'])
    tela.blit(texto, (15, 410))
    # valor
    tela.blit(font.render(host, True, variaveis['preto']), (155, 410))


    # instrucao navegacao
    instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
    tela.blit(instrucao, variaveis['posicionamento-instrucao'])

#
#fim exibir informações em tela

while not terminou:
        
    for event in pygame.event.get():

        # para a aplicacao
        if event.type == pygame.QUIT:
            terminou = True
        
        # monitora interação do usuario
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                posicao_atual = posicao_atual + 1
                
            elif event.key == pygame.K_LEFT:
                posicao_atual = posicao_atual - 1
            
            elif event.key == pygame.K_SPACE:
                posicao_atual = 7


#carrossel           
    if count == 60:
        tela.fill(variaveis['grafite'])

        if posicao_atual < 0:
            posicao_atual = 7
            
        elif posicao_atual > 7:
            posicao_atual = 0
        
        variaveis['executando'] = True
        get_envolucro(posicao_atual)
        variaveis['executou'] = True
        
        count = 0    
        
    pygame.display.update()
    
    clock.tick(60)
    count = count + 1
        
pygame.display.quit()

