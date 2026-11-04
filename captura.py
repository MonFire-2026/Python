import os
import time

import mysql.connector
import psutil
from rich import print


CODIGOS_PYTHON = ("CPU_USO", "RAM_USO", "DISCO_USO")
INTERVALO_CAPTURA = 2
ids_configuracao = {}


def inteiro_positivo_do_ambiente(nome):
    valor = os.getenv(nome, "").strip()

    try:
        numero = int(valor)
    except ValueError as erro:
        raise ValueError(f"A variável {nome} deve ser um inteiro positivo.") from erro

    if numero <= 0:
        raise ValueError(f"A variável {nome} deve ser um inteiro positivo.")

    return numero


def conectar_banco():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "MonFire"),
        user=os.getenv("DB_USER", "aluno"),
        password=os.getenv("DB_PASS", "sptech"),
    )


def preparar_leitura_do_host():
    proc_do_host = "/host/proc"

    if os.path.isdir(proc_do_host):
        psutil.PROCFS_PATH = proc_do_host
        print(f"[cyan]CPU e RAM serão lidas de {proc_do_host}.[/cyan]")


def carregar_configuracoes(cursor, maquina_id):
    cursor.execute(
        """
        SELECT cm.id, tc.codigo
        FROM configuracao_maquina AS cm
        INNER JOIN componente AS comp ON comp.id = cm.fk_componente
        INNER JOIN tipo_componente AS tc ON tc.id = comp.fk_tipo_componente
        WHERE cm.fk_maquina = %s
            AND cm.ativa = 1
            AND comp.status_atividade = 1
            AND tc.codigo IN ('CPU_USO', 'RAM_USO', 'DISCO_USO')
        """,
        (maquina_id,),
    )

    ids_configuracao.clear()
    ids_configuracao.update({
        codigo: configuracao_id
        for configuracao_id, codigo in cursor.fetchall()
    })


def buscar_configuracao(codigo):
    return ids_configuracao.get(codigo)


def caminho_disco_monitorado():
    if os.path.isdir("/host"):
        return "/host"

    if os.name == "nt":
        return "C:\\"

    return "/"


def CPU():
    if buscar_configuracao("CPU_USO") is None:
        return None

    porcentagem_de_uso_cpu = psutil.cpu_percent(interval=0.1)
    print(f"CPU: [green]{porcentagem_de_uso_cpu:.2f}%[/green]")
    return "CPU_USO", porcentagem_de_uso_cpu


def RAM():
    if buscar_configuracao("RAM_USO") is None:
        return None

    porcentagem_de_uso_ram = psutil.virtual_memory().percent
    print(f"RAM: [green]{porcentagem_de_uso_ram:.2f}%[/green]")
    return "RAM_USO", porcentagem_de_uso_ram


def Disco():
    if buscar_configuracao("DISCO_USO") is None:
        return None

    porcentagem_de_uso_disco = psutil.disk_usage(caminho_disco_monitorado()).percent
    print(f"Disco: [green]{porcentagem_de_uso_disco:.2f}%[/green]")
    return "DISCO_USO", porcentagem_de_uso_disco


def banco(conexao, cursor, leituras):
    registros = [
        (valor, buscar_configuracao(codigo))
        for codigo, valor in leituras
        if buscar_configuracao(codigo) is not None
    ]

    if not registros:
        return 0

    cursor.executemany(
        "INSERT INTO captura (valor, fk_configuracao_maquina) VALUES (%s, %s)",
        registros,
    )
    conexao.commit()
    return len(registros)


def main():
    maquina_id = inteiro_positivo_do_ambiente("MAQUINA_ID")
    preparar_leitura_do_host()

    conexao = conectar_banco()
    cursor = conexao.cursor(buffered=True)

    try:
        carregar_configuracoes(cursor, maquina_id)
        codigos = ", ".join(ids_configuracao) if ids_configuracao else "nenhuma"
        print(f"[bold cyan]Máquina {maquina_id} | Métricas Python: {codigos}[/bold cyan]")

        while True:
            try:
                leituras = [leitura for leitura in (CPU(), RAM(), Disco()) if leitura]
                quantidade = banco(conexao, cursor, leituras)

                if quantidade:
                    print(f"[blue]{quantidade} captura(s) salva(s).[/blue]\n")
                else:
                    print("[yellow]Nenhuma métrica de CPU, RAM ou Disco foi configurada.[/yellow]\n")
            except mysql.connector.Error as erro:
                conexao.rollback()
                print(f"[bold red]Erro ao salvar capturas: {erro}[/bold red]")

            time.sleep(INTERVALO_CAPTURA)
    except KeyboardInterrupt:
        print("\n[yellow]Coletor Python encerrado.[/yellow]")
    finally:
        cursor.close()
        conexao.close()


if __name__ == "__main__":
    main()
