"""Monta e valida o banco de palavras a partir de words.py (fonte única)."""
import json
import unicodedata

from words import PARES, RULES, WORDS

# Só agudo e circunflexo contam como acento no jogo. Til e cedilha ficam visíveis.
ACCENT_MARKS = {"́", "̂"}


def analisar(palavra):
    """Retorna (palavra_sem_acento, indice_da_letra_acentuada_ou_None)."""
    mostrada, pos = [], None
    for i, ch in enumerate(palavra):
        decomposto = unicodedata.normalize("NFD", ch)
        if any(m in decomposto for m in ACCENT_MARKS):
            if pos is not None:
                raise ValueError(f"'{palavra}' tem mais de um acento — o jogo suporta só um.")
            pos = i
            decomposto = "".join(c for c in decomposto if c not in ACCENT_MARKS)
        mostrada.append(unicodedata.normalize("NFC", decomposto))
    return "".join(mostrada), pos


def montar_banco():
    banco, vistas = [], set()
    fontes = [(item, "normal") for item in WORDS] + [(item, "dificil") for item in PARES]
    for item, nivel in fontes:
        if nivel == "normal" and len(item) != 2:
            raise ValueError(f"Nível normal usa (palavra, regra): {item}")
        if nivel == "dificil" and len(item) != 4:
            raise ValueError(f"Nível difícil usa (palavra, regra, frase, par): {item}")
        palavra, regra = item[0], item[1]
        if regra not in RULES:
            raise ValueError(f"Regra desconhecida '{regra}' em '{palavra}'.")
        if palavra in vistas:
            raise ValueError(f"Palavra repetida: '{palavra}'.")
        vistas.add(palavra)
        mostrada, pos = analisar(palavra)
        if RULES[regra][0] != (pos is not None):
            raise ValueError(f"'{palavra}' está na regra {regra}, que não bate com a palavra.")
        if nivel == "dificil" and "___" not in item[2]:
            raise ValueError(f"A frase de '{palavra}' precisa ter a lacuna ___.")
        banco.append({
            "palavra": palavra, "mostrada": mostrada, "pos": pos, "regra": regra,
            "nivel": nivel,
            "frase": item[2] if nivel == "dificil" else None,
            "par": item[3] if nivel == "dificil" else None,
        })
    return banco


def banco_json():
    dados = {
        "regras": {codigo: texto for codigo, (_, texto) in RULES.items()},
        "palavras": montar_banco(),
    }
    return json.dumps(dados, ensure_ascii=False, separators=(",", ":"))
