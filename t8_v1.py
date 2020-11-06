import pygame
import psutil
import cpuinfo
import platform
import subprocess
import os
import time
import socket
import sched
import nmap
import threading
import time

# variaveis globais
## cores
preto = (0, 0, 0)
cinza = (100, 100, 100)
grafite = (105,105,105)



## dimensoes
largura_tela = 800
altura_tela = 600

## controle aplicacao
variaveis = {
    'cpu': '',
    'memoria': '',
    'arquivos': {},
    'hosts': [],
    'hosts_detalhado': [],
    'executou': False,
    'executando': False,
    'ips': [],
    'vermelho': (255, 0, 0),
    'azul': (0, 0, 255),
    'preto': (0, 0, 0),
    'branco': (255, 255, 255),
    'posicionamento-instrucao': (300, 560)
}

terminou = False
count = 60
meu_ip = ''
lista_de_processos = []
posicao_atual = 1

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Projeto de bloco - Carlos Henrique")
pygame.display.init()

pygame.font.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

# superficies
superficie_info_cpu = pygame.surface.Surface((largura_tela, int(altura_tela/3)))

superficie_info_disco = pygame.surface.Surface((largura_tela, int(altura_tela/3)))
superficie_grafico_disco = pygame.surface.Surface((largura_tela, int(altura_tela/3)))

superficie_info_memoria = pygame.surface.Surface((largura_tela, int(altura_tela/3)))
superficie_grafico_memoria = pygame.surface.Surface((largura_tela, int(altura_tela/3)))

superficie_info_rede = pygame.surface.Surface((largura_tela, int(altura_tela/3)))

superficie_info_resumo = pygame.surface.Surface((largura_tela, int(altura_tela/3)))

# configuracao processador
info_cpu = cpuinfo.get_cpu_info()
psutil.cpu_percent(interval=1, percpu=True)

# classes
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
      get_arquivos()
      print ("Exiting thread" + self.name)

# inicio obtenção de dados
#
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
    #nm = nmap.PortScanner()
    for host in host_validos:
        try:            
            #nm.scan(host)

            #host_ = Host(host, nm[host].hostname())            
            host_ = Host(host, 'carlos-MS-7a38')            

            #for proto in nm[host].all_protocols():
            #    print('----------')
            #    print('Protocolo : %s' % proto)

            #lport = nm[host][proto].keys()
            #for port in lport:
            #    port_ = Port(port, nm[host][proto][port]['state'])
            #    host_.ports.append(port_)
            for i in range(0, 5):
                port_ = Port(i, 'open')
                host_.ports.append(port_)

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

    hosts_localizados = ['192.168.0.12', '192.168.0.13', '192.168.0.14']#get_hosts_rede(base_ip)
    
    print('Verificar nomes dos hosts', hosts_localizados, '\r')
    detalhar_host(hosts_localizados)

def get_info_memoria():

    if len(variaveis['memoria']) == 0:
        variaveis['memoria'] = []
        memoria = psutil.virtual_memory()
        capacidade = round(memoria.total/(1024**3), 2)
        disponivel = round(memoria.available/(1024**3), 2)

        memoria_aux = Memoria(memoria, capacidade, disponivel)
        variaveis['memoria'].append(memoria_aux)

def get_info_disco():
    disco = psutil.disk_usage('.')

    usado = round((disco.total - disco.free)  / 1024**3, 2)
    total = round(disco.total / (1024**3), 2)
    livre = round(disco.free/(1024**3),2)

    disco = Disco(disco, usado, total, livre)
    

#
# fim obtencao de dados

# inicio exibir informações em tela
def get_envolucro_cpu(cpu):
    """ RESPONSAVEL POR OBTER AS INFORMACOES DA CPU E EXIBIR EM TELA """
    superficie_info_cpu.fill(grafite)

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

def get_envolucro(posicao):

    if posicao == 0:
        get_envolucro_cpu(variaveis['cpu'])
        
        if len(variaveis['arquivos']) == 0:            
            thread1 = ThreadArquivos(1, "Thread-1 - Arquivos", 1)
            thread1.start()

        if len(variaveis['hosts']) == 0 and not variaveis['executou']:
            variaveis['hosts'] = get_meus_ips()

            thread2 = ThreadRede(1, "Thread-2", 1)
            thread2.start()

    elif posicao == 1:
        get_info_memoria()
        get_envolucro_memoria()

    elif posicao == 2:
        get_info_disco()
        #envolucro_dados_disco()

    elif posicao == 3:
        get_envolucro_rede()

    elif posicao == 4:
        print()
        #envolucro_arquivos()

    elif posicao == 5:    
        print()
        #envolucro_processo()

    elif posicao == 6:
        print()
        #resumo()

# 
def set_info_cpu(cpu):
    """ RESPONSAVEL POR EXIBIR EM TELA AS INFORMACOES DA CPU E """
    superficie_info_cpu.fill(grafite)

    # label
    text_arquitetura = font.render('Arquitetura:', True, 30)
    superficie_info_cpu.blit(text_arquitetura, (40, 30))
    # valor
    valor_arquitetura = font.render(cpu.arquitetura, True, 30)
    superficie_info_cpu.blit(valor_arquitetura, (180, 30))

    # label
    text_bits = font.render('Total Bits:', True, 30)
    superficie_info_cpu.blit(text_bits, (40, 50))
    # valor
    valor_bits = font.render(cpu.bits, True, 30)
    superficie_info_cpu.blit(valor_bits, (180, 50))

    # label
    text_frequencia = font.render('Frequência:', True, 30)
    superficie_info_cpu.blit(text_frequencia, (40, 70))
    # valor
    valor_frquencia = font.render(cpu.frequencia, True, 30)
    superficie_info_cpu.blit(valor_frquencia, (180, 70))

    # label
    text_nucleo = font.render('Núcleos (físico):', True, 30)
    superficie_info_cpu.blit(text_nucleo, (40, 90))
    # valor
    valor_nucleo = font.render(cpu.nucleos, True, 30)
    superficie_info_cpu.blit(valor_nucleo, (180, 90))

    # label
    texto_nome = font.render('Nome:', True, preto)
    superficie_info_cpu.blit(texto_nome, (40, 110))
    # valor
    valor_nome = font.render(cpu.nome, True, preto)
    superficie_info_cpu.blit(valor_nome, (180, 110))

    tela.blit(superficie_info_cpu, (0,0))

def set_grafico_cpu(s):
    # construcao do grafico
    l_cpu_percent = psutil.cpu_percent(percpu=True)

    s.fill(grafite)

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
    instrucao = font.render('Tecle ← ou → para navegar', True, preto)
    tela.blit(instrucao, (300, 580))

    tela.blit(s, (0, 300))

def set_info_rede():
    tela.fill(grafite)

    titulo = font.render("** Informações de Rede **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 30))

    espacos = 55

    hosts_aux = variaveis['hosts']

    for host in hosts_aux:
        ip_formatada = str(host[1])

        if len(host[2]) == 9:
            gateway_formatada = '{:>33}'.format(str(host[2]))
        else:
            gateway_formatada = '{:>30}'.format(str(host[2]))

        if len(host[0]) < 5:
            nome_interface_formatada = '{:>23}'.format(str(host[0]))
        else:    
            nome_interface_formatada = '{:>20}'.format(str(host[0]))

        texto = font.render(ip_formatada +  gateway_formatada + nome_interface_formatada, 1, preto)
        
        tela.blit(texto, (15, espacos))
        espacos += 25

    # exibir msg de informacao: escaneando rede
    if len(variaveis['hosts_detalhado']) == 0:
        texto_atencao = font.render('Lendo dados da rede. Aguarde...', 10, variaveis['vermelho'])
        tela.blit(texto_atencao, (260, 185))

def set_info_hosts_rede():

    espacos = 200

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
            detalhe_porta = font.render("Porta: " + str(porta.port) + " - Estado: " + porta.state ,1, variaveis['azul'])
            tela.blit(detalhe_porta, (15, espacos + 10))
            espacos += 15

        espacos += 10

    # instrucao navegacao
    instrucao = font.render('Tecle ← ou → para navegar', True, preto)
    tela.blit(instrucao, (300, 570))

def set_info_memoria():
    tela.fill(grafite)

    titulo = font.render("** Informações de Memória **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 30))

    # titulo
    texto = font.render('Capacidade', True, variaveis['preto'])
    tela.blit(texto, (15, 60))

    # valor
    tela.blit(font.render(str(variaveis['memoria'][0].capacidade) + 'GB', True, preto), (155, 60))

    #titulo
    texto = font.render('Disponível', True, variaveis['preto'])
    tela.blit(texto, (15, 80))

    # valor
    tela.blit(font.render(str(variaveis['memoria'][0].disponivel), True, preto), (155, 80))

def set_grafico_memoria():
    memoria = variaveis['memoria'][0].memoria

    largura = largura_tela - 2 * 20
    pygame.draw.rect(tela, variaveis['branco'], (15, 270, largura, 5))
    
    largura = largura * memoria.percent / 100
    pygame.draw.rect(tela, variaveis['azul'], (15, 270, largura, 5))
    
    total = round(memoria.total / (1024 * 1024 * 1024), 2)
    
    percentagem = memoria.percent
    texto_da_barra = ('Percentual usado: {}% (Total: {} GB)'.format(percentagem, total))
    text = font.render(texto_da_barra, 1, variaveis['branco'])

    tela.blit(text, (20, 240))

    # instrucao navegacao
    instrucao = font.render('Tecle ← ou → para navegar', True, preto)
    tela.blit(instrucao, variaveis['posicionamento-instrucao'])


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
                posicao_atual = 6


#carrossel           
    if count == 60:
        tela.fill(grafite)

        if posicao_atual < 0:
            posicao_atual = 6
            
        elif posicao_atual > 6:
            posicao_atual = 0
        
        variaveis['executando'] = True
        get_envolucro(posicao_atual)
        variaveis['executou'] = True
        
        count = 0    
        
    pygame.display.update()
    
    clock.tick(60)
    count = count + 1
        
pygame.display.quit()

