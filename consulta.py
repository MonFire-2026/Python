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

def consulta():
    desejo = input("Deseja consultar as KPIs? (s/n) ")
    if(desejo.lower() == "n"):
        print("Encerrando programa...")
    elif (desejo.lower() != "n" and desejo.lower() != "s"):
        print("Você digitou algo errado...tente novamente")
        consulta()
    elif (desejo.lower() == "s"):
        def Views():
            cursor.execute("select * from ViewDashboard")
            resultados = cursor.fetchall()
            kpi = input("Qual KPI deseja consultar? \n-Média da CPU neste dia (digite '1') \n-Média da RAM neste dia (digite '2') \n-Menor uso da CPU neste dia (digite '3') \n-Maior uso da CPU neste dia (digite '4') \n-Menor uso da RAM neste dia (digite '5') \n-Maior uso da RAM neste dia (digite '6') \n-Deseja encerrar o programa (digite '7') \n")
            for produto in resultados:
                if(kpi == 1 or kpi == "1"):
                    print(f"Média da CPU neste dia: {produto[0]}")
                    consulta()
                elif(kpi == 2 or kpi == "2"):
                    print(f"Média da RAM neste dia: {produto[1]}")
                    consulta()
                elif(kpi == 3 or kpi == "3"):
                    print(f"Menor uso da CPU neste dia: {produto[2]}")
                    consulta()
                elif(kpi == 4 or kpi == "4"):
                    print(f"Maior uso da CPU neste dia: {produto[3]}")
                    consulta()
                elif(kpi == 5 or kpi == "5"):
                    print(f"Menor uso da RAM neste dia: {produto[4]}")
                    consulta()
                elif(kpi == 6 or kpi == "6"):
                    print(f"Maior uso da ram neste dia: {produto[5]}")
                    consulta()
                elif(kpi == 7 or kpi == "7"):
                    print("Encerrando programa...")
                else:
                    print("Você digitou algo errado...tente novamente")
                    Views()
        Views()

       
          

cursor = conexao.cursor()
consulta()