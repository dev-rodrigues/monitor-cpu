import psutil
import time

pids = psutil.pids()

nome_do_processo = psutil.Process(1).name()
percent_uso_processo = psutil.Process(1).memory_percent()
memoria_usada_processo = psutil.Process(1).memory_info().rss / 1024/1024
threads_processo = psutil.Process(1).num_threads()
tempo_usuario = str(psutil.Process(1).cpu_times().user) + ' s'
data_criacao = time.ctime(psutil.Process(1).create_time())


print(nome_do_processo
        ,   '{:.2f}'.format(percent_uso_processo) + ' %'
        ,   '{:.2f}'.format(memoria_usada_processo) + ' MB'
        ,   threads_processo
        ,   tempo_usuario
        ,   data_criacao
    )