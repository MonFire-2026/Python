import psutil as p

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="mickaela",
  password="0308",
  database="MonFire"
)

mycursor = mydb.cursor()

mycursor.execute("USE MonFire")

for x in mycursor:
  print(x)


def capturaDados():



    print("\n=======================Menu===================================\n")
    print("\n 1- Comando para ver a uso da CPUs")
    print(" 2- Comando para ver o percentual de uso da memoria ram")
    print(" 3- Comando para uso do disco\n")
    print("------------------------------------------------------------------\n")

    pergunta_principal = int(input("Qual componente vc deseja visualizar?\n"))



    if pergunta_principal == 1:

      print("===================Resposta===================")
      selecionar = "select * from ViewCPU"


    elif pergunta_principal == 2:

      print("===================Resposta===================")
      selecionar = "select * from ViewRAM"

      

    elif pergunta_principal == 3:

      print("===================Resposta===================")
      selecionar = "select * from ViewDisco"


  
    mycursor = mydb.cursor()

    mycursor.execute(selecionar)

    myresult = mycursor.fetchall()

    for x in myresult:
      print(x)

    repetir()
    
def repetir():

    

    pergunta_repetir = input("Deseja realizar uma nova consulta? (s/n)") 

    if pergunta_repetir == "n":
        print("\nAgradecemos a preferência")
        print("\nEncerrando o programa...")
    
    elif pergunta_repetir == "s":
        capturaDados()
    else:
            print("\nEncerrando o programa...")
    
capturaDados()






