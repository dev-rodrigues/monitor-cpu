import sched, time

inicio = time.time()
inicioClock = time.process_time()

s = sched.scheduler(time.time, time.sleep)

s.enter(3, 1, None)

tempoFinal = 'TEMPO FINAL: %s | CLOCK FINAL: %0.2f' % (time.ctime(), time.process_time())

final = time.time() - inicio
finalClock = time.process_time() - inicioClock


tempoUsado = 'TEMPO USADO NESSA CHAMADA: %0.3f segundos | CLOCK USADO NESSA CHAMADA: %0.2f' % (final, finalClock)

print(tempoUsado)