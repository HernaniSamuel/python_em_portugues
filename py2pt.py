# py2pt_burro.py
import json
import sys
from pathlib import Path
import re


# pega os dicionários de python para português
def carregar_dicionario_py_para_pt():
    pasta = Path("python_para_portugues")
    arquivos = ["palavras.json", "builtins.json", "operadores.json", "tipos.json"]
    dicionario = {}
    for nome in arquivos:
        caminho = pasta / nome
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
            dicionario.update(dados)
    return dicionario

# Traduz palavra por palavra preservando formatação
def traduz_linha_burra(linha, dicionario):
    nova_linha = ""
    i = 0
    dentro_de_string = False
    aspas_atual = None

    # Ignora comentários de linha
    if linha.strip().startswith("#"):
        return linha

    # Ignora blocos de comentário com aspas triplas
    if linha.strip().startswith(('"""', "'''")):
        return linha

    while i < len(linha):
        char = linha[i]

        # Início/fim de string
        if char in {"'", '"'}:
            if not dentro_de_string:
                dentro_de_string = True
                aspas_atual = char
            elif linha[i] == aspas_atual:
                dentro_de_string = False
            nova_linha += char
            i += 1
            continue

        if dentro_de_string:
            nova_linha += char
            i += 1
            continue

        # Espaço
        if char.isspace():
            nova_linha += char
            i += 1
            continue

        # Palavras
        if re.match(r"[a-zA-Z0-9_]", char):
            palavra = ""
            while i < len(linha) and re.match(r"[a-zA-Z0-9_]", linha[i]):
                palavra += linha[i]
                i += 1
            nova_linha += dicionario.get(palavra, palavra)
            continue

        # Operador de 3 caracteres
        if i + 2 < len(linha):
            tres = linha[i:i+3]
            if tres in dicionario:
                antes = linha[i-1] if i > 0 else " "
                depois = linha[i+3] if i+3 < len(linha) else " "
                if antes.isspace() and depois.isspace():
                    nova_linha += dicionario[tres]
                    i += 3
                    continue

        # Operador de 2 caracteres
        if i + 1 < len(linha):
            dois = linha[i:i+2]
            if dois in dicionario:
                antes = linha[i-1] if i > 0 else " "
                depois = linha[i+2] if i+2 < len(linha) else " "
                if antes.isspace() and depois.isspace():
                    nova_linha += dicionario[dois]
                    i += 2
                    continue

        # Operador de 1 caractere
        if char in dicionario:
            antes = linha[i-1] if i > 0 else " "
            depois = linha[i+1] if i+1 < len(linha) else " "
            if antes.isspace() and depois.isspace():
                nova_linha += dicionario[char]
            else:
                nova_linha += char
        else:
            nova_linha += char

        i += 1

    return nova_linha

def traduzir_texto_para_pt(caminho_py, dicionario):
    with open(caminho_py, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    resultado = []
    dentro_de_bloco_string = False

    for linha in linhas:
        # Detecta """ ou ''' (início ou fim)
        if '"""' in linha or "'''" in linha:
            if not dentro_de_bloco_string:
                dentro_de_bloco_string = True
            else:
                dentro_de_bloco_string = False
            resultado.append(linha)
            continue

        if dentro_de_bloco_string:
            resultado.append(linha)
        else:
            resultado.append(traduz_linha_burra(linha, dicionario))

    caminho_saida = Path(caminho_py).with_suffix(".txt")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.writelines(resultado)

    print(f"✅ Tradução salva em: {caminho_saida}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python py2pt.py arquivo.py")
        sys.exit(1)

    dicionario = carregar_dicionario_py_para_pt()
    traduzir_texto_para_pt(sys.argv[1], dicionario)
