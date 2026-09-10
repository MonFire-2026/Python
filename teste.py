from rich import print
import psutil as p

rede1 = p.net_io_counters(pernic=True, nowrap= True)
print(rede1)