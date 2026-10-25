#!/usr/bin/env python3
"""Otimizion: utilitários simples de manutenção do computador."""

from getpass import getpass
import os
from pathlib import Path
import shutil
import subprocess

SENHA_CORRETA = "223542"


def limpar_diretorio(conteudo: Path, erros: list[str]) -> None:
    """Remove os itens de um diretório sem seguir links simbólicos."""
    if not conteudo.exists():
        return
    try:
        itens = list(conteudo.iterdir())
    except OSError as erro:
        erros.append(f"Não foi possível acessar {conteudo}: {erro}")
        return

    for item in itens:
        try:
            if item.is_symlink() or not item.is_dir():
                item.unlink()
            else:
                shutil.rmtree(item)
        except OSError as erro:
            erros.append(f"Não foi possível remover {item}: {erro}")


def limpar_lixo() -> None:
    print("\nLimpando arquivos temporários seguros e a lixeira...")
    erros: list[str] = []
    data_home = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
    cache_home = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))

    # A lixeira é esvaziada porque isso foi solicitado explicitamente.
    limpar_diretorio(data_home / "Trash" / "files", erros)
    limpar_diretorio(data_home / "Trash" / "info", erros)
    # Miniaturas podem ser recriadas pelos aplicativos.
    limpar_diretorio(cache_home / "thumbnails", erros)

    # Limpa somente o cache de pacotes baixados; não remove programas instalados.
    if shutil.which("apt-get"):
        print("Limpando o cache de pacotes do sistema (pode pedir sua senha do Linux)...")
        try:
            resultado = subprocess.run(["sudo", "apt-get", "clean"], check=False)
            if resultado.returncode != 0:
                erros.append("Não foi possível limpar o cache de pacotes do sistema.")
        except OSError as erro:
            erros.append(f"Não foi possível iniciar a limpeza do cache de pacotes: {erro}")

    if erros:
        print("\nLimpeza concluída com erros:")
        for erro in erros:
            print(f"- {erro}")
    else:
        print("\nBomba limpada com sucesso!!")


def mostrar_armazenamento() -> None:
    try:
        uso = shutil.disk_usage(Path.home())
        gib = 1024 ** 3
        print("\nArmazenamento do disco que contém sua pasta pessoal:")
        print(f"Livre: {uso.free / gib:.2f} GB")
        print(f"Usado: {(uso.total - uso.free) / gib:.2f} GB")
        print(f"Total: {uso.total / gib:.2f} GB")
    except OSError as erro:
        print(f"\nNão foi possível consultar o armazenamento: {erro}")


def executar_atualizacao(comando: list[str], nome: str) -> bool:
    print(f"\n{nome}...")
    try:
        resultado = subprocess.run(comando, check=False)
    except OSError as erro:
        print(f"Erro ao iniciar {nome.lower()}: {erro}")
        return False
    if resultado.returncode != 0:
        print(f"O comando de {nome.lower()} terminou com erro (código {resultado.returncode}).")
        return False
    return True


def atualizar() -> None:
    print("\nProcurando e instalando atualizações disponíveis...")
    sucesso = True
    apt = shutil.which("apt-get")
    if apt:
        if executar_atualizacao(["sudo", apt, "update"], "Verificação de atualizações do sistema"):
            sucesso = executar_atualizacao(
                ["sudo", apt, "upgrade", "-y"], "Atualização do sistema e dos aplicativos APT"
            ) and sucesso
        else:
            sucesso = False

    flatpak = shutil.which("flatpak")
    if flatpak:
        sucesso = executar_atualizacao(
            [flatpak, "update", "--assumeyes"], "Atualização dos aplicativos Flatpak"
        ) and sucesso

    snap = shutil.which("snap")
    if snap:
        sucesso = executar_atualizacao(["sudo", snap, "refresh"], "Atualização dos aplicativos Snap") and sucesso

    if sucesso:
        print("\nAtualizações concluídas.")
    else:
        print("\nA atualização terminou com um ou mais erros; veja as mensagens acima.")


def mostrar_menu() -> None:
    print("\nAcesso liberado, o que você deseja hoje?\n")
    print("[1] Limpar lixo")
    print("[2] Ver armazenamento")
    print("[3] Atualizar")
    print("[4] Sair")
    print("\nby:guilhermeexzk")


def voltar_ou_sair() -> bool:
    while True:
        print("\nO que deseja agora?")
        print("[1] Voltar ao menu")
        print("[2] Sair")
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            return True
        if escolha == "2":
            print("Até logo.")
            return False
        print("Opção inválida. Digite [1] ou [2].")


def main() -> None:
    try:
        print("\033[1m╔══════════════════════════════════════════════════════════════╗")
        print("║                      Bem vindo(a)!!                          ║")
        print("║                                                              ║")
        print("║ Informe a senha e tenha acesso ao melhor script             ║")
        print("╚══════════════════════════════════════════════════════════════╝\033[0m\n")
        senha = getpass("Senha: ")
        if senha != SENHA_CORRETA:
            print("Senha incorreta.")
            return

        while True:
            mostrar_menu()
            escolha = input("Escolha: ").strip()
            if escolha == "1":
                limpar_lixo()
            elif escolha == "2":
                mostrar_armazenamento()
            elif escolha == "3":
                atualizar()
            elif escolha == "4":
                print("Até logo.")
                return
            else:
                print("Opção inválida. Digite [1], [2], [3] ou [4].")
                continue

            if not voltar_ou_sair():
                return
    except (EOFError, KeyboardInterrupt):
        print("\nAté logo.")


if __name__ == "__main__":
    main()
