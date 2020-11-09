import psutil


io_status = psutil.net_io_counters(pernic=True)


nomes = []

# for status in io_status:
#     print(status)


teste = io_status['enp37s0']

dado = teste[0]

teste2 = round(dado / (1024 ** 2), 2)

print(teste2)