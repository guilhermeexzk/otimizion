# Otimizion

Aplicativo pessoal de manutenção do sistema, atualmente voltado para Linux (Zorin/Ubuntu). O menu oferece limpeza básica, consulta de armazenamento e atualização de pacotes disponíveis.

## Limpeza atual

A opção de limpeza esvazia a lixeira do usuário, apaga miniaturas regeneráveis e tenta limpar o cache de pacotes APT. Ela não identifica arquivos corrompidos nem varre todo o computador à procura de arquivos inúteis.

## Executar

```bash
python3 otimizion.py
```

O lançador `otimizion.desktop` pode ser ajustado para o caminho onde o projeto for instalado. A versão para Windows será planejada separadamente, com ações próprias do Windows.