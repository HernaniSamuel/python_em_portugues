# pt2py_burro.py
import json
import sys
from pathlib import Path
import re

# Carrega dicionários invertidos pt -> py
def carregar_dicionario_pt_para_py():
    pasta = Path("portugues_para_python")
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

    # Cria lista ordenada por tamanho (maiores primeiro) para capturar operadores multi-caractere
    chaves_ordenadas = sorted(dicionario.keys(), key=len, reverse=True)

    while i < len(linha):
        char = linha[i]

        if char.isspace():
            nova_linha += char
            i += 1
            continue

        # Primeiro tenta encontrar a maior correspondência possível (operadores multi-caractere)
        encontrou = False
        for chave in chaves_ordenadas:
            if linha[i:].startswith(chave):
                # Verifica se é uma palavra completa (não parte de outra palavra)
                if chave.replace('_', '').isalpha():  # É uma palavra
                    # Verifica limites de palavra
                    inicio_ok = i == 0 or not linha[i-1].isalnum() and linha[i-1] != '_'
                    fim_ok = (i + len(chave)) >= len(linha) or not linha[i + len(chave)].isalnum() and linha[i + len(chave)] != '_'
                    if inicio_ok and fim_ok:
                        nova_linha += dicionario[chave]
                        i += len(chave)
                        encontrou = True
                        break
                else:  # É um operador ou símbolo
                    nova_linha += dicionario[chave]
                    i += len(chave)
                    encontrou = True
                    break

        if not encontrou:
            # Se não encontrou correspondência, tenta capturar palavra normal
            match = re.match(r"[a-zA-Z0-9_áéíóúâêôãõçÁÉÍÓÚÂÊÔÃÕÇ]+", linha[i:])
            if match:
                palavra = match.group(0)
                nova_linha += dicionario.get(palavra, palavra)
                i += len(palavra)
            else:
                # Caractere individual
                nova_linha += char
                i += 1

    return nova_linha


def traduzir_texto_para_py(caminho_txt, dicionario):
    with open(caminho_txt, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    resultado = [traduz_linha_burra(linha, dicionario) for linha in linhas]

    caminho_saida = Path(caminho_txt).with_suffix(".py")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.writelines(resultado)

    print(f"✅ Tradução concluída: {caminho_saida}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python pt2py_burro.py arquivo.txt")
        sys.exit(1)

    dicionario = carregar_dicionario_pt_para_py()
    traduzir_texto_para_py(sys.argv[1], dicionario)