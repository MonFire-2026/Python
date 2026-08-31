import psutil as p
import time as t
import datetime as d
import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="monitoramento24h"
)


def captura():
    print("\n-----MONITORAMENTO-----")
    print("Uso da CPU:",p.cpu_percent(interval=1),"%")
    print("Uso da Memória RAM:",p.virtual_memory().percent, "%")
    print("Uso do Disco:",p.disk_usage('C:\\').used, "Bytes")
    print("Horário da captura:",d.datetime.now())
    sql = "INSERT INTO captura (porcentagem_de_uso_cpu, porcentagem_de_uso_ram, espaco_utilizado, dtHr) VALUES (%s, %s, %s, %s)"
    valores = (p.cpu_percent(interval=1), p.virtual_memory().percent, p.disk_usage('C:\\').used, d.datetime.now())
    cursor.execute(sql, valores)
    conexao.commit()
    

cursor = conexao.cursor()
while True:
    captura()
    t.sleep(10)
    
    