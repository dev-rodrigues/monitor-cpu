import pygame, math, datetime
import socket, time, pickle

## controle aplicacao
variaveis = {
    'vermelho': (255, 0, 0),
    'azul': (29, 51, 74),
    'preto': (0, 0, 0),
    'branco': (255, 255, 255),
    'cinza': (128, 128, 128),
    'grafite': (128, 128, 128),
    'posicionamento-instrucao': (250, 560),
    'tamanho-minimo-palavra': 15,
    'porta': 9999,
    'posicao_atual': 0
}

# inicio configuracoes pygame
#
largura_tela = 800
altura_tela = 600

terminou = False
count = 60
meu_ip = ''
lista_de_processos = []


tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Projeto de bloco - Carlos Henrique")
pygame.display.init()

pygame.font.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

superficie_info_cpu = pygame.surface.Surface((largura_tela, int(altura_tela/3)))
#
# fim configuracoes pygame

# inicio socket
socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_.connect((socket.gethostname(), 9999))

def request(message):
    socket_.send(message.encode('ascii'))
    received = socket_.recv(1024)
    response = pickle.loads(received)
    return response

# fim socket

# inicio exibir informações em tela
#
def get_envolucro_cpu():
    print('REQUEST: > ', datetime.datetime.now(), ' > ',' cpu')
    response_cpu = request('cpu')
    print('RESPONSE: > ', datetime.datetime.now(), ' > ',response_cpu)
    set_info_cpu(response_cpu)
    set_grafico_cpu(superficie_info_cpu, response_cpu)

def get_envolucro_memoria():
    print('REQUEST: > ', datetime.datetime.now(), ' > ' , ' memoria')
    response_memoria = request('memoria')
    print('RESPONSE: > ', datetime.datetime.now(), ' > ', response_memoria)
    set_info_memoria(response_memoria)
    set_grafico_memoria(response_memoria)

def get_envolucro_disco():
    print('REQUEST: > ', datetime.datetime.now(), ' > ' , ' disco')
    response_disco = request('disco')
    print('RESPONSE: > ', datetime.datetime.now(), ' > ', response_disco)
    set_info_disco(response_disco)
    set_grafico_disco(response_disco)

# def get_envolucro_rede():
#     set_info_rede()
#     set_info_hosts_rede()

# def get_envolucro_arquivo():
#     set_info_arquivo()

# def get_envolucro_processos():
#     set_info_processo()

# def get_envolucro_trafego_processo():
#     get_trafego_processo()
#     set_trafego_dados_processo()

# def get_envolucro_resumo():
#     set_info_resumo()

def get_envolucro(posicao):

    if posicao == 0:
        get_envolucro_cpu()
    
    elif posicao == 1:
        get_envolucro_memoria()
    
    elif posicao == 2:        
        get_envolucro_disco()
    # elif posicao == 3:
    #     get_envolucro_rede()
    # elif posicao == 4:
    #     get_envolucro_arquivo()
    # elif posicao == 5:    
    #     get_envolucro_processos()
    # elif posicao == 6:
    #     get_envolucro_resumo()

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
    tela.blit(titulo, (15, 30))

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
    tela.blit(titulo, (15, 30))

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

# def set_info_rede():
#     tela.fill(variaveis['grafite'])

#     titulo = font.render("** Informações de Rede **" , 1, variaveis['azul'])
#     tela.blit(titulo, (15, 30))

#     titulo = font.render("Interface                    IP                    Mascara                    Pct. Enviado              Pct. Recebido" , 1, variaveis['preto'])
#     tela.blit(titulo, (15, 55))

#     espacos = 100

#     hosts_aux = variaveis['hosts']

#     for host in hosts_aux:


#         interface = host[0]
#         trafego_da_interface = get_trafego_da_interface(interface)

#         ip = str(host[1])

#         if ip !='127.0.0.1':            

#             pct_recebido = round(trafego_da_interface.pacotes_recebidos / (1024 ** 2), 2)
#             pct_enviado = round(trafego_da_interface.pacotes_enviados / (1024 ** 2), 2)

#             pct_enviado_formatado = '{:>25}'.format(str(pct_enviado)) + 'MB'
#             pct_recebido_formatado = '{:>20}'.format(str(pct_recebido)) + 'MB'

#             nome_interface_formatada = get_nova_string(str(host[0]))
            
#             ip_formatada = get_nova_string(str(host[1]))
#             ip_formatada_ = '{:>20}'.format(ip_formatada)

#             mascara = get_nova_string(str(host[2]))
#             mascara_formatada = '{:>20}'.format(mascara)

#             texto = font.render(nome_interface_formatada + ip_formatada_ +  mascara_formatada + pct_enviado_formatado + pct_recebido_formatado, 1, variaveis['preto'])
            
#             tela.blit(texto, (15, espacos))
#             espacos += 25

#     # exibir msg de informacao: escaneando rede
#     if len(variaveis['hosts_detalhado']) == 0:
#         texto_atencao = font.render('Lendo dados da rede. Aguarde...', 10, variaveis['vermelho'])
#         tela.blit(texto_atencao, (260, 185))

# def set_info_hosts_rede():

#     espacos = 300

#     for host in variaveis['hosts_detalhado']:
#         host_name = ""

#         if host.name != "":
#             host_name = host.name

#         else:
#             host_name = "NÃO IDENTIFICADO"

#         cor = ""

#         if host_name != "NÃO IDENTIFICADO":
#             cor = variaveis['vermelho']

#         else:
#             cor = variaveis['azul']

#         texto = font.render(host.ip + ': Nome: ' + host_name, 1, variaveis['azul'])
        
#         tela.blit(texto, (15, espacos + 5))
#         espacos += 15

#         for porta in host.ports:
#             porta_label = font.render("Porta: ", 1, variaveis['branco'])            
#             tela.blit(porta_label, (15, espacos + 10))

#             porta_text = font.render(str(porta.port), 1, variaveis['branco'])
#             tela.blit(porta_text, (70, espacos + 10))

#             estado_label = font.render("Estado: ", 1, variaveis['branco'])            
#             tela.blit(estado_label, (140, espacos + 10))
            
#             estado = font.render(porta.state, 1, variaveis['branco'])            
#             tela.blit(estado, (210, espacos + 10))

#             espacos += 15

#         espacos += 20

#     # instrucao navegacao
#     instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
#     tela.blit(instrucao, variaveis['posicionamento-instrucao'])

  

# def set_info_arquivo():

#     tela.fill(variaveis['grafite'])

#     titulo = font.render("** Arquivos do diretório **" , 1, variaveis['azul'])
#     tela.blit(titulo, (15, 30))

#     arquivos = variaveis['arquivos']

    
#     titulo = font.render("Nome                       Data Criacao                        Data Modificacao                                 Tamanho" , 1, variaveis['preto'])
#     tela.blit(titulo, (15, 55))

#     espacos = 100
#     total_a_exibir = 0

#     for arquivo in arquivos:        

#         if total_a_exibir <= 10:

#             tamanho_aux = len(arquivo)

#             tamanho_arquivo = str(math.ceil(arquivos[arquivo][0] / 1024)) + 'KB'
                    
#             nome_arquivo = get_nova_string(arquivo)
#             texto_formatado = font.render(nome_arquivo , 1, variaveis['preto'])
#             tela.blit(texto_formatado, (15, espacos))

#             data_criacao = datetime.datetime.fromtimestamp(arquivos[arquivo][1]).strftime("%d-%m-%Y %H:%M:%S") #time.ctime(arquivos[arquivo][1])
#             texto_formatado = font.render(data_criacao , 1, variaveis['preto'])
#             tela.blit(texto_formatado, (140, espacos))

            
#             data_modificacao = datetime.datetime.fromtimestamp(arquivos[arquivo][2]).strftime("%d-%m-%Y %H:%M:%S") #time.ctime(arquivos[arquivo][2])
#             data_modificacao_formatado = font.render(data_modificacao , 1, variaveis['preto'])
#             tela.blit(texto_formatado, (400, espacos))
            

#             tamanho_arquivo_formatado = font.render(tamanho_arquivo, 1, variaveis['preto'])
#             tela.blit(tamanho_arquivo_formatado, (700, espacos))
            
#             espacos += 25
#             total_a_exibir += 1

#     time_leitura = variaveis['execucao_leitura_arquivos']

#     tempoFinal = time_leitura[0]
#     tempoUsado = time_leitura[1]

#     informacao = font.render(tempoFinal, True, variaveis['branco'])
#     tela.blit(informacao, (15, 480))

#     informacao = font.render(tempoUsado, True, variaveis['branco'])
#     tela.blit(informacao, (15, 500))

#     # instrucao navegacao
#     instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
#     tela.blit(instrucao, variaveis['posicionamento-instrucao'])

# def set_info_processo():
#     tela.fill(variaveis['grafite'])

#     titulo = font.render("** Lista dos 10 últimos processos em execução **" , 1, variaveis['azul'])
#     tela.blit(titulo, (15, 30))

#     titulo = font.render("PID            % Uso        Mem. Usada     Threads Usada           Tempo                        Nome" , 1, variaveis['preto'])
#     tela.blit(titulo, (15, 55))

#     espacos = 100

#     processos = variaveis['processos']

#     for processo in processos:

#         text_pid = '{:>0}'.format(str(processo.pid))

#         if len(str(processo.pid)) == 1:
#             text_percentual_uso = '{:>17}'.format(str(format(processo.percentual_uso, '.2f')))
#         else:
#             text_percentual_uso = '{:>15}'.format(str(format(processo.percentual_uso, '.2f')))

#         text_memoria_usada = '{:>20}'.format(str(format(processo.memoria_usada, '.2f') ))
#         text_threads_processo = '{:>20}'.format(str(format(processo.threads_processo, '.2f')))
#         text_tempo_usuario = '{:>20}'.format(processo.tempo_usuario)
#         text_nome = '{:>30}'.format(processo.nome)

#         texto_formatado = text_pid + text_percentual_uso + text_memoria_usada + text_threads_processo #+ text_tempo_usuario + text_nome

#         texto = font.render(text_tempo_usuario, 1, variaveis['preto'])
#         tela.blit(texto, (410, espacos))

#         texto = font.render(texto_formatado, 1, variaveis['preto'])
#         tela.blit(texto, (15, espacos))

#         texto = font.render(text_nome, 1, variaveis['preto'])
#         tela.blit(texto, (530, espacos))

#         espacos += 25
    
#     # instrucao navegacao
#     instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
#     tela.blit(instrucao, variaveis['posicionamento-instrucao'])

# def set_info_resumo():
#     tela.fill(variaveis['grafite'])

#     titulo = font.render("** Resumo dos dados coletados **" , 1, variaveis['azul'])
#     tela.blit(titulo, (15, 30))

#     titulo = font.render("CPU" , 1, variaveis['azul'])
#     tela.blit(titulo, (15, 60))

#     processador = variaveis['cpu']
#     disco = variaveis['disco'][0]
#     memoria = variaveis['memoria'][0]

#     # obtem o ip do usuario
#     host = variaveis['hosts'][0][1]
#     if host == '127.0.0.1':
#         host = variaveis['hosts'][1][1]

#     # titulo
#     texto = font.render('Processador:', True, variaveis['preto'])
#     tela.blit(texto, (15, 80))
#     # valor
#     tela.blit(font.render(processador.nome, True, variaveis['preto']), (155, 80))

#     # titulo
#     texto = font.render('Frequência:', True, variaveis['preto'])
#     tela.blit(texto, (15, 100))
#     # valor
#     tela.blit(font.render(processador.frequencia, True, variaveis['preto']), (155, 100))

#     # titulo
#     texto = font.render('Bits:', True, variaveis['preto'])
#     tela.blit(texto, (15, 120))
#     # valor
#     tela.blit(font.render(processador.bits, True, variaveis['preto']), (155, 120))
    
#     #
#     tela.blit(font.render('----------------------------------------------------------', True, variaveis['branco']), (180, 150))

#     titulo = font.render("Disco" , 1, variaveis['azul'])
#     tela.blit(titulo, (15, 170))

#     # titulo
#     texto = font.render('Total:', True, variaveis['preto'])
#     tela.blit(texto, (15, 190))
#     # valor
#     tela.blit(font.render(str(disco.total) + 'GB', True, variaveis['preto']), (155, 190))

#     # titulo
#     texto = font.render('Livre:', True, variaveis['preto'])
#     tela.blit(texto, (15, 210))
#     # valor
#     tela.blit(font.render(str(disco.livre) + 'GB', True, variaveis['preto']), (155, 210))

#     # titulo
#     texto = font.render('Usado:', True, variaveis['preto'])
#     tela.blit(texto, (15, 230))
#     # valor
#     tela.blit(font.render(str(disco.usado) + 'GB', True, variaveis['preto']), (155, 230))

#     #
#     tela.blit(font.render('----------------------------------------------------------', True, variaveis['branco']), (180, 260))

#     titulo = font.render("Memória" , 1, variaveis['azul'])
#     tela.blit(titulo, (15, 280))

#     # titulo
#     texto = font.render('Total:', True, variaveis['preto'])
#     tela.blit(texto, (15, 300))
#     # valor
#     tela.blit(font.render(str(memoria.capacidade) + 'GB', True, variaveis['preto']), (155, 300))

#     # titulo
#     texto = font.render('Livre:', True, variaveis['preto'])
#     tela.blit(texto, (15, 320))
#     # valor
#     tela.blit(font.render(str(memoria.disponivel) + 'GB', True, variaveis['preto']), (155, 320))

#     # titulo
#     texto = font.render('Usado:', True, variaveis['preto'])
#     tela.blit(texto, (15, 340))
#     # valor
#     tela.blit(font.render(str((format(float(memoria.capacidade) - float(memoria.disponivel), '.2f'))) + 'GB', True, variaveis['preto']), (155, 340))

#     #
#     tela.blit(font.render('----------------------------------------------------------', True, variaveis['branco']), (180, 370))

#     titulo = font.render("Rede" , 1, variaveis['azul'])
#     tela.blit(titulo, (15, 390))

#     # titulo
#     texto = font.render('IP:', True, variaveis['preto'])
#     tela.blit(texto, (15, 410))
#     # valor
#     tela.blit(font.render(host, True, variaveis['preto']), (155, 410))


#     # instrucao navegacao
#     instrucao = font.render('Tecle ← ou → para navegar', True, variaveis['preto'])
#     tela.blit(instrucao, variaveis['posicionamento-instrucao'])

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
                variaveis['posicao_atual'] = variaveis['posicao_atual'] + 1
                
            elif event.key == pygame.K_LEFT:
                variaveis['posicao_atual'] = variaveis['posicao_atual'] - 1
            
            elif event.key == pygame.K_SPACE:
                variaveis['posicao_atual'] = 6


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