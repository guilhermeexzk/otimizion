#!/usr/bin/env python3
"""Otimizion: limpeza simples para Windows e Linux (Zorin/Ubuntu)."""

from datetime import datetime, timedelta
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
from getpass import getpass


DIAS_PARA_ARQUIVOS_TEMP = 7
PIN_OTIMIZION = "223542"


def limpar_conteudo(pasta: Path, mais_antigo_que: datetime | None = None) -> tuple[int, list[str]]:
    """Apaga itens de uma pasta sem seguir links simbólicos."""
    removidos = 0
    erros: list[str] = []
    try:
        itens = list(pasta.iterdir())
    except FileNotFoundError:
        return removidos, erros
    except OSError as erro:
        return removidos, [f"Não foi possível acessar {pasta}: {erro}"]

    for item in itens:
        try:
            info = item.lstat()
            if mais_antigo_que is not None and datetime.fromtimestamp(info.st_mtime) > mais_antigo_que:
                continue
            if item.is_symlink() or not item.is_dir():
                item.unlink()
            else:
                shutil.rmtree(item)
            removidos += 1
        except OSError as erro:
            erros.append(f"Não foi possível remover {item.name}: {erro}")
    return removidos, erros


def limpar_temporarios_antigos(pasta: Path, limite: datetime, uid: int | None = None) -> tuple[int, list[str]]:
    """Remove somente itens antigos; mantém diretórios que ainda tenham arquivos recentes."""
    removidos = 0
    erros: list[str] = []
    try:
        for raiz, diretorios, arquivos in os.walk(pasta, topdown=False, followlinks=False):
            raiz_path = Path(raiz)
            for nome in arquivos + diretorios:
                item = raiz_path / nome
                try:
                    info = item.lstat()
                    if uid is not None and info.st_uid != uid:
                        continue
                    if datetime.fromtimestamp(info.st_mtime) > limite:
                        continue
                    if item.is_symlink() or not item.is_dir():
                        item.unlink()
                    else:
                        item.rmdir()
                    removidos += 1
                except OSError as erro:
                    erros.append(f"Não foi possível remover {item.name}: {erro}")
    except OSError as erro:
        erros.append(f"Não foi possível acessar {pasta}: {erro}")
    return removidos, erros


def limpar_temporarios() -> None:
    """Limpa arquivos temporários antigos e miniaturas regeneráveis."""
    print("\nLimpando arquivos temporários antigos...")
    erros: list[str] = []
    total = 0
    limite = datetime.now() - timedelta(days=DIAS_PARA_ARQUIVOS_TEMP)
    temp_dir = Path(tempfile.gettempdir())

    if platform.system() == "Linux":
        # /tmp é compartilhado: remove somente itens antigos pertencentes ao usuário atual.
        uid = os.getuid()
        apagados, falhas = limpar_temporarios_antigos(temp_dir, limite, uid)
        total += apagados
        erros.extend(falhas)

        cache = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
        thumbs, falhas = limpar_conteudo(cache / "thumbnails")
        total += thumbs
        erros.extend(falhas)
    else:
        apagados, falhas = limpar_temporarios_antigos(temp_dir, limite)
        total += apagados
        erros.extend(falhas)

    if erros:
        print(f"Itens removidos: {total}. Alguns arquivos estavam em uso ou sem permissão.")
        for erro in erros[:8]:
            print(f"- {erro}")
        if len(erros) > 8:
            print(f"- e mais {len(erros) - 8} item(ns).")
    else:
        print(f"Limpeza concluída. Itens removidos: {total}.")
    print(f"Arquivos temporários mais novos que {DIAS_PARA_ARQUIVOS_TEMP} dias são mantidos.")


def limpar_lixeira() -> None:
    """Esvazia a lixeira do usuário atual."""
    print("\nEsvaziando a Lixeira...")
    if platform.system() == "Windows":
        comando = [
            "powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
            "Clear-RecycleBin -Force -ErrorAction Stop",
        ]
        try:
            resultado = subprocess.run(comando, check=False, capture_output=True, text=True)
            if resultado.returncode == 0:
                print("Lixeira esvaziada.")
            else:
                print("Não foi possível esvaziar a Lixeira. Confira se há itens e tente novamente.")
        except OSError as erro:
            print(f"Não foi possível abrir a ferramenta do Windows: {erro}")
        return

    data_home = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
    erros: list[str] = []
    files, falhas = limpar_conteudo(data_home / "Trash" / "files")
    erros.extend(falhas)
    info, falhas = limpar_conteudo(data_home / "Trash" / "info")
    erros.extend(falhas)
    if erros:
        print("A Lixeira foi processada, mas alguns itens não puderam ser removidos.")
        for erro in erros[:8]:
            print(f"- {erro}")
    else:
        print(f"Lixeira esvaziada. Itens removidos: {files + info}.")


def limpar_cache_ram() -> None:
    """Solicita a limpeza de cache recuperável no Linux; no Windows abre o monitor."""
    sistema = platform.system()
    print("\nMemória RAM")
    if sistema == "Windows":
        print("O Windows administra a memória em cache automaticamente.")
        print("Abrindo o Gerenciador de Tarefas para consultar o uso da memória...")
        try:
            subprocess.Popen(["taskmgr.exe"])
        except OSError as erro:
            print(f"Não foi possível abrir o Gerenciador de Tarefas: {erro}")
        return

    if sistema == "Linux":
        print("O Linux vai liberar apenas caches recuperáveis do sistema; isso pode deixar a próxima abertura de arquivos mais lenta.")
        resposta = input("Deseja continuar? [s/N]: ").strip().lower()
        if resposta not in {"s", "sim"}:
            print("Operação cancelada.")
            return
        shell = "sync && echo 3 > /proc/sys/vm/drop_caches"
        pkexec = shutil.which("pkexec")
        sudo = shutil.which("sudo")
        try:
            if pkexec:
                resultado = subprocess.run([pkexec, "sh", "-c", shell], check=False)
            elif sudo:
                resultado = subprocess.run([sudo, "sh", "-c", shell], check=False)
            else:
                print("Não encontrei pkexec ou sudo para solicitar a autorização do sistema.")
                return
            if resultado.returncode == 0:
                print("Cache recuperável da memória liberado.")
            else:
                print("A operação foi cancelada ou o sistema não permitiu a limpeza.")
        except OSError as erro:
            print(f"Não foi possível iniciar a limpeza de memória: {erro}")
        return

    print("Este sistema não tem uma ação de limpeza de memória configurada.")


def mostrar_menu() -> None:
    print("\n\033[1;32m╔══════════════════════════════════════════════════════════════╗")
    print("║                         OTIMIZION                            ║")
    print("║                Limpeza simples do computador                 ║")
    print("╚══════════════════════════════════════════════════════════════╝\033[0m")
    print("\n[1] Limpar arquivos temporários")
    print("[2] Esvaziar a Lixeira")
    print("[3] Consultar / liberar cache de RAM")
    print("[4] Limpar temporários + esvaziar Lixeira")
    print("[5] Sair")
    print("\nby:guilhermeexzk")


def aguardar() -> None:
    try:
        input("\nPressione Enter para voltar ao menu...")
    except (EOFError, KeyboardInterrupt):
        pass


def main() -> None:
    if platform.system() not in {"Windows", "Linux"}:
        print("O Otimizion foi preparado para Windows e Linux (incluindo Zorin/Ubuntu).")
        return
    print("\033[1;32m╔══════════════════════════════════════════════════════════════╗")
    print("║                         OTIMIZION                            ║")
    print("║                 Digite o PIN para continuar                  ║")
    print("╚══════════════════════════════════════════════════════════════╝\033[0m")
    try:
        if getpass("PIN: ") != PIN_OTIMIZION:
            print("PIN incorreto.")
            return
    except (EOFError, KeyboardInterrupt):
        print("\nAté logo.")
        return
    while True:
        mostrar_menu()
        try:
            escolha = input("Escolha: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo.")
            return
        if escolha == "1":
            limpar_temporarios()
        elif escolha == "2":
            limpar_lixeira()
        elif escolha == "3":
            limpar_cache_ram()
        elif escolha == "4":
            limpar_temporarios()
            limpar_lixeira()
        elif escolha == "5":
            print("Até logo.")
            return
        else:
            print("Opção inválida. Digite de [1] a [5].")
            continue
        aguardar()


if __name__ == "__main__":
    main()
