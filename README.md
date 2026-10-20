# Acentua Aí

Jogo pra treinar acentuação: aparece uma palavra sem acento agudo/circunflexo e o jogador diz se ela tem acento — e, se tiver, toca na letra onde ele fica.

**Pontuação**
- Acertou tudo (tem acento + lugar certo, ou disse que não tem e não tem): **+2**
- Disse que tem, tem, mas errou o lugar: **+1**
- Errou se tem ou não: **−1**

**Níveis**
- **Normal** — a palavra sozinha já resolve.
- **Difícil** — sem o acento, a palavra vira outra (sábia/sabia/sabiá, está/esta, pôde/pode…). Uma frase com lacuna decide.
- **Misto** — os dois juntos.

Depois de cada resposta aparece a palavra certa, o par (no difícil) e a regra de acentuação. Placar e recorde por nível ficam salvos no navegador.

## Como está organizado

```
words.py      # fonte única das palavras e regras (edite aqui)
banco.py      # valida o banco e gera o JSON
build.py      # gera o site estático em dist/ (Netlify)
web/          # o jogo (HTML/CSS/JS) — roda todo no navegador
app.py        # servidor Flask opcional (PythonAnywhere / local)
netlify.toml  # config do Netlify
```

## Netlify

Já configurado no `netlify.toml`: build `python3 build.py`, publish `dist`.
Conecte o repositório no Netlify (Add new site → Import an existing project → GitHub → `acento`) e todo push na `main` publica sozinho.

## Rodar local

```bash
python3 build.py && python3 -m http.server -d dist 8000   # versão estática
# ou
pip install -r requirements.txt && python3 app.py          # versão Flask
```

## PythonAnywhere (opcional)

WSGI:

```python
import sys
path = '/home/SEU_USUARIO/acento'
if path not in sys.path:
    sys.path.insert(0, path)
from app import app as application
```

## Adicionar palavras

Edite `words.py`.

Nível **Normal** → lista `WORDS`:

```python
("pássaro", "PROPAROX"),
```

Nível **Difícil** → lista `PARES`, sempre com frase (use `___` na lacuna) e o par explicado:

```python
("bebê", "OXI_AEO", "O ___ está dormindo.", "bebê (criança) × bebe (verbo beber)"),
("bebe", "PAROX_COMUM", "Ele ___ muita água.", "bebê (criança) × bebe (verbo beber)"),
```

Coloque sempre os dois lados do par, senão o difícil fica viciado em "sim".
O build falha com mensagem clara se uma regra não bater com a palavra, se houver palavra repetida ou frase sem lacuna — então um erro em `words.py` nunca vai pro ar.
