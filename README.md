# Otimizion

Utilitário simples de limpeza para Windows e Linux, incluindo Zorin OS e Ubuntu. O mesmo arquivo `otimizion.py` funciona nos dois sistemas e mantém o menu em terminal do Otimizion.

## O que ele faz

- Limpa arquivos temporários com mais de 7 dias. No Linux, limita a limpeza de `/tmp` a arquivos pertencentes ao usuário atual e remove miniaturas regeneráveis.
- Esvazia a Lixeira do usuário atual.
- No Linux, oferece liberar caches recuperáveis de RAM após confirmação e autorização do sistema. Isso pode deixar a abertura de arquivos mais lenta por um tempo.
- No Windows, abre o Gerenciador de Tarefas para consultar a RAM. O Windows gerencia a memória em cache automaticamente.

O Otimizion não atualiza o sistema, não remove programas instalados e não apaga documentos fora da Lixeira.

**PIN do menu: `223542`.** Como o repositório é público, o PIN e o código ficam visíveis para qualquer pessoa; ele serve apenas como uma confirmação simples antes de abrir o menu.

## Windows

1. Instale o Python 3.10 ou mais recente pelo site oficial [python.org](https://www.python.org/downloads/). Durante a instalação, marque **Add Python to PATH**.
2. Nesta página do GitHub, abra `otimizion.py` e escolha **Download raw file** (ou **Raw** e depois salve o arquivo).
3. Abra o Terminal ou Prompt de Comando na pasta onde salvou o arquivo.
4. Execute:

   ```powershell
   py otimizion.py
   ```

   Se `py` não funcionar, tente `python otimizion.py`.

5. Escolha a opção desejada no menu. O Windows pode manter temporários que estejam sendo usados por algum programa.

## Zorin OS / Ubuntu

1. Abra o Terminal na pasta onde salvou `otimizion.py`.
2. Execute:

   ```bash
   python3 otimizion.py
   ```

3. Escolha uma opção no menu. Para liberar cache recuperável de RAM, escolha a opção 3 e confirme; o sistema pedirá autorização.

### Manter o Otimizion no menu do Zorin

Se o atalho atual já abre o arquivo `otimizion.py`, substitua esse arquivo pela versão baixada e mantenha o atalho. Se você mudou a pasta do arquivo, edite o atalho do aplicativo para apontar para o novo caminho e mantenha a opção **Executar em terminal** ativada.

## Baixar o arquivo

Use o botão **Code → Download ZIP** para baixar o projeto completo, ou abra `otimizion.py` e baixe somente o arquivo. Para o uso normal, basta esse único arquivo Python.
