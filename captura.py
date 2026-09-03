import psutil as p
import time as t
from datetime import datetime
import mysql.connector
from rich import print


def banco(N1, N2, N3, N4):

    cnx = mysql.connector.connect(user = "adm_monfire",
                                  password = "Monfire@2026",
                                  host = "10.18.33.86",
                                  database = "monfire"
                                  )

    cursor = cnx.cursor()

    add_value = ("INSERT INTO captura (valor, tipo, fk_componente, uni_medida, fk_maquina) VALUES (%s, %s, %s, %s, 1)")

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

    print('\n')
    porcentagem_de_uso_cpu = p.cpu_percent(interval=0.1)
    frequencia = p.cpu_freq().current

    if porcentagem_de_uso_cpu >= 80 :
        print(f"Alerta o uso da sua CPU está em: [bold red]{porcentagem_de_uso_cpu}% [/bold red]")   

    elif porcentagem_de_uso_cpu >= 2 :
        print(f"Alerta o uso da sua CPU está em: [bold yellow]{porcentagem_de_uso_cpu}% [/bold yellow]")  

    else : 
        print(f"Porcentagem de uso da CPU: [blue]{porcentagem_de_uso_cpu}%[/blue]")

    if frequencia >= 1700 :
        print(f"Alerta a frequência da sua CPU está em: [bold red]{frequencia}Hz [/bold red]")   

    elif frequencia >= 1500 :
        print(f"Alerta a frequência da sua CPU está em: [bold yellow]{porcentagem_de_uso_cpu}Hz [/bold yellow]")  

    else :
        print(f"A frequência da sua CPU está em: [blue]{frequencia}Hz[/blue]")

    print('\n')

    banco(porcentagem_de_uso_cpu, 'Uso',1, '%' )
    banco(frequencia, 'Frequência', 1,'Hz')


def RAM() :
         
    porcentagem_de_uso_ram = p.virtual_memory().percent
    memoria_total = round(p.virtual_memory().total / (1024**3))
    memoria_disponivel = round(p.virtual_memory().available / (1024**3))
    memoria_utilizada = round(p.virtual_memory().used / (1024**3))

    if porcentagem_de_uso_ram >= 80 :
        print(f"Alerta o uso da sua RAM está em: [bold red]{porcentagem_de_uso_ram}% [/bold red]")   

    elif porcentagem_de_uso_ram >= 65 :
        print(f"Alerta o uso da sua RAM está em: [bold yellow]{porcentagem_de_uso_cpu}% [/bold yellow]") 

    else :
        print(f"Porcentagem de uso da RAM: [blue]{porcentagem_de_uso_ram}%[/blue]")

    
    print(f"[blue]{memoria_total}Gb[/blue]")


    if memoria_disponivel < 7 :
        print(f"Alerta você só tem: [bold red]{memoria_disponivel}Gb da sua RAM dísponivel [/bold red]")

    elif memoria_disponivel <= 5.5 :
        print(f"Alerta você só tem: [bold yellow]{memoria_disponivel}Gb da sua RAM dísponivel [/bold yellow]")

    else :
        print(f"[blue]{memoria_disponivel}Gb[/blue]")

    if memoria_utilizada >= 7 :
        print(f"Alerta você está usando: [bold red]{memoria_utilizada}Gb da sua RAM [/bold red]")

    elif memoria_utilizada >= 5.5 :
        print(f"Alerta você está usando: [bold yellow]{memoria_utilizada}Gb da sua RAM [/bold yellow]")   

    else :
        print(f"Gigabytes de uso da RAM: [blue]{memoria_utilizada}Gb[/blue]")


    print('\n')


    banco(porcentagem_de_uso_ram, 'Uso',7, '%')
    banco(memoria_total, 'Total', 7, 'Gb')
    banco(memoria_disponivel, 'Disponível', 7, 'Gb')
    banco(memoria_utilizada, 'Em uso', 7, 'Gb')


def Disco() :

    porcentagem_de_disco = p.disk_usage('C:\\').percent
    espaco_total = round(p.disk_usage('C:\\').total / (1024 ** 3))
    espaco_livre = round(p.disk_usage('C:\\').free / (1024 ** 3))
    espaco_utilizado = round(p.disk_usage('C:\\').used / (1024 ** 3))

    if porcentagem_de_disco >= 80 :
        print(f"Alerta o uso do seu Disco está em: [bold red]{porcentagem_de_disco}% [/bold red]") 

    elif porcentagem_de_disco >= 65 :
        print(f"Alerta o uso do seu Disco está em: [bold yellow]{memoria_disponivel}% [/bold yellow]")  

    else :
        print(f"Porcentagem de uso do Disco: [blue]{porcentagem_de_disco}%[/blue]")

    
    print(f"Espaço total do seu Disco: [blue]{espaco_total}Gb[/blue]")

    
    if espaco_livre < 20 :
        print(f"Alerta o uso do seu Disco está em: [bold red]{espaco_livre}Gb [/bold red]")

    elif memoria_disponivel <= 45 :
        print(f"Alerta o uso do seu Disco está em: [bold yellow]{memoria_disponivel}Gb [/bold yellow]") 

    else :
        print(f"Espaço livre do seu Disco: [blue]{espaco_livre}Gb[/blue]")
    
    if espaco_utilizado >= 220 :
        print(f"Alerta você só tem [bold red]{espaco_total - espaco_utilizado}Gb do seu Disco dísponivel [/bold red]")

    elif espaco_utilizado <= 5.5 :
        print(f"Alerta você só tem: [bold yellow]{espaco_total - espaco_utilizado}Gb do seu Disco dísponivel [/bold yellow]") 

    else :
        print(f"Espaço do Disco que está sendo utilizado: [blue]{espaco_utilizado}Gb[/blue]")

    
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
    