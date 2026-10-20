"""Gera o site estático em dist/ (usado pelo Netlify). Só usa a biblioteca padrão."""
import shutil
from pathlib import Path

from banco import banco_json, montar_banco, montar_ortografia

RAIZ = Path(__file__).parent
DIST = RAIZ / "dist"


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(RAIZ / "web", DIST)
    (DIST / "words.json").write_text(banco_json(), encoding="utf-8")
    print(f"dist/ gerado: {len(montar_banco())} de acentuação, {len(montar_ortografia())} de ortografia.")


if __name__ == "__main__":
    main()
