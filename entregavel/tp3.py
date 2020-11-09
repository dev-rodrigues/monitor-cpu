import pygame
import psutil
import cpuinfo
import platform

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
pygame.display.set_caption("Informações de CPU")
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
    s.fill(cinza)
    num_cpu = len(l_cpu_percent)
    x = y = 10
    desl = 10
    alt = s.get_height() - 2*y
    larg = (s.get_width()- 2*y - (num_cpu+1) * desl) / num_cpu
    d = x + desl
    
    for i in l_cpu_percent:
        pygame.draw.rect(s, vermelho, (d, y, larg, alt))
        pygame.draw.rect(s, azul, (d, y, larg, (1-i/100)*alt))
        d = d + larg + desl
        tela.blit(s, (0, 140))

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
    disco = psutil.disk_usage('/')
    texto = font.render(nome, True, preto)
    s1.blit(texto, (40, pos_y))
    disco_usado= str(round(disco.percent, 2)) + "%"
    total_disco = str(round(disco.used/(1024**3), 2)) + "GB"
    disco_livre = str(round(disco.free/(1024**3), 2)) + "GB"
    
    if chave == "total_disco":
        s1.blit(font.render(total_disco, True, preto), (155, pos_y))
    elif chave == "disco_usado":
        s1.blit(font.render(disco_usado, True, preto), (155, pos_y))
    elif chave == "disco_livre":
        s1.blit(font.render(disco_livre, True, preto), (155, pos_y))
        
def mostra_uso_disco():
    disco = psutil.disk_usage('/')
    larg = largura_tela - 2*20
    pygame.draw.rect(superficie_grafico_disco, azul, (20, 50, larg/2, 70))
    larg = larg * disco.percent/100
    pygame.draw.rect(superficie_grafico_disco, Dim, (20, 50, larg/2, 70))
    total = round(disco.total/(1024**3), 2)
    texto_barra = "Uso de Disco: (Total: " + str(total) + "GB):"
    texto = font.render(texto_barra, 1, branco)
    superficie_grafico_disco.blit(texto, (20, 10))
    tela.blit(superficie_grafico_disco, (0, 200))
    
def envolucro_dados_disco():
    mostrar_info_disco()
    mostra_uso_disco()

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
    ip = getIp()
    
    if chave == "disco_livre":
        s1.blit(font.render(disco_livre, True, preto), (155, pos_y))
    elif chave == "memoria_livre":
        s1.blit(font.render(memoria_livre, True, preto), (155, pos_y))
    elif chave == "ip_rede":
        s1.blit(font.render(ip, True, preto), (155, pos_y))
        
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
    mem = psutil.virtual_memory()
    larg = largura_tela - 2*20
    pygame.draw.rect(superficie_grafico_memoria, azul, (20, 50, larg/2, 70))    
    tela.blit(superficie_grafico_memoria, (0, 270))
    larg = larg * mem.percent / 100
    pygame.draw.rect(superficie_grafico_memoria, preto, (20, 5, larg, 5))
    tela.blit(superficie_grafico_memoria, (0, 270))
    total = round(mem.total / (1024 * 1024 * 1024), 2)
    percent = mem.percent
    msg = ('Uso de Memória: {}% (Total: {} GB)'.format(percent, total))
    text = font.render(msg, 1, branco)
    tela.blit(text, (20, 270))
    
def envolucro_dados_memoria():
    mostrar_info_memoria()
    mostra_uso_memoria()
####################################################################################################################
def getIp():
    plataforma = platform.system()
    dic_interfaces = psutil.net_if_addrs()

    if plataforma == 'Linux':
        ip = (dic_interfaces['wlp3s0'][0].address)
        return ip
    elif plataforma == "Windows":
        ip = (dic_interfaces['Ethernet'][1].address)
        return ip
    else:
        ip = (dic_interfaces['wlp3s0'][0].address)
        return ip
    
def mostrar_texto_rede():    
  plataforma = "IP: " + getIp()
  mostra_texto(superficie_info_rede, plataforma, 10)
  tela.blit(superficie_info_rede, (20, 0))
  
def mostra_texto(s1, nome, pos_y):
    text = font.render(nome, True, branco)
    superficie_info_rede.blit(text, (10, pos_y))
####################################################################################################################   
def getEnvolucro(posicao):
    if posicao == 0:
        envolucro_dados_cpu()
    elif posicao == 1:
        envolucro_dados_memoria()
    elif posicao == 2:
        envolucro_dados_disco()
    elif posicao == 3:
        mostrar_texto_rede()
    elif posicao == 4:
        resumo()
####################################################################################################################
posicao_atual = 0
posicao_cpu = 0
posicao_mem = 1
posicao_dis = 2
posicao_red = 3
posicao_res = 4
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

    if count == 60:
        tela.fill(preto)
        
        if posicao_atual < posicao_cpu:
            posicao_atual = 5
            
        elif posicao_atual > posicao_res:
            posicao_atual = 0
            
        getEnvolucro(posicao_atual)
        
        count = 0    
        
    pygame.display.update()
    
    clock.tick(60)
    count = count + 1
        
pygame.display.quit()