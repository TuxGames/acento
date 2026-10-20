const $ = (s) => document.querySelector(s);

const PONTOS = { tudo: 2, parcial: 1, erro: -1 };
const NIVEIS = ["normal", "dificil", "misto"];
const CHAVE = "acentua-ai:v1";
const DESCRICOES = {
  normal: "A palavra sozinha já diz se tem acento.",
  dificil: "Sem o acento, a palavra vira OUTRA. Leia a frase — é o sentido que decide.",
  misto: "Normal e difícil juntos, embaralhados.",
};
const TITULOS = {
  tudo: "Acertou tudo! +2",
  parcial: "Tem acento, mas o lugar tá errado. +1",
  erro: "Errou! −1",
};

let REGRAS = {};
let PORPALAVRA = new Map();   // palavra -> entrada
let LISTAS = {};              // nivel -> [palavra, ...]
let estado;                   // salvo no navegador
let fase = "carregando";      // pergunta | local | resultado | carregando

/* ---------- estado salvo ---------- */
const placarZerado = () => ({ pontos: 0, sequencia: 0, melhor_sequencia: 0, acertos: 0, parciais: 0, erros: 0, rodadas: 0 });

function carregarEstado() {
  let s = null;
  try { s = JSON.parse(localStorage.getItem(CHAVE)); } catch (_) { /* sem storage */ }
  if (!s || !NIVEIS.includes(s.nivel)) s = { nivel: "normal", recordes: {} };
  s.placar = s.placar || placarZerado();
  s.recordes = s.recordes || {};
  s.baralho = (s.baralho || []).filter((p) => PORPALAVRA.has(p));
  if (s.atual && !PORPALAVRA.has(s.atual)) s.atual = null;
  return s;
}

function salvar() {
  try { localStorage.setItem(CHAVE, JSON.stringify(estado)); } catch (_) { /* tudo bem */ }
}

function zerarPartida(nivel) {
  estado = { nivel, recordes: estado.recordes, placar: placarZerado(), baralho: [], atual: null };
  salvar();
}

function embaralhar(lista) {
  const a = lista.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function palavraAtual() {
  if (!estado.atual) {  // recarregar a página não troca a palavra
    if (!estado.baralho.length) estado.baralho = embaralhar(LISTAS[estado.nivel]);
    estado.atual = estado.baralho.pop();
    salvar();
  }
  return PORPALAVRA.get(estado.atual);
}

/* ---------- tela ---------- */
function atualizarPlacar() {
  const p = estado.placar;
  $("#p-pontos").textContent = p.pontos;
  $("#p-seq").textContent = p.sequencia;
  $("#p-recorde").textContent = estado.recordes[estado.nivel] || 0;
  $("#p-rodadas").textContent = p.rodadas;
  document.querySelectorAll(".nivel").forEach((b) => {
    const ativo = b.dataset.nivel === estado.nivel;
    b.classList.toggle("ativo", ativo);
    b.setAttribute("aria-selected", ativo);
  });
  $("#desc-nivel").textContent = DESCRICOES[estado.nivel];
}

function mostrarFase(nome) {
  fase = nome;
  $("#fase-pergunta").hidden = nome !== "pergunta";
  $("#fase-local").hidden = nome !== "local";
  $("#fase-resultado").hidden = nome !== "resultado";
}

function desenharPalavra(texto, { clicavel = false, certa = null, errada = null } = {}) {
  const box = $("#palavra");
  box.innerHTML = "";
  Array.from(texto).forEach((ch, i) => {
    const el = document.createElement(clicavel ? "button" : "div");
    el.className = "letra";
    el.textContent = ch;
    if (i === certa) el.classList.add("certa");
    if (i === errada) el.classList.add("errada");
    if (clicavel) {
      el.type = "button";
      el.title = "O acento fica aqui";
      el.addEventListener("click", () => responder(true, i));
    }
    box.appendChild(el);
  });
  box.classList.remove("pop"); void box.offsetWidth; box.classList.add("pop");
}

function desenharFrase(frase, preenchida = null) {
  const el = $("#frase");
  el.innerHTML = "";
  el.hidden = !frase;
  if (!frase) return;
  const [antes, depois] = frase.split("___");
  const lacuna = document.createElement("span");
  lacuna.className = "lacuna";
  lacuna.textContent = preenchida ?? "_____";
  el.append(antes, lacuna, depois ?? "");
}

function perguntaTexto(p) {
  return p.frase ? "Nessa frase, a palavra tem acento?" : "Essa palavra tem acento?";
}

function proximaPalavra() {
  const p = palavraAtual();
  atualizarPlacar();
  desenharPalavra(p.mostrada);
  desenharFrase(p.frase);
  $("#instrucao").textContent = perguntaTexto(p);
  mostrarFase("pergunta");
}

function pedirLocal() {
  $("#instrucao").textContent = "Em qual letra fica o acento? Toque nela.";
  desenharPalavra(PORPALAVRA.get(estado.atual).mostrada, { clicavel: true });
  mostrarFase("local");
}

function voltar() {
  const p = PORPALAVRA.get(estado.atual);
  $("#instrucao").textContent = perguntaTexto(p);
  desenharPalavra(p.mostrada);
  mostrarFase("pergunta");
}

/* ---------- regra do jogo ---------- */
function responder(disseQueTem, posicao = null) {
  if (fase !== "pergunta" && fase !== "local") return;
  const p = PORPALAVRA.get(estado.atual);
  const tem = p.pos !== null;

  let resultado;
  if (!tem) resultado = disseQueTem ? "erro" : "tudo";
  else if (!disseQueTem) resultado = "erro";
  else resultado = posicao === p.pos ? "tudo" : "parcial";

  const s = estado.placar;
  s.pontos += PONTOS[resultado];
  s.rodadas += 1;
  if (resultado === "tudo") {
    s.acertos += 1;
    s.sequencia += 1;
    s.melhor_sequencia = Math.max(s.melhor_sequencia, s.sequencia);
  } else {
    s[resultado === "parcial" ? "parciais" : "erros"] += 1;
    s.sequencia = 0;
  }
  estado.recordes[estado.nivel] = Math.max(estado.recordes[estado.nivel] || 0, s.pontos);
  estado.atual = null;  // impede responder a mesma palavra duas vezes
  salvar();

  const escolhida = disseQueTem ? posicao : null;
  const errada = escolhida !== null && escolhida !== p.pos ? escolhida : null;
  desenharPalavra(p.mostrada, { certa: p.pos, errada });
  desenharFrase(p.frase, p.palavra);

  const fb = $("#feedback");
  fb.className = `feedback ${resultado}`;
  fb.innerHTML = "";
  fb.append(TITULOS[resultado]);
  const correta = document.createElement("span");
  correta.className = "correta";
  correta.textContent = p.palavra;
  fb.appendChild(correta);

  $("#par").hidden = !p.par;
  $("#par").textContent = p.par || "";
  $("#regra").textContent = REGRAS[p.regra];
  $("#instrucao").textContent = tem ? "O acento fica na letra destacada." : "Aqui ela não tem acento.";
  atualizarPlacar();
  mostrarFase("resultado");
  $("#btn-proxima").focus();
}

function novoJogo(nivel = estado.nivel, perguntar = true) {
  if (perguntar && estado.placar.rodadas > 0 && !confirm("Zerar o placar e começar de novo?")) return;
  zerarPartida(nivel);
  proximaPalavra();
}

/* ---------- eventos ---------- */
document.querySelectorAll(".nivel").forEach((b) => {
  b.addEventListener("click", () => {
    const n = b.dataset.nivel;
    if (fase === "carregando" || n === estado.nivel) return;
    if (estado.placar.rodadas > 0 && !confirm("Trocar de nível zera o placar desta partida. Continuar?")) return;
    novoJogo(n, false);
  });
});

$("#btn-sim").addEventListener("click", pedirLocal);
$("#btn-nao").addEventListener("click", () => responder(false));
$("#btn-voltar").addEventListener("click", voltar);
$("#btn-proxima").addEventListener("click", proximaPalavra);
$("#btn-reiniciar").addEventListener("click", () => fase !== "carregando" && novoJogo());

document.addEventListener("keydown", (e) => {
  const k = e.key.toLowerCase();
  if (fase === "pergunta" && k === "s") pedirLocal();
  else if (fase === "pergunta" && k === "n") responder(false);
  else if (fase === "local" && k === "escape") voltar();
  else if (fase === "resultado" && k === "enter") { e.preventDefault(); proximaPalavra(); }
});

/* ---------- início ---------- */
async function iniciar() {
  try {
    const r = await fetch("words.json", { cache: "no-cache" });
    const dados = await r.json();
    REGRAS = dados.regras;
    PORPALAVRA = new Map(dados.palavras.map((p) => [p.palavra, p]));
    LISTAS = {
      normal: dados.palavras.filter((p) => p.nivel === "normal").map((p) => p.palavra),
      dificil: dados.palavras.filter((p) => p.nivel === "dificil").map((p) => p.palavra),
      misto: dados.palavras.map((p) => p.palavra),
    };
    document.querySelectorAll("[data-contagem]").forEach((el) => {
      el.textContent = LISTAS[el.dataset.contagem].length;
    });
    estado = carregarEstado();
    proximaPalavra();
  } catch (e) {
    $("#instrucao").textContent = "Não consegui carregar as palavras. Recarregue a página.";
    console.error(e);
  }
}

iniciar();
