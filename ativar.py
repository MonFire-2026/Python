import getpass
import os
import socket
import sys

import mysql.connector
import psutil


CAMINHO_AGENTE = os.getenv("AGENTE_ENV_PATH", "/dados/agente.env")


def variavel_obrigatoria(nome):
    valor = os.getenv(nome, "").strip()

    if not valor:
        raise ValueError(f"A variável {nome} não foi informada.")

    return valor


def conectar_banco():
    return mysql.connector.connect(
        host=variavel_obrigatoria("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=variavel_obrigatoria("DB_NAME"),
        user=variavel_obrigatoria("DB_USER"),
        password=variavel_obrigatoria("DB_PASS"),
    )


def coletar_hostname():
    with open("/host/etc/hostname", "r", encoding="utf-8") as arquivo:
        return arquivo.read().strip()


def coletar_sistema_operacional():
    with open("/host/etc/os-release", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if linha.startswith("PRETTY_NAME="):
                sistema = linha.split("=", 1)[1].strip().strip("\"'")
                if sistema:
                    return sistema

    raise ValueError("Não foi possível identificar o sistema operacional.")


def coletar_ip():
    host_banco = variavel_obrigatoria("DB_HOST")
    porta_banco = int(os.getenv("DB_PORT", "3306"))

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_rede:
        socket_rede.connect((host_banco, porta_banco))
        return socket_rede.getsockname()[0]


def coletar_mac(ip):
    for enderecos in psutil.net_if_addrs().values():
        for endereco in enderecos:
            if endereco.family == socket.AF_INET and endereco.address == ip:
                for endereco_mac in enderecos:
                    if endereco_mac.family == psutil.AF_LINK:
                        return endereco_mac.address

    raise ValueError("Não foi possível identificar o MAC correspondente ao IP.")


def coletar_identificacao_host():
    ip = coletar_ip()

    return {
        "hostname": coletar_hostname(),
        "mac": coletar_mac(ip),
        "ip": ip,
        "sistema_operacional": coletar_sistema_operacional(),
    }


def ativar_maquina(conexao, codigo, identificacao):
    cursor = conexao.cursor(buffered=True)

    try:
        cursor.callproc(
            "ativar_maquina",
            [
                codigo,
                identificacao["hostname"],
                identificacao["mac"],
                identificacao["ip"],
                identificacao["sistema_operacional"],
            ],
        )

        resultados = list(cursor.stored_results())
        if not resultados:
            raise RuntimeError("A procedure não devolveu os dados da máquina.")

        maquina = resultados[0].fetchone()
        if not maquina or not isinstance(maquina[0], int) or maquina[0] <= 0:
            raise RuntimeError("A procedure devolveu um ID de máquina inválido.")

        return maquina[0]
    finally:
        cursor.close()


def salvar_id_maquina(maquina_id, caminho=CAMINHO_AGENTE):
    if os.path.exists(caminho):
        raise FileExistsError(
            f"O arquivo {caminho} já existe. A ativação não será substituída."
        )

    diretorio = os.path.dirname(caminho)
    if diretorio:
        os.makedirs(diretorio, exist_ok=True)

    descritor = os.open(caminho, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descritor, "w", encoding="utf-8") as arquivo:
        arquivo.write(f"MAQUINA_ID={maquina_id}\n")


def main():
    conexao = None

    try:
        codigo = getpass.getpass("Código de ativação: ").strip()
        if len(codigo) < 20:
            raise ValueError("Código de ativação inválido.")

        identificacao = coletar_identificacao_host()
        print(f"Hostname: {identificacao['hostname']}")
        print(f"IP: {identificacao['ip']}")
        print(f"MAC: {identificacao['mac']}")
        print(f"Sistema operacional: {identificacao['sistema_operacional']}")

        conexao = conectar_banco()
        maquina_id = ativar_maquina(conexao, codigo, identificacao)
        salvar_id_maquina(maquina_id)
        print(f"Máquina ativada com sucesso. ID: {maquina_id}")
    except (ValueError, RuntimeError, FileExistsError, OSError, mysql.connector.Error) as erro:
        print(f"Falha na ativação: {erro}", file=sys.stderr)
        return 1
    finally:
        if conexao is not None and conexao.is_connected():
            conexao.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
