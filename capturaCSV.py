import psutil as p
import time as t
from datetime import datetime
import csv

ARQUIVO_CSV = "capturas.csv"
COLUNAS_CSV = ["data_hora", "maquina", "componente", "tipo", "valor", "uni_medida"]
MAQUINA = "" 
SEPARADOR_DECIMAL = ","


def salvar_csv(valor, tipo, componente, uni_medida):
    """Acrescenta uma linha no CSV (escreve o cabeçalho se o arquivo estiver vazio/novo)."""
    with open(ARQUIVO_CSV, "a", newline="", encoding="utf-8-sig") as f:
        escritor = csv.writer(f, delimiter=";")

        if f.tell() == 0:
            escritor.writerow(COLUNAS_CSV)

        escritor.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            MAQUINA,
            componente,
            tipo,
            str(valor).replace(".", SEPARADOR_DECIMAL),
            uni_medida,
        ])


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
        print(f"Alerta o uso da sua CPU está em: {porcentagem_de_uso_cpu}%")

    elif porcentagem_de_uso_cpu >= 50 :
        print(f"Alerta o uso da sua CPU está em: {porcentagem_de_uso_cpu}%")

    else : 
        print(f"Porcentagem de uso da CPU: {porcentagem_de_uso_cpu}%")

    if frequencia >= 1700 :
        print(f"Alerta a frequência da sua CPU está em: {frequencia}Hz")

    elif frequencia >= 1500 :
        print(f"Alerta a frequência da sua CPU está em: {porcentagem_de_uso_cpu}Hz")

    else :
        print(f"A frequência da sua CPU está em: {frequencia}Hz")

    print('\n')

    salvar_csv(porcentagem_de_uso_cpu, 'Uso', 'CPU', '%')
    salvar_csv(frequencia, 'Frequência', 'CPU', 'Hz')


def RAM() :
         
    porcentagem_de_uso_ram = p.virtual_memory().percent
    memoria_total = round(p.virtual_memory().total / (1024**3))
    memoria_disponivel = round(p.virtual_memory().available / (1024**3))
    memoria_utilizada = round(p.virtual_memory().used / (1024**3))

    if porcentagem_de_uso_ram >= 80 :
        print(f"Alerta o uso da sua RAM está em: {porcentagem_de_uso_ram}%")

    elif porcentagem_de_uso_ram >= 65 :
        print(f"Alerta o uso da sua RAM está em: {porcentagem_de_uso_cpu}%")

    else :
        print(f"Porcentagem de uso da RAM: {porcentagem_de_uso_ram}%")

    
    print(f"Memória RAM total: {memoria_total}Gb")


    if memoria_disponivel < 7 :
        print(f"Alerta você só tem: {memoria_disponivel}Gb da sua RAM dísponivel")

    elif memoria_disponivel <= 5.5 :
        print(f"Alerta você só tem: {memoria_disponivel}Gb da sua RAM dísponivel")

    else :
        print(f"{memoria_disponivel}Gb")

    if memoria_utilizada >= 7 :
        print(f"Alerta você está usando: {memoria_utilizada}Gb da sua RAM")

    elif memoria_utilizada >= 5.5 :
        print(f"Alerta você está usando: {memoria_utilizada}Gb da sua RAM")

    else :
        print(f"Gigabytes de uso da RAM: {memoria_utilizada}Gb")


    print('\n')


    salvar_csv(porcentagem_de_uso_ram, 'Uso', 'RAM', '%')
    salvar_csv(memoria_total, 'Total', 'RAM', 'Gb')
    salvar_csv(memoria_disponivel, 'Disponível', 'RAM', 'Gb')
    salvar_csv(memoria_utilizada, 'Em uso', 'RAM', 'Gb')


def Disco() :

    porcentagem_de_disco = p.disk_usage('/').percent
    espaco_total = round(p.disk_usage('/').total / (1024 ** 3))
    espaco_livre = round(p.disk_usage('/').free / (1024 ** 3))
    espaco_utilizado = round(p.disk_usage('/').used / (1024 ** 3))

    if porcentagem_de_disco >= 80 :
        print(f"Alerta o uso do seu Disco está em: {porcentagem_de_disco}%")

    elif porcentagem_de_disco >= 65 :
        print(f"Alerta o uso do seu Disco está em: {porcentagem_de_disco}%")

    else :
        print(f"Porcentagem de uso do Disco: {porcentagem_de_disco}%")

    
    print(f"Espaço total do seu Disco: {espaco_total}Gb")

    
    if espaco_livre < 20 :
        print(f"Alerta o uso do seu Disco está em: {espaco_livre}Gb")

    elif espaco_livre <= 45 :
        print(f"Alerta o uso do seu Disco está em: {espaco_livre}Gb")

    else :
        print(f"Espaço livre do seu Disco: {espaco_livre}Gb")
    
    if espaco_utilizado >= 220 :
        print(f"Alerta você só tem {espaco_total - espaco_utilizado}Gb do seu Disco dísponivel")

    elif espaco_utilizado <= 5.5 :
        print(f"Alerta você só tem: {espaco_total - espaco_utilizado}Gb do seu Disco dísponivel")

    else :
        print(f"Espaço do Disco que está sendo utilizado: {espaco_utilizado}Gb")

    
    salvar_csv(porcentagem_de_disco, 'Uso', 'DISCO', '%')
    salvar_csv(espaco_total, 'Total', 'DISCO', 'Gb')
    salvar_csv(espaco_livre, 'Disponível', 'DISCO', 'Gb')
    salvar_csv(espaco_utilizado, 'Em uso', 'DISCO', 'Gb')
                 
    print('\n')
                   
    print("Hora da captura:")
    print(datetime.now().strftime("%H:%M:%S"))
                 
    print('\n')  


def Rede() :
   
    dados_rede = p.net_io_counters()

    bytes_enviados = round(dados_rede.bytes_sent / (1024**2), 2)
    bytes_recebidos = round(dados_rede.bytes_recv / (1024**2), 2)

    if bytes_recebidos >= 500 :
        print(f"Alerta! Dados recebidos (Download): {bytes_recebidos} MB")

    elif bytes_recebidos >= 200 :
        print(f"Alerta! Dados recebidos (Download): {bytes_recebidos} MB")

    else :
        print(f"Dados recebidos (Download): {bytes_recebidos} MB")

    if bytes_enviados >= 200 :
        print(f"Alerta! Dados enviados (Upload): {bytes_enviados} MB")

    elif bytes_enviados >= 100 :
        print(f"Alerta! Dados enviados (Upload): {bytes_enviados} MB")

    else :
        print(f"Dados enviados (Upload): {bytes_enviados} MB")

    print('\n')

    salvar_csv(bytes_recebidos, 'Download', 'REDE', 'MB')
    salvar_csv(bytes_enviados, 'Upload', 'REDE', 'MB')


while MAQUINA == "":
    MAQUINA = input("Digite o nome da máquina (ex: Felipe): ").strip()

print(f"\nIniciando captura da máquina: {MAQUINA}")

while True:
    CPU()
    RAM()
    Disco()
    Rede()
    t.sleep(5)