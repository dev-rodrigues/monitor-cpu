import pygame, datetime
import socket, pickle
import os, threading
import time

## controle aplicacao
variaveis = {
    'vermelho': (255, 0, 0),
    'azul': (29, 51, 74),
    'preto': (0, 0, 0),
    'branco': (255, 255, 255),
    'cinza': (128, 128, 128),
    'grafite': (128, 128, 128),
    'posicionamento-paginacao': (290, 530),
    'posicionamento-instrucao': (290, 560),
    'tamanho-minimo-palavra': 30,
    'porta': 9999,
    'posicao_atual': 0,
    'pagina': 1,
    'tamanho_tela': (800, 600),
    'diretorio_atual': '',
    'cache_arquivo': []
}

# inicio configuracoes pygame
#
largura_tela = 800
altura_tela = 600

terminou = False
count = 60

variaveis['diretorio_atual'] = os.getcwd()

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Projeto de bloco - Carlos Henrique")
pygame.display.init()

pygame.font.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

superficie_info_cpu = pygame.surface.Surface((largura_tela, int(altura_tela/3)))

#
# fim configuracoes pygame

# inicio thread
#
class ThreadLog(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter        

    def run(self):
        print('ThreadLog >> iniciando escrita do log') 
        while True:
            if len(variaveis['cache_arquivo'])> 1:
                logs = variaveis['cache_arquivo']
                log_aux = logs[len(logs) - 1]
                set_log(log_aux)
                del(logs[len(logs) - 1])

t = ThreadLog(1, 'ThreadLog', 2)
t.start()

#
# fim thread

# inicio socket
#
socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                 

try:
    socket_.connect((socket.gethostname(), 9999))
except:
    print('ERRO AO CONECTAR COM O SERVIDOR')
    os._exit(1)

def request(message):
    try:
        socket_.send(message.encode('ascii'))
        received = socket_.recv(90000)
        response = pickle.loads(received)
        return response
    except:
        print('ERRO AO CONECTAR COM O SERVIDOR')
        os._exit(1)

#
# fim socket

# inicio exibir informações em tela
#
def get_envolucro_cpu():
    log_ = 'REQUEST: > ' + str(datetime.datetime.now()) + ' > cpu'
    variaveis['cache_arquivo'].append(log_)
    response_cpu = request('cpu')
    log_ = 'RESPONSE: > ' + str(datetime.datetime.now()) + ' > ' + str(response_cpu)
    variaveis['cache_arquivo'].append(log_)

    set_info_cpu(response_cpu)
    set_grafico_cpu(superficie_info_cpu, response_cpu)

def get_envolucro_memoria():
    log_ = 'REQUEST: > ' + str(datetime.datetime.now()) + ' > memoria'
    variaveis['cache_arquivo'].append(log_)

    response_memoria = request('memoria')
    log_ = 'RESPONSE: > ' + str(datetime.datetime.now()) + ' > ' + str(response_memoria)
    variaveis['cache_arquivo'].append(log_)

    set_info_memoria(response_memoria)
    set_grafico_memoria(response_memoria)

def get_envolucro_disco():
    log_ = 'REQUEST: > ' + str(datetime.datetime.now()) + ' > disco'
    variaveis['cache_arquivo'].append(log_)

    response_disco = request('disco')
    log_ = 'RESPONSE: > ' + str(datetime.datetime.now()) + ' > ' + str(response_disco)
    variaveis['cache_arquivo'].append(log_)

    set_info_disco(response_disco)
    set_grafico_disco(response_disco)

def get_envolucro_rede():
    log_ = 'REQUEST: > ' + str(datetime.datetime.now()) + ' > ips'
    variaveis['cache_arquivo'].append(log_)

    response_ips = request('ips')
    log_ = 'RESPONSE: > ' + str(datetime.datetime.now()) + ' > ' + str(response_ips)
    variaveis['cache_arquivo'].append(log_)

    log_ = 'REQUEST: > ' + str(datetime.datetime.now()) + ' > trafego'
    variaveis['cache_arquivo'].append(log_)

    response_trafego = request('trafego')
    log_ = 'RESPONSE: > ' + str(datetime.datetime.now()) + ' > ' + str(response_trafego)
    variaveis['cache_arquivo'].append(log_)

    log_ = 'REQUEST: > ', str(datetime.datetime.now()), ' > ' , ' rede'
    variaveis['cache_arquivo'].append(log_)

    response_host = request('rede')
    log_ = 'RESPONSE: > ' + str(datetime.datetime.now()) + ' > ' + str(response_host)
    variaveis['cache_arquivo'].append(log_)

    set_info_rede(response_ips, response_trafego, response_host)
    set_info_hosts_rede(response_host)

response_cache_arquivo = ''
def get_envolucro_arquivo():
    global response_cache_arquivo

    if response_cache_arquivo != '' and int(variaveis['pagina']) > int(response_cache_arquivo[2]['total_paginas']):
        variaveis['pagina'] = int(response_cache_arquivo[1]['total_paginas'])

    log_ = 'REQUEST: > ' + str(datetime.datetime.now()) + ' > arquivos/' + str(variaveis['pagina'])
    variaveis['cache_arquivo'].append(log_)

    response_arquivos = request('arquivos/' + str(variaveis['pagina']))
    response_cache_arquivo = response_arquivos

    log_ = 'RESPONSE: > ' + str(datetime.datetime.now()) + ' > ' + str(response_arquivos)
    variaveis['cache_arquivo'].append(log_)

    set_info_arquivo(response_arquivos)

response_cache_processo = ''
def get_envolucro_processos():
    global response_cache_processo

    if response_cache_processo != '' and int(variaveis['pagina']) > int(response_cache_processo['total_paginas']):
        variaveis['pagina'] = int(response_cache_processo['total_paginas'])

    log_ = 'REQUEST: > ' + str(datetime.datetime.now()) + ' > processo/' + str(variaveis['pagina'])
    variaveis['cache_arquivo'].append(log_)

    response_processos = request('processo/' + str(variaveis['pagina']))
    response_cache_processo = response_processos

    log_ = 'RESPONSE: > ' + str(datetime.datetime.now()) + ' > ' + str(response_processos)
    variaveis['cache_arquivo'].append(log_)

    set_info_processo(response_processos)

def get_envolucro_resumo():
    log_ ='REQUEST: > ' + str(datetime.datetime.now()) + ' > resumo'
    variaveis['cache_arquivo'].append(log_)

    response_resumo = request('resumo')
    log_ ='RESPONSE: > ' + str(datetime.datetime.now()) + ' > ' + str(response_resumo)
    variaveis['cache_arquivo'].append(log_)

    set_info_resumo(response_resumo)

def get_envolucro(posicao):

    if posicao == 0:
        get_envolucro_cpu()
    
    elif posicao == 1:
        get_envolucro_memoria()
    
    elif posicao == 2:        
        get_envolucro_disco()

    elif posicao == 3:        
        get_envolucro_rede()

    elif posicao == 4:
        get_envolucro_arquivo()

    elif posicao == 5:    
        get_envolucro_processos()

    elif posicao == 6:
        get_envolucro_resumo()

def set_info_cpu(cpu):
    superficie_info_cpu.fill(variaveis['grafite'])

    # label
    text_arquitetura = font.render('Arquitetura:', True, (30, 0, 0))
    superficie_info_cpu.blit(text_arquitetura, (40, 30))
    # valor
    valor_arquitetura = font.render(cpu['arquitetura'], True, (30, 0, 0))
    superficie_info_cpu.blit(valor_arquitetura, (180, 30))

    # label
    text_bits = font.render('Total Bits:', True, (30, 0, 0))
    superficie_info_cpu.blit(text_bits, (40, 50))
    # valor
    valor_bits = font.render(cpu['bits'], True, (30, 0, 0))
    superficie_info_cpu.blit(valor_bits, (180, 50))

    # label
    text_frequencia = font.render('Frequência:', True, (30, 0, 0))
    superficie_info_cpu.blit(text_frequencia, (40, 70))
    # valor
    valor_frquencia = font.render(cpu['frequencia'], True, (30, 0, 0))
    superficie_info_cpu.blit(valor_frquencia, (180, 70))

    # label
    text_nucleo = font.render('Núcleos (físico):', True, (30, 0, 0))
    superficie_info_cpu.blit(text_nucleo, (40, 90))
    # valor
    valor_nucleo = font.render(cpu['nucleos'], True, (30, 0, 0))
    superficie_info_cpu.blit(valor_nucleo, (180, 90))

    # label
    texto_nome = font.render('Nome:', True, variaveis['preto'])
    superficie_info_cpu.blit(texto_nome, (40, 110))
    # valor
    valor_nome = font.render(cpu['nome'], True, variaveis['preto'])
    superficie_info_cpu.blit(valor_nome, (180, 110))

    tela.blit(superficie_info_cpu, (0,0))

def set_grafico_cpu(s, cpu):
    l_cpu_percent = cpu['l_cpu_percent']

    s.fill(variaveis['grafite'])

    capacidade = cpu['capacidade']
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

def set_info_memoria(memoria):
    tela.fill(variaveis['grafite'])

    titulo = font.render("** Informações de Memória **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 10))

    # titulo
    texto = font.render('Capacidade', True, variaveis['preto'])
    tela.blit(texto, (15, 60))
    # valor
    tela.blit(font.render(str(memoria['capacidade']) + 'GB', True, variaveis['preto']), (155, 60))

    #titulo
    texto = font.render('Disponível', True, variaveis['preto'])
    tela.blit(texto, (15, 80))
    # valor
    tela.blit(font.render(str(memoria['disponivel']), True, variaveis['preto']), (155, 80))

def set_grafico_memoria(memoria):
    memoria = memoria['memoria']

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

def set_info_disco(memoria):
    tela.fill(variaveis['grafite'])

    titulo = font.render("** Informações do Disco **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 10))
    

    # titulo
    texto = font.render('Capacidade', True, variaveis['preto'])
    tela.blit(texto, (15, 60))
    # valor
    tela.blit(font.render(str(memoria['total']) + ' GB', True, variaveis['preto']), (155, 60))

    #titulo
    texto = font.render('Disponível', True, variaveis['preto'])
    tela.blit(texto, (15, 80))
    # valor
    tela.blit(font.render(str(memoria['livre']) + ' GB', True, variaveis['preto']), (155, 80))

    #titulo
    texto = font.render('Usado', True, variaveis['preto'])
    tela.blit(texto, (15, 100))
    # valor
    tela.blit(font.render(str(memoria['usado']) + ' GB', True, variaveis['preto']), (155, 100))

def set_grafico_disco(memoria):
    disco_aux = memoria['disco']

    total = memoria['total']
    largura = largura_tela - 2 * 20

    pygame.draw.rect(tela, variaveis['branco'], (15, 270, largura, 5))
    
    consumo = (largura * disco_aux.percent) / 100
    pygame.draw.rect(tela, variaveis['azul'], (15, 270, consumo, 5))

    texto_da_barra = ('Uso de Disco: {}% (Total: {} GB)'.format(disco_aux.percent, total))
    texto = font.render(texto_da_barra, 1, variaveis['branco'])
    tela.blit(texto, (20, 240))

    # instrucao navegacao
    instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
    tela.blit(instrucao, variaveis['posicionamento-instrucao'])  

def set_info_rede(ips, trafegos, hosts):
    tela.fill(variaveis['grafite'])

    titulo = font.render("** Informações de Rede **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 10))
    
    titulo = font.render("Interface                              IP                        Máscara             Pct. Enviado       Pct. Recebido" , 1, variaveis['preto'])
    tela.blit(titulo, (15, 75))


    espacos = 100

    for host in ips:

        interface = host[0]
        trafego_da_interface = get_trafego_da_interface(interface, trafegos)

        ip = str(host[1])

        if ip !='127.0.0.1':            

            pct_recebido = size_format(trafego_da_interface['pacotes_recebidos']) 
            pct_enviado = size_format(trafego_da_interface['pacotes_enviados'])

            pct_enviado_formatado = '{:^30}'.format(str(pct_enviado))
            pct_recebido_formatado = '{:^15}'.format(str(pct_recebido))

            nome_interface_formatada = get_nova_string(str(host[0]))
            
            ip_formatada = str(host[1])
            ip_formatada_ = '{:<20}'.format(ip_formatada)

            mascara = str(host[2])
            mascara_formatada = '{:^15}'.format(mascara)

            texto = font.render(nome_interface_formatada + ip_formatada_ +  mascara_formatada + pct_enviado_formatado + pct_recebido_formatado, 1, variaveis['preto'])
            
            tela.blit(texto, (15, espacos))
            espacos += 25

    # exibir msg de informacao: escaneando rede
    if hosts == 'NoNe':
        texto_atencao = font.render('Lendo dados da rede. Aguarde...', 10, variaveis['vermelho'])
        tela.blit(texto_atencao, (260, 185))

def set_info_hosts_rede(hosts):

    espacos = 300

    if hosts != 'NoNe':
        for host in hosts:
            host_name = ""

            if host['nome'] != "":
                host_name = host['nome']

            else:
                host_name = "NÃO IDENTIFICADO"

            cor = ""

            if host_name == "NÃO IDENTIFICADO":
                cor = variaveis['vermelho']
            else:
                cor = variaveis['azul']

            texto = font.render(host['ip'] + ': Nome: ' + host_name, 1, variaveis['azul'])
            
            tela.blit(texto, (15, espacos + 5))
            espacos += 15

            for porta in host['portas']:
                porta_label = font.render("Porta: ", 1, variaveis['branco'])            
                tela.blit(porta_label, (15, espacos + 10))

                porta_text = font.render(str(porta['porta']), 1, variaveis['branco'])
                tela.blit(porta_text, (70, espacos + 10))

                estado_label = font.render("Estado: ", 1, variaveis['branco'])            
                tela.blit(estado_label, (140, espacos + 10))
                
                estado = font.render(porta['estado'], 1, variaveis['branco'])            
                tela.blit(estado, (210, espacos + 10))

                espacos += 15

            espacos += 20

    # instrucao navegacao
    instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
    tela.blit(instrucao, variaveis['posicionamento-instrucao'])

def set_info_arquivo(response):

    tela.fill(variaveis['grafite'])

    titulo = font.render("** Arquivos do diretório **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 10))

    diretorio = font.render("> " + response[0], 1, variaveis['preto'])
    tela.blit(diretorio, (15, 45))

    titulo = font.render("Nome                                               Data Criação                      Data Modificação             Tamanho" , 1, variaveis['preto'])
    tela.blit(titulo, (15, 75))

    espacos = 100
    
    tempo_execucao = response[1]

    arquivos = response[2]
    total_paginas = arquivos['total_paginas']
    pagina_atual = arquivos['pagina_atual']

    for arquivo in arquivos['elementos']:

        tamanho_arquivo = size_format(arquivo['tamanho'])
                
        nome_arquivo = get_nova_string(arquivo['nome'])
        texto_formatado = font.render(nome_arquivo , 1, variaveis['preto'])
        tela.blit(texto_formatado, (15, espacos))

        data_criacao = datetime.datetime.fromtimestamp(arquivo['data_criacao']).strftime("%d-%m-%Y %H:%M:%S")
        texto_formatado = font.render(data_criacao , 1, variaveis['preto'])
        tela.blit(texto_formatado, (300, espacos))

        
        data_modificacao = datetime.datetime.fromtimestamp(arquivo['data_modificacao']).strftime("%d-%m-%Y %H:%M:%S")
        data_modificacao_formatado = font.render(data_modificacao , 1, variaveis['preto'])
        tela.blit(data_modificacao_formatado, (500, espacos))
        
        tamanho_arquivo_formatado = font.render(tamanho_arquivo, 1, variaveis['preto'])
        tela.blit(tamanho_arquivo_formatado, (700, espacos))
        
        espacos += 25
    
    get_paginar(total_paginas, pagina_atual)

    informacao = font.render(tempo_execucao[0], True, variaveis['branco'])
    tela.blit(informacao, (15, 480))

    informacao = font.render(tempo_execucao[1], True, variaveis['branco'])
    tela.blit(informacao, (15, 500))

    # instrucao navegacao
    instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
    tela.blit(instrucao, variaveis['posicionamento-instrucao'])

def set_info_processo(response):
    total_de_paginas = response['total_paginas']
    pagina_atual = response['pagina_atual']


    tela.fill(variaveis['grafite'])

    titulo = font.render("** Lista dos processos em execução **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 10))

    titulo = font.render("    PID        % Uso        Mem. Usada     Threads Usada            Tempo                      Nome" , 1, variaveis['preto'])
    tela.blit(titulo, (15, 55))

    espacos = 100

    processos = response['elementos']


    for processo in processos:

        text_pid = '{:<15}'.format(str(processo['pid']))
        texto = font.render(text_pid, 1, variaveis['preto'])
        tela.blit(texto, (40, espacos))

        text_percentual_uso = '{:<20}'.format(str(format(processo['percentual_uso'], '.2f')))
        texto = font.render(text_percentual_uso, 1, variaveis['preto'])
        tela.blit(texto, (110, espacos))

        text_memoria_usada = '{:<20}'.format(size_format(processo['memoria_usada']))
        texto = font.render(text_memoria_usada, 1, variaveis['preto'])
        tela.blit(texto, (220, espacos))

        text_threads_processo = '{:<20}'.format(str(format(processo['threads_processo'], '.2f')))
        texto = font.render(text_threads_processo, 1, variaveis['preto'])
        tela.blit(texto, (350, espacos))

        texto_tempo_exec = '{:<20}'.format(processo['tempo_usuario'])
        texto = font.render(texto_tempo_exec, 1, variaveis['preto'])
        tela.blit(texto, (490, espacos))

        text_nome = '{:<30}'.format(processo['nome'])
        texto = font.render(text_nome, 1, variaveis['preto'])
        tela.blit(texto, (620, espacos))

        espacos += 25
    
    get_paginar(total_de_paginas, pagina_atual)
    
    # instrucao navegacao
    instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
    tela.blit(instrucao, variaveis['posicionamento-instrucao'])

def set_info_resumo(response):
    tela.fill(variaveis['grafite'])

    titulo = font.render("** Resumo dos dados coletados **" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 10))

    titulo = font.render("CPU" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 60))

    processador = response['cpu']
    disco = response['disco']
    
    memoria_total = response['memoria_capacidade']
    memoria_disponivel = response['memoria_disponivel']
    memoria_usada = memoria_total - memoria_disponivel

    # obtem o ip do usuario
    host = response['ips'][0][1]
    if host == '127.0.0.1':
        host = response['ips'][1][1]

    # titulo
    texto = font.render('Processador:', True, variaveis['preto'])
    tela.blit(texto, (15, 80))
    # valor
    tela.blit(font.render(processador['nome'], True, variaveis['preto']), (155, 80))

    # titulo
    texto = font.render('Frequência:', True, variaveis['preto'])
    tela.blit(texto, (15, 100))
    # valor
    tela.blit(font.render(processador['frequencia'], True, variaveis['preto']), (155, 100))

    # titulo
    texto = font.render('Bits:', True, variaveis['preto'])
    tela.blit(texto, (15, 120))
    # valor
    tela.blit(font.render(processador['bits'], True, variaveis['preto']), (155, 120))
    
    #
    tela.blit(font.render('----------------------------------------------------------', True, variaveis['branco']), (180, 150))

    titulo = font.render("Disco" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 170))

    # titulo
    texto = font.render('Total:', True, variaveis['preto'])
    tela.blit(texto, (15, 190))
    # valor
    tela.blit(font.render(size_format(disco['disco'][0]), True, variaveis['preto']), (155, 190))

    # titulo
    texto = font.render('Livre:', True, variaveis['preto'])
    tela.blit(texto, (15, 210))
    # valor
    tela.blit(font.render(size_format(disco['disco'][2]), True, variaveis['preto']), (155, 210))

    # titulo
    texto = font.render('Usado:', True, variaveis['preto'])
    tela.blit(texto, (15, 230))
    # valor
    tela.blit(font.render(size_format(disco['disco'][1]), True, variaveis['preto']), (155, 230))

    #
    tela.blit(font.render('----------------------------------------------------------', True, variaveis['branco']), (180, 260))

    titulo = font.render("Memória" , 1, variaveis['azul'])
    tela.blit(titulo, (15, 280))

    # titulo
    texto = font.render('Total:', True, variaveis['preto'])
    tela.blit(texto, (15, 300))
    # valor
    tela.blit(font.render(str(memoria_total) + 'GB', True, variaveis['preto']), (155, 300))

    # titulo
    texto = font.render('Livre:', True, variaveis['preto'])
    tela.blit(texto, (15, 320))
    # valor
    tela.blit(font.render(str(memoria_disponivel) + 'GB', True, variaveis['preto']), (155, 320))

    # titulo
    texto = font.render('Usado:', True, variaveis['preto'])
    tela.blit(texto, (15, 340))
    # valor
    tela.blit(font.render(str((format(memoria_usada, '.2f'))) + 'GB', True, variaveis['preto']), (155, 340))

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

def get_trafego_da_interface(interface, trafegos):
    response = ''
    medicoes = trafegos[len(trafegos) - 1]

    for trafego in medicoes:
        if trafego['interface'] == interface:
            response = trafego
            break
    return response

def get_nova_string(palavra):
    palavra_aux = palavra

    tamanho_minimo = variaveis['tamanho-minimo-palavra']
    tamanho_palavra = len(palavra_aux)

    if tamanho_palavra > tamanho_minimo:
        # recorta a string
        palavra_aux = '{:.30}'.format(palavra)
    else:
        # adiciona espacos
        while tamanho_palavra != tamanho_minimo:
            palavra_aux = palavra_aux + " "
            tamanho_palavra = len(palavra_aux)

    return palavra_aux

def size_format(b):
    if b < 1000:
              return '%i' % b + 'B'
    elif 1000 <= b < 1000000:
        return '%.1f' % float(b/1000) + 'KB'
    elif 1000000 <= b < 1000000000:
        return '%.1f' % float(b/1000000) + 'MB'
    elif 1000000000 <= b < 1000000000000:
        return '%.1f' % float(b/1000000000) + 'GB'
    elif 1000000000000 <= b:
        return '%.1f' % float(b/1000000000000) + 'TB'

def get_paginar(total_paginas, pagina_atual):
    
    count_1 = 1
    count_2 = 1
    count_3 = 1
    count_4 = 1
    
    # instrucao paginacao
    if int(total_paginas) > 1:
        instrucao = font.render('Tecle + ou - para paginar', True, variaveis['azul'])
        tela.blit(instrucao, variaveis['posicionamento-paginacao'])

    for n in range(1, total_paginas + 1):

        cor = variaveis['branco']

        if n == int(pagina_atual):
            cor = variaveis['azul']

        if n <= 20:
            area = (30 * n, 300, 25, 25)
            pygame.draw.rect(tela, cor, area) 

            instrucao = font.render(str(n), True, variaveis['preto'])
            tela.blit(instrucao, ((30 * n) + 5, 300))

        elif n > 20 and n <= 40:
            area = (30 * count_1, 330, 25, 25)
            count_2 = 1
            pygame.draw.rect(tela, cor, area) 

            instrucao = font.render(str(n), True, variaveis['preto'])
            tela.blit(instrucao, ((30 * count_1) + 5, 330))
            count_2 = 1
            count_1 = count_1 + 1
            count_2 = 1

        elif n > 40 and n <=60:
            area = (30 * count_2, 360, 25, 25)
            pygame.draw.rect(tela, cor, area) 

            instrucao = font.render(str(n), True, variaveis['preto'])
            tela.blit(instrucao, ((30 * count_2) + 5, 360))
            count_2 = count_2 + 1

        elif n > 60 and n <=80:
            area = (30 * count_3, 390, 25, 25)
            pygame.draw.rect(tela, cor, area) 

            instrucao = font.render(str(n), True, variaveis['preto'])
            tela.blit(instrucao, ((30 * count_3) + 5, 390))
            count_3 = count_3 + 1
        
        elif n > 80 and n <= 100:
            area = (30 * count_4, 420, 25, 25)
            pygame.draw.rect(tela, cor, area) 

            instrucao = font.render(str(n), True, variaveis['preto'])
            tela.blit(instrucao, ((30 * count_4) + 5, 420))
            count_4 = count_4 + 1

def set_log(message):
    try:
        file = open(variaveis['diretorio_atual'] + '\\log-request.txt', 'a')
        file.write(str(message) + '\n')
        file.close()
    except:
        print('ERROR >>> SEM PERMISSÃO PARA ABRIR ARQUIVO')

#
#fim exibir informações em tela

while not terminou:
    # monitorando eventos   
    for event in pygame.event.get():

        # para a aplicacao
        if event.type == pygame.QUIT:
            terminou = True
        
        # monitora interação do usuario
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                variaveis['pagina'] = 1
                variaveis['posicao_atual'] = variaveis['posicao_atual'] + 1
                
            elif event.key == pygame.K_LEFT:
                variaveis['pagina'] = 1
                variaveis['posicao_atual'] = variaveis['posicao_atual'] - 1
            
            elif event.key == pygame.K_SPACE:
                variaveis['posicao_atual'] = 6

            elif event.key == pygame.K_KP_PLUS:
                variaveis['pagina'] = variaveis['pagina'] + 1
            
            elif event.key == pygame.K_KP_MINUS:
                if variaveis['pagina'] > 1:
                    variaveis['pagina'] = variaveis['pagina'] - 1
                else:
                    variaveis['pagina'] = 1

#carrossel           
    if count == 60:
        tela.fill(variaveis['grafite'])

        if variaveis['posicao_atual'] < 0:
            variaveis['posicao_atual'] = 6
            
        elif variaveis['posicao_atual'] > 6:
            variaveis['posicao_atual'] = 0
        
        get_envolucro(variaveis['posicao_atual'])

        count = 0    
        
    pygame.display.update()
    
    clock.tick(60)
    count = count + 1
        
pygame.display.quit()