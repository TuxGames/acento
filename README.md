# Gustavo vs. Analfabetismo

A luta do Gustavo contra o analfabetismo, em dois modos.

**Acentuação** — aparece uma palavra sem acento agudo/circunflexo: tem acento? Se tiver, onde?
- **Normal**: a palavra sozinha já resolve.
- **Difícil**: sem o acento, a palavra vira outra (sábia/sabia/sabiá, está/esta, pôde/pode…). Uma frase decide.
- **Misto**: os dois juntos.
- Pontos: tudo certo **+2** · tem acento mas lugar errado **+1** · errou **−1**

**Ortografia** — a palavra aparece com uma lacuna: S ou Z? SS, Ç ou S? SC? X ou CH? G ou J?
Inclui pares de mesmo som e sentido diferente (conserto/concerto, censo/senso, acender/ascender, caçar/cassar, viagem/viajem), decididos por uma frase.
- Pontos: acertou **+2** · errou **−1**

Depois de cada resposta aparece a palavra certa e a regra que explica o caso.

**Progresso salvo no navegador**: cada modo guarda os próprios pontos, sequência, recorde e melhor sequência, além do placar geral *Gustavo × Analfabetismo*. Trocar de modo não perde nada; "Zerar" reinicia só a partida do modo atual (os recordes ficam). O save é por navegador/aparelho.

## Como está organizado

```
words.py       # palavras e regras de acentuação
ortografia.py  # palavras e regras de ortografia
banco.py       # valida tudo e gera o JSON
build.py       # gera o site estático em dist/ (Netlify)
web/           # o jogo (HTML/CSS/JS) — roda todo no navegador
app.py         # servidor Flask opcional (PythonAnywhere / local)
netlify.toml   # config do Netlify
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

## Adicionar palavras

**Acentuação** (`words.py`):

```python
# nível Normal → WORDS
("pássaro", "PROPAROX"),
# nível Difícil → PARES (frase com ___ e o par explicado; coloque os dois lados do par)
("bebê", "OXI_AEO", "O ___ está dormindo.", "bebê (criança) × bebe (verbo beber)"),
("bebe", "PAROX_COMUM", "Ele ___ muita água.", "bebê (criança) × bebe (verbo beber)"),
```

**Ortografia** (`ortografia.py`) — a lacuna vai entre colchetes, as opções separadas por `/`:

```python
("ca[s]a", "s/z", "S_SOM_Z"),
("na[sc]er", "sc/ss/c", "SC"),
("con[s]erto", "s/c", "HOMOFONO", "Levei o celular pro ___.", "conserto (reparo) × concerto (apresentação musical)"),
```

O build falha com mensagem clara se algo estiver errado (regra inexistente, resposta fora das opções, palavra repetida, frase sem lacuna) — então um erro nunca vai pro ar.
