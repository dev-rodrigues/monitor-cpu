import pygame
import psutil
import cpuinfo
import platform
import subprocess
import os
import time
import socket
import re,os,sys

def get_ip_addresses(family):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == family:
                yield (interface, snic.address, snic.netmask)

ipv4s = list(get_ip_addresses(socket.AF_INET))

ip_base = ipv4s[0][1]
