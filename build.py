"""Gera o site estático em dist/ (usado pelo Netlify). Só usa a biblioteca padrão."""
import shutil
from pathlib import Path

from banco import banco_json, montar_banco

RAIZ = Path(__file__).parent
DIST = RAIZ / "dist"


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(RAIZ / "web", DIST)
    (DIST / "words.json").write_text(banco_json(), encoding="utf-8")
    total = len(montar_banco())
    print(f"dist/ gerado com {total} palavras.")


if __name__ == "__main__":
    main()
