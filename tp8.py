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

info_cpu = cpuinfo.get_cpu_info()
psutil.cpu_percent(interval=1, percpu=True)

preto = (0, 0, 0)
branco = (255, 255, 255)
cinza = (100, 100, 100)
Dim = (105,105,105)
azul = (0, 0, 255)
vermelho = (255, 0, 0)

largura_tela = 800
altura_tela = 600

# configurações da tela
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Projeto de bloco - Carlos Henrique")
pygame.display.init()

# configurando a fonte
pygame.font.init()
font = pygame.font.SysFont(None, 20)

superficie_info_cpu = pygame.surface.Surface((largura_tela, int(altura_tela/3)))
superficie_grafico_cpu = pygame.surface.Surface((largura_tela, int(altura_tela/3)))

superficie_info_disco = pygame.surface.Surface((largura_tela, int(altura_tela/3)))
superficie_grafico_disco = pygame.surface.Surface((largura_tela, int(altura_tela/3)))

superficie_info_memoria = pygame.surface.Surface((largura_tela, int(altura_tela/3)))
superficie_grafico_memoria = pygame.surface.Surface((largura_tela, int(altura_tela/3)))

superficie_info_rede = pygame.surface.Surface((largura_tela, int(altura_tela/3)))

superficie_info_resumo = pygame.surface.Surface((largura_tela, int(altura_tela/3)))

clock = pygame.time.Clock()

terminou = False
count = 60

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

class ThreadRede(threading.Thread):

   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter      

   def run(self):
      print ("Starting thread" + self.name)
      envolucro_detalhar_host()
      print ("Exiting thread" + self.name)

class ThreadArquivos(threading.Thread):

   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter      

   def run(self):
      print ("Starting thread" + self.name)
      mostrar_dados_diretorio()
      print ("Exiting thread" + self.name)

####################################################################################################################
# variaveis globais
meu_ip = ''
hosts = []
lista_de_processos = []
posicao_atual = 0
arquivos = {}
####################################################################################################################
def mostra_info_cpu():
    superficie_info_cpu.fill(branco)
    
    mostra_texto_cpu(superficie_info_cpu, "Nome:", "brand_raw", 110)
    mostra_texto_cpu(superficie_info_cpu, "Arquitetura:", "arch", 30)
    mostra_texto_cpu(superficie_info_cpu, "Palavra (bits):", "bits", 50)
    mostra_texto_cpu(superficie_info_cpu, "Frequência (MHz):", "hz_actual_friendly", 70)
    mostra_texto_cpu(superficie_info_cpu, "Núcleos (físicos):", "count", 90)
    tela.blit(superficie_info_cpu, (0, 0))

def mostra_texto_cpu(s1, nome, chave, pos_y):
    text = font.render(nome, True, preto)
    s1.blit(text, (40, pos_y))
    
    if chave == "freq":
        s = str(round(psutil.cpu_freq().current, 2))
        
    elif chave == "nucleos":
        s = str(psutil.cpu_count())
        s = s + " (" + str(psutil.cpu_count(logical=False)) + ")"
        
    else:
        s = str(info_cpu[chave])
        text = font.render(s, True, cinza)
        superficie_info_cpu.blit(text, (155, pos_y))
# Desenha grafico  
def mostrar_uso_cpu(s):
    l_cpu_percent = psutil.cpu_percent(percpu=True)
    s.fill(preto)
    capacidade = psutil.cpu_percent(interval=1)
    num_cpu = len(l_cpu_percent)
    x = y = 10
    desl = 10
    alt = s.get_height() - 2*y
    larg = (s.get_width() - 2 * y - (num_cpu + 1) * desl) / num_cpu
    d = x + desl
    
    for i in l_cpu_percent:
        pygame.draw.rect(s, azul, (d, y + 20, larg, alt))
        pygame.draw.rect(s, Dim, (d, y + 20, larg, (1 - i / 100) * alt))
        d = d + larg + desl

    text = font.render("Uso de CPU por núcleo total: " + str(capacidade) + "%", 1, branco)
    s.blit(text, (20, 5))
    tela.blit(s, (0, 200))

def envolucro_dados_cpu():
    mostra_info_cpu()
    mostrar_uso_cpu(superficie_grafico_cpu)
####################################################################################################################
def mostrar_info_disco():
    superficie_info_disco.fill(branco)    

    titulo = font.render("** Informações do Disco **" ,1, azul)

    superficie_info_disco.blit(titulo,(15, 30))

    mostrar_texto_disco(superficie_info_disco, "total_disco", "Total:", 60)
    mostrar_texto_disco(superficie_info_disco, "disco_livre", "Livre:", 75)    
    mostrar_texto_disco(superficie_info_disco, "disco_usado", "Usado:", 45)
    tela.blit(superficie_info_disco, (0, 0))    

def mostrar_texto_disco(s1, chave, nome, pos_y):
    disco = psutil.disk_usage('.')
    texto = font.render(nome, True, preto)
    s1.blit(texto, (40, pos_y))
    

    usado = (disco.total - disco.free)  / 1024**3

    disco_usado= str(round(usado, 2)) + " GB"
    total_disco = str(round(disco.total / (1024**3), 2)) + " GB"
    disco_livre = str(round(disco.free/(1024**3), 2)) + " GB"
    
    if chave == "total_disco":
        s1.blit(font.render(total_disco, True, preto), (155, pos_y))
        
    elif chave == "disco_usado":
        s1.blit(font.render(disco_usado, True, preto), (155, pos_y))
        
    elif chave == "disco_livre":
        s1.blit(font.render(disco_livre, True, preto), (155, pos_y))
        
def mostra_uso_disco(eixo_x, eixo_y):
    disco = psutil.disk_usage('.')
    total = round(disco.total / (1024 * 1024 * 1024), 2)
    largura = largura_tela - 2 * 20

    pygame.draw.rect(superficie_grafico_disco, cinza, (20, 5, largura, 5))

    tela.blit(superficie_grafico_disco, (0, eixo_x))
    largura = largura * disco.percent / 100

    pygame.draw.rect(superficie_grafico_disco, azul, (20, 5, largura, 5))
    tela.blit(superficie_grafico_disco, (0, eixo_y))

    
    percentagem = disco.percent

    texto_da_barra = ('Uso de Disco: {}% (Total: {} GB)'.format(percentagem, total))
    text = font.render(texto_da_barra, 1, branco)
    tela.blit(text, (20, eixo_y))

def envolucro_dados_disco():
    mostrar_info_disco()
    mostra_uso_disco(410, 390)
####################################################################################################################
def resumo():
    superficie_info_resumo.fill(branco)
    mostrar_texto_resumo(superficie_info_resumo, "disco_livre", "Disco livre:", 10)
    mostrar_texto_resumo(superficie_info_resumo, "memoria_livre", "Memoria livre:", 30)
    mostrar_texto_resumo(superficie_info_resumo, "ip_rede", "IP:", 50)
    tela.blit(superficie_info_resumo, (0, 0))    
    
def mostrar_texto_resumo(s1, chave, nome, pos_y):
    disco = psutil.disk_usage('/')
    mem = psutil.virtual_memory()
    
    texto = font.render(nome, True, preto)
    s1.blit(texto, (40, pos_y))
    
    disco_livre = str(round(disco.free/(1024**3), 2)) + "GB"
    memoria_livre = str(round(mem.available/(1024**3), 2))
    ip = resumoGetNewIp()
    
    if chave == "disco_livre":
        s1.blit(font.render(disco_livre, True, preto), (155, pos_y))
        
    elif chave == "memoria_livre":
        s1.blit(font.render(memoria_livre, True, preto), (155, pos_y))
    
    elif chave == "ip_rede":
        meu_ip = ips[0][1]

        if meu_ip == '127.0.0.1':
            meu_ip = ips[1][1]

        s1.blit(font.render(meu_ip, True, preto), (155, pos_y))
####################################################################################################################
def mostrar_info_memoria():
    superficie_info_memoria.fill(branco)    

    titulo = font.render("** Informações de Memória **" ,1, azul)
    superficie_info_memoria.blit(titulo,(15, 30))

    mostrar_texto_memoria(superficie_info_memoria, "capacidade", "Capacidade:", 45)
    mostrar_texto_memoria(superficie_info_memoria, "disponivel", "Disponivel:", 60)        
    tela.blit(superficie_info_memoria, (0, 0))    

def mostrar_texto_memoria(s1, chave, nome, pos_y):    
    mem = psutil.virtual_memory()
    texto = font.render(nome, True, preto)
    s1.blit(texto, (40, pos_y))
    
    capacidade = round(mem.total/(1024**3),  2)
    disponivel = round(mem.available/(1024**3), 2)
    
    memoria_usada = str(capacidade) + "GB"
    memoria_disponivel = str(disponivel) + "GB"    
    
    if chave == "capacidade":
        s1.blit(font.render(memoria_usada, True, preto), (155, pos_y))
        
    elif chave == "disponivel":
        s1.blit(font.render(memoria_disponivel, True, preto), (155, pos_y))
    
    tela.blit(superficie_info_memoria, (0, 0))    
        
def mostra_uso_memoria():
    memoria = psutil.virtual_memory()
    largura = largura_tela - 2 * 20
    pygame.draw.rect(superficie_grafico_memoria, cinza, (30, 5, largura, 5))
    tela.blit(superficie_grafico_memoria, (0, 270))
    
    largura = largura * memoria.percent / 100
    pygame.draw.rect(superficie_grafico_memoria, azul, (30, 5, largura, 5))

    tela.blit(superficie_grafico_memoria, (0, 270))
    total = round(memoria.total / (1024 * 1024 * 1024), 2)
    
    percentagem = memoria.percent
    texto_da_barra = ('Percentual usado: {}% (Total: {} GB)'.format(percentagem, total))
    text = font.render(texto_da_barra, 1, branco)
    tela.blit(text, (20, 240))
    
def envolucro_dados_memoria():
    mostrar_info_memoria()
    mostra_uso_memoria()
####################################################################################################################
def envolucro_arquivos():
    apresenta_dados_arquivos()

def mostrar_dados_diretorio():
    lista = os.listdir()

    for i in lista:
        arquivos[i] = []
        arquivos[i].append(os.stat(i).st_size)
        arquivos[i].append(os.stat(i).st_ctime)
        arquivos[i].append(os.stat(i).st_mtime)

    tituloInfo = 'Arquivos do diretório:'
    titulo_tamanho = '{:>5}'.format('Tamanho')
    titulo_data_criacao = '{:>30}'.format('Criação')
    titulo_data_modificacao = '{:>38}'.format('Modificação')
    titulo_nome = '{:>38}'.format('Nome')
    titulo = titulo_tamanho + titulo_data_criacao + titulo_data_modificacao + titulo_nome
    textoTituloInfo = font.render(tituloInfo, 1, branco)
    tela.blit(textoTituloInfo, (20, 20))
    textoTitulo = font.render(titulo, 1, branco)
    tela.blit(textoTitulo, (20, 60))

    #rquivos = dados_organizados

def apresenta_dados_arquivos():
    espacos = 100
    for i in arquivos:
        tamanho_arquivo = arquivos[i][0]/1024
        
        tamanho_formatado = '{:>10}'.format(str('{:.2f}'.format(tamanho_arquivo) + 'KB'))
        data_criacao = '{:>30}'.format(time.ctime(arquivos[i][0]))
        time_mod = '{:>30}'.format(time.ctime(arquivos[i][1]))
        nomeArquivo = '{:>30}'.format(i)

        textoArqDir = font.render(tamanho_formatado + data_criacao + time_mod + nomeArquivo, 1, branco)
        tela.blit(textoArqDir, (15, espacos))
        espacos += 25
####################################################################################################################
def mostrar_texto_rede():   
    superficie_info_memoria.fill(branco)
    
    titulo = font.render("** Informações de Rede **" , 1, azul)
    superficie_info_memoria.blit(titulo,(15, 30))

    espacos = 100

    for ip in ips:
        nome_interface_formatada = '{:>10}'.format(str(ip[0]))
        ip_formatada = '{:>10}'.format(str(ip[1]))
        gateway_formatada = '{:>10}'.format(str(ip[2]))
        
        texto = font.render('Interface:' + nome_interface_formatada + '{:>15}'.format('- Ip: ') + ip_formatada + '{:>15}'.format('- Mascara: ') + gateway_formatada, 1, preto)

        superficie_info_memoria.blit(texto, (0, espacos))
        espacos += 25

    # lançar mensagem de informação
    if len(hosts) == 0:
        texto_atencao = font.render('Lendo dados da rede. Aguarde...', 10, vermelho)
        superficie_info_memoria.blit(texto_atencao, (260, 185))


    for host in hosts:
        host_name = ""

        if host.name != "":
            host_name = host.name
        else:
            host_name = "NÃO LOCALIZADO"

        cor = ""
        
        if host_name != "NÃO LOCALIZADO":
            cor = (255, 255, 255)
        else:
            cor = (255, 0, 0)        

        texto = font.render(host.ip + ': Nome: ' + host_name, 1, azul)
        tela.fill(preto)
        tela.blit(texto, (15, espacos + 5))
        espacos += 15

        for porta in host.ports:
            detalhe_porta = font.render("Porta: " + str(porta.port) + " - Estado: " + porta.state ,1, azul)
            tela.blit(detalhe_porta, (15, espacos))
            espacos += 15
        
        espacos += 10

    tela.blit(superficie_info_memoria, (0, 0))

def mostra_texto(s1, nome, pos_y):
    text = font.render(nome, True, branco)
    superficie_info_rede.blit(text, (10, pos_y))

def getNewIp(sistema):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == sistema:
                yield (interface, snic.address, snic.netmask)

def resumoGetNewIp():
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

def verifica_hosts_validos(base_ip):
    """Verifica todos os host com a base_ip entre 1 e 255 retorna uma lista com todos os host que tiveram resposta 0 (ativo)"""
    print("Mapeando\r")
    host_validos = []
    return_codes = dict()
    for i in range(1, 255):
    
        return_codes[base_ip + '{0}'.format(i)] = retorna_codigo_ping(base_ip + '{0}'.format(i))
        if i %20 ==0:
            print(".", end = "")

        if return_codes[base_ip + '{0}'.format(i)] == 0:
            host_validos.append(base_ip + '{0}'.format(i))

    print("\nMapeamento pronto...")

    return host_validos

def detalhar_host(host_validos):
    """Obtendo nome do host"""
    nm = nmap.PortScanner()
    for host in host_validos:
        print('**************************************************************\r')
        try:            
            nm.scan(host)
            host_ = Host(host, nm[host].hostname())            
            #print('O IP', host, 'possui o nome', nm[host].hostname())

            for proto in nm[host].all_protocols():
                print('----------')
                print('Protocolo : %s' % proto)

            lport = nm[host][proto].keys()
            for port in lport:
                port_ = Port(port, nm[host][proto][port]['state'])
                host_.ports.append(port_)

        except:
            print(':rocket: Exception')
            pass

        hosts.append(host_)

executando = False
executou = False
ips = resumoGetNewIp()

def envolucro_detalhar_host():
        
    meu_ip = ips[0][1]

    if meu_ip == '127.0.0.1':
        print('meu_ip = broadcast ->>> realizando troca')
        meu_ip = ips[1][1]

    print('Ip que será utilizado como base', meu_ip)
    ip_string = meu_ip

    ip_lista = ip_string.split('.')
    base_ip = ".".join(ip_lista[0:3]) + '.'
    print("O teste será feito na sub rede: ", base_ip)

    hosts_localizados = verifica_hosts_validos(base_ip)
    
    print('Verificar nomes dos hosts', hosts_localizados, '\r')
    detalhar_host(hosts_localizados)
###################################################################################################################
def envolucro_processo():
    # só obtem listagem de processos uma vez
    if len(lista_de_processos) == 0:
        get_dados_processo()

    info_processos()

def get_dados_processo():
    pids = psutil.pids()
    total_de_processos = 0

    for pid in pids:
        try:            
            nome = psutil.Process(pid).name()
            tamanho_nome = len(nome)

            if tamanho_nome <= 15 and pid != 1:
                percent_uso = psutil.Process(pid).memory_percent()
                memoria_usada = psutil.Process(pid).memory_info().rss / 1024/1024
                threads_usadas = psutil.Process(pid).num_threads()
                tempo_usuario = str(psutil.Process(pid).cpu_times().user) + ' s'
                data_criacao = time.ctime(psutil.Process(pid).create_time())

                aux_processo = Processo(pid, nome, percent_uso
                    , memoria_usada, threads_usadas, tempo_usuario, data_criacao)

                lista_de_processos.append(aux_processo)
            
        except:
            print(':error: erro ao obter dados do processo')

        if total_de_processos == 20:
            break
        total_de_processos += 1

def info_processos():
    tela.fill(branco)

    titulo1 = 'Lista dos 20 primeiros processos em execução'
    text1 = font.render(titulo1, 1, preto)
    tela.blit(text1, (15, 30))

    titulo2 = 'PID       Nome         Percent. Uso (%)       Mem. Usada (MB)       Threads        Tempo Exec.             Criação'
    
    text2 = font.render(titulo2, 1, preto)
    tela.blit(text2, (15, 60))

    espacos = 90

    for processo in lista_de_processos:

        text_pid = str(processo.pid) + ' - '
        text_nome = '{:>15}'.format(processo.nome)
        text_percentual_uso = '{:>20}'.format(processo.percentual_uso)
        text_memoria_usada = '{:>25}'.format(processo.memoria_usada)
        text_threads_processo = '{:>30}'.format(processo.threads_processo)
        text_tempo_usuario = '{:>25}'.format(processo.tempo_usuario)
        text_data_criacao = '{:>35}'.format(processo.data_criacao)

        text_formatado = text_pid + text_nome + text_percentual_uso + text_memoria_usada + text_threads_processo + text_tempo_usuario + text_data_criacao

        text3 = font.render(text_formatado, 1, preto)
        tela.blit(text3, (15, espacos))
        espacos += 20

####################################################################################################################
def get_envolucro(posicao):
    if posicao == 0:
        envolucro_dados_cpu()

        if len(arquivos) == 0:
            thread2 = ThreadArquivos(1, "Thread-2", 1)
            thread2.start()

        if len(hosts) == 0 and not executou:            
            thread1 = ThreadRede(1, "Thread-1", 1)
            thread1.start()

    elif posicao == 1:
        envolucro_dados_memoria()

    elif posicao == 2:
        envolucro_dados_disco()

    elif posicao == 3:
        mostrar_texto_rede()

    elif posicao == 4:
        envolucro_arquivos()

    elif posicao == 5:    
        envolucro_processo()

    elif posicao == 6:
        resumo()
####################################################################################################################

while not terminou:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminou = True
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                posicao_atual = posicao_atual + 1
                
            elif event.key == pygame.K_LEFT:
                posicao_atual = posicao_atual - 1
            
            elif event.key == pygame.K_SPACE:
                posicao_atual = 6

#carrossel           
    if count == 60:
        tela.fill(preto)
        
        if posicao_atual < 0:
            posicao_atual = 6
            
        elif posicao_atual > 6:
            posicao_atual = 0
        
        executando = True
        get_envolucro(posicao_atual)
        executou = True
        
        count = 0    
        
    pygame.display.update()
    
    clock.tick(60)
    count = count + 1
        
pygame.display.quit()
