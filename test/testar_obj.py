# classes

host = ""

if len(host) == 0:
    print('none')


class Host:
    def __init__(self, ip):
        self.ip = ip


host = Host('123123')
print(host)

