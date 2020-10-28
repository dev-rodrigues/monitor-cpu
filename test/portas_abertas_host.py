import nmap

def scan_host(host):
    nm = nmap.PortScanner()

    nm.scan(host)
    print(nm[host].hostname())
    for proto in nm[host].all_protocols():
        print('----------')
        print('Protocolo : %s' % proto)

    lport = nm[host][proto].keys()
    #lport.sort()
    for port in lport:
        print ('Porta: %s\t Estado: %s' % (port, nm[host][proto][port]['state']))

scan_host('192.168.0.12')