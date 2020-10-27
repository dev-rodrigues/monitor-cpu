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

superficie_info_ips = pygame.surface.Surface((largura_tela, int(altura_tela/3)))

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
    mostrar_texto_disco(superficie_info_disco, "disco_usado", "Usado:", 10)
    mostrar_texto_disco(superficie_info_disco, "total_disco", "Total:", 30)
    mostrar_texto_disco(superficie_info_disco, "disco_livre", "Livre:", 50)
    
    tela.blit(superficie_info_disco, (0, 0))    

def mostrar_texto_disco(s1, chave, nome, pos_y):
    disco = psutil.disk_usage('.')
    texto = font.render(nome, True, preto)
    s1.blit(texto, (40, pos_y))
    
    disco_usado= str(round(disco.percent, 2)) + " %"
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
        s1.blit(font.render(ip[0][1], True, preto), (155, pos_y))
####################################################################################################################
def mostrar_info_memoria():
    superficie_info_memoria.fill(branco)    
    mostrar_texto_memoria(superficie_info_memoria, "capacidade", "Capacidade:", 10)
    mostrar_texto_memoria(superficie_info_memoria, "disponivel", "Disponivel:", 30)        
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
    texto_da_barra = ('Uso de Memória: {}% (Total: {} GB)'.format(percentagem, total))
    text = font.render(texto_da_barra, 1, branco)
    tela.blit(text, (20, 240))
    
def envolucro_dados_memoria():
    mostrar_info_memoria()
    mostra_uso_memoria()

####################################################################################################################
def envolucro_arquivos():
    arquivos = mostrar_dados_diretorio()
    apresenta_dados(arquivos)

def mostrar_dados_diretorio():
    lista = os.listdir()
    dados_organizados = {}

    for i in lista:
        dados_organizados[i] = []
        dados_organizados[i].append(os.stat(i).st_size)
        dados_organizados[i].append(os.stat(i).st_ctime)
        dados_organizados[i].append(os.stat(i).st_mtime)

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
    return dados_organizados

def apresenta_dados(arquivos):
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
    espacos = 100
    for ip in ips:        
        texto = font.render(ip[0] + ': ' + ip[1] + ' - ' + ip[2], 1, branco)
        tela.blit(texto, (15, espacos))
        espacos += 25
  
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
                #print ('Porta: %s\t Estado: %s' % (port, nm[host][proto][port]['state']))

        except:
            print(':rocket: Exception')
            pass

        hosts.append(host_)

meu_ip = ''
hosts = []
ips = resumoGetNewIp()

executando = False
executou = False

def envolucro_detalhar_host():
    executando = True

    print('Iniciando coleta de dados da rede:', executando)

    meu_ip = ips[0][1]
    print('Ip que será utilizado como base', meu_ip)
    ip_string = meu_ip

    ip_lista = ip_string.split('.')
    base_ip = ".".join(ip_lista[0:3]) + '.'
    print("O teste será feito na sub rede: ", base_ip)

    hosts_localizados = verifica_hosts_validos(base_ip)
    print ("Os host válidos são: ", hosts_localizados)

    print('Verifica nome do host\r')
    detalhar_host(hosts_localizados)

    executou = True
    print('Processo finalizado', executou)


###################################################################################################################
def info_processos():
    pid = subprocess.Popen('cmd.exe').pid

    p = psutil.Process(pid)
    perc_mem = '{:.2f}'.format(p.memory_percent())
    mem = '{:.2f}'.format(p.memory_info().rss/1024/1024)

    tituloInfo = 'Informações sobre processos:'
    textoTituloInfo = font.render(tituloInfo, 1, branco)
    tela.blit(textoTituloInfo, (100, 160))

    texto1 = 'Nome: ' + p.name()
    texto01 = font.render(texto1, 1, branco)
    tela.blit(texto01, (100,200))

    texto2 = 'Executável: ' + p.exe()
    texto02 = font.render(texto2, 1, branco)
    tela.blit(texto02, (100,220))

    texto3 = 'Tempo de criação: ' + time.ctime(p.create_time())
    texto03 = font.render(texto3, 1, branco)
    tela.blit(texto03, (100,240))

    texto4 = 'Tempo de usuário: ' + str(p.cpu_times().user) + 's'
    texto04 = font.render(texto4, 1, branco)
    tela.blit(texto04, (100,260))

    texto5 = 'Tempo de sistema: ' + str(p.cpu_times().system) + 's'
    texto05 = font.render(texto5, 1, branco)
    tela.blit(texto05, (100,280))

    texto6 = 'Percentual de uso de CPU: ' + str(p.cpu_percent(interval=1.0)) + '%'
    texto06 = font.render(texto6, 1, branco)
    tela.blit(texto06, (100,300))

    texto7 = 'Percentual de uso de memória: ' + perc_mem + '%'
    texto07 = font.render(texto7, 1, branco)
    tela.blit(texto07, (100,320))

    texto8 = 'Uso de memória: ' + mem + 'MB'
    texto08 = font.render(texto8, 1, branco)
    tela.blit(texto08, (100,340))

    texto9 = 'Número de threads: ' + str(p.num_threads())
    texto09 = font.render(texto9, 1, branco)
    tela.blit(texto09, (100,360))
####################################################################################################################
def getEnvolucro(posicao):
    if posicao == 0:
        envolucro_dados_cpu()

        if len(hosts) == 0 and not executando and not executou:
            envolucro_detalhar_host()

    elif posicao == 1:
        envolucro_dados_memoria()

    elif posicao == 2:
        envolucro_dados_disco()

    elif posicao == 3:
        mostrar_texto_rede()

    elif posicao == 4:
        envolucro_arquivos()

    elif posicao == 5:        
        info_processos()

    elif posicao == 6:
        resumo()
####################################################################################################################
posicao_atual = 0
######################################################################################################################
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
                posicao_atual = 4

#carrossel           
    if count == 60:
        tela.fill(preto)
        
        if posicao_atual < 0:
            posicao_atual = 6
            
        elif posicao_atual > 6:
            posicao_atual = 0
            
        getEnvolucro(posicao_atual)
        
        count = 0    
        
    pygame.display.update()
    
    clock.tick(60)
    count = count + 1
        
pygame.display.quit()
