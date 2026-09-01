import psutil as psiu
import time as t
from datetime import datetime
import mysql.connector

def banco(N1, N2, N3, N4):

    cnx = mysql.connector.connect(user = "mickaela",
                                  password = "0308",
                                  host = "localhost",
                                  database = "MonFire"
                                  )

    cursor = cnx.cursor()

    add_value = ("INSERT INTO captura (valor, tipo, fk_componente, uni_medida, fk_maquina) VALUES (%s, %s, %s,%s, 1)")

    data_value = (N1, N2, N3, N4)

    cursor.execute(add_value, data_value)

    cnx.commit()

    # cursor.execute( "SELECT * FROM captura")

    for db in cursor:
        print(db)
 
    cursor.close()

# variaveis CPU
porcentagem_de_uso_cpu = 0
frequencia = 0

# variaveis memoria
porcentagem_de_uso_ram = 0
memoria_total = 0
memoria_disponivel = 0
memoria_utilizada = 0

# variaveis disco
porcentagem_de_disco = 0
espaco_total = 0
espaco_livre = 0
espaco_utilizado = 0 


def CPU():

    # Análise CPU
    print('\n')

    print("Porcentagem de CPU usada:")
    porcentagem_de_uso_cpu = psiu.cpu_percent(interval=0.1)
    print(porcentagem_de_uso_cpu)

    print("Frequência da CPU")
    frequencia = psiu.cpu_freq().current
    print(frequencia)

    print('\n')

    banco(porcentagem_de_uso_cpu, 'Uso',1, '%' )
    banco(frequencia, 'Frequência', 1,'Hz')

def RAM() :
    # Análise memória RAM
        
    print("Memória RAM utilizada:") 
    porcentagem_de_uso_ram = psiu.virtual_memory().percent
    print(porcentagem_de_uso_ram)
    
    print("Memória RAM total:") 
    memoria_total = round(psiu.virtual_memory().total / (1024**3))
    print(memoria_total)
    
    print("Memória RAM disponível:")
    memoria_disponivel = round(psiu.virtual_memory().available / (1024**3))
    print(memoria_disponivel)
    
    print("Memória RAM usada:")
    memoria_utilizada = round(psiu.virtual_memory().used / (1024**3))
    print(memoria_utilizada)
    
    print('\n')

    banco(porcentagem_de_uso_ram, 'Uso',7, '%')
    banco(memoria_total, 'Total', 7, 'Gb')
    banco(memoria_disponivel, 'Disponível', 7, 'Gb')
    banco(memoria_utilizada, 'Em uso', 7, 'Gb')

def Disco() :
     # Análise Disco
                         
    print("Porcentagem do Disco usada:")
    porcentagem_de_disco = psiu.disk_usage('C:\\').percent
    print(porcentagem_de_disco)
     
    print("Disco total usado:")
    espaco_total = round(psiu.disk_usage('C:\\').total / (1024 ** 3))
    print(espaco_total)
         
    print("Parte livre do disco:")
    espaco_livre = round(psiu.disk_usage('C:\\').free / (1024 ** 3))
    print(espaco_livre)
         
    print("Parte usada do disco:") 
    espaco_utilizado = round(psiu.disk_usage('C:\\').used / (1024 ** 3))
    print(espaco_utilizado)

    banco(porcentagem_de_disco, 'Uso', 13, '%')
    banco(espaco_total, 'Total', 13, 'Gb')
    banco(espaco_livre, 'Disponível', 13, 'Gb')
    banco(espaco_utilizado, 'Em uso', 13, 'Gb')
                 
    print('\n')
                   
    print("Hora da captura:")
    print(datetime.now().strftime("%H:%M:%S"))
                 
    print('\n')     



while True:
    CPU()
    RAM()
    Disco()
    t.sleep(5)