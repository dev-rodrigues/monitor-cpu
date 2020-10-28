import os
import subprocess
import platform
import psutil
import cpuinfo
import time
import socket
import re,os,sys
import nmap

def getNewIp(family):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == family:
                yield (interface, snic.address, snic.netmask)

ipv4s = list(getNewIp(socket.AF_INET))

my_ip = ipv4s[0][1]

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
    
        return_codes[base_ip + '{0}'.format(i)] =   retorna_codigo_ping(base_ip + '{0}'.format(i))
        if i %20 ==0:
            print(".", end = "")

        if return_codes[base_ip + '{0}'.format(i)] == 0:
            host_validos.append(base_ip + '{0}'.format(i))

    print("\nMapeamento pronto...")

    return host_validos

class Host:
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name
        self.ports = []   

class Port:
    def __init__(self, port, state):
        self.port = port
        self.state = state   

hosts = []

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



# Chamadas 
print('Ip que será utilizado como base', my_ip)
ip_string = my_ip

ip_lista = ip_string.split('.')
base_ip = ".".join(ip_lista[0:3]) + '.'
print("O teste será feito na sub rede: ", base_ip)

hosts_localizados = verifica_hosts_validos(base_ip)
print ("Os host válidos são: ", hosts_localizados)

print('Verifica nome do host\r')
detalhar_host(hosts_localizados)