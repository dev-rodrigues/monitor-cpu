import psutil


p = psutil.Process(210306)
conn = p.connections()
print(conn)