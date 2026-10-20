const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);

const NOME = "Gustavo";
const CHAVE = "gva:v2";
const CHAVE_ANTIGA = "acentua-ai:v1";
const MODOS = ["normal", "dificil", "misto", "ortografia"];
const PONTOS = { tudo: 2, parcial: 1, erro: -1 };

const DESCRICOES = {
  normal: "A palavra sozinha já diz se tem acento.",
  dificil: "Sem o acento, a palavra vira OUTRA. Leia a frase — é o sentido que decide.",
  misto: "Normal e difícil juntos, embaralhados.",
  ortografia: "S ou Z? SS ou Ç? X ou CH? G ou J? Escolha o que completa a palavra.",
};

const FRASES = {
  tudo: [`Boa, ${NOME}!`, `Mandou bem, ${NOME}!`, `Isso aí, ${NOME}!`, `O Analfabetismo apanhou dessa, ${NOME}!`, `Brabo, ${NOME}!`, `Na mosca, ${NOME}!`],
  parcial: [`Quase, ${NOME}! Tem acento, mas não nessa letra.`, `Meio certo, ${NOME}: tem acento, mas o lugar tá errado.`],
  erro: [`Ih, ${NOME}…`, `Ponto pro Analfabetismo, ${NOME}.`, `Essa o Analfabetismo levou, ${NOME}.`, `Não foi dessa vez, ${NOME}.`, `Vacilou, ${NOME}!`],
};
const sortear = (lista) => lista[Math.floor(Math.random() * lista.length)];
const sinal = (n) => (n > 0 ? `+${n}` : `−${Math.abs(n)}`);

let REGRAS = {}, ORTO_REGRAS = {};
let ITENS = new Map();  // id -> item (tipo: "acento" | "ortografia")
let LISTAS = {};        // modo -> [id, ...]
let estado;
let fase = "carregando"; // pergunta | local | opcoes | resultado | carregando

/* ================= estado salvo no navegador ================= */
const placarZerado = () => ({ pontos: 0, sequencia: 0, acertos: 0, parciais: 0, erros: 0, rodadas: 0, bateuRecorde: false });
const estadoNovo = () => ({ modo: "normal", ultimoAcento: "normal", modos: {}, geral: { gustavo: 0, analf: 0 } });

function modoEstado(m = estado.modo) {
  if (!estado.modos[m]) estado.modos[m] = { placar: placarZerado(), baralho: [], atual: null, recorde: 0, melhorSeq: 0 };
  return estado.modos[m];
}

function lerJSON(chave) {
  try { return JSON.parse(localStorage.getItem(chave)); } catch (_) { return null; }
}

function migrarV1(v1) {
  const s = estadoNovo();
  estado = s;
  const nivel = MODOS.includes(v1.nivel) ? v1.nivel : "normal";
  Object.entries(v1.recordes || {}).forEach(([n, r]) => { if (MODOS.includes(n)) modoEstado(n).recorde = r; });
  const p = v1.placar || {};
  const me = modoEstado(nivel);
  me.placar = { ...placarZerado(), ...p };
  me.melhorSeq = p.melhor_sequencia || 0;
  s.modo = nivel;
  s.ultimoAcento = nivel;
  s.geral.gustavo = (p.acertos || 0) + (p.parciais || 0);
  s.geral.analf = p.erros || 0;
  return s;
}

function carregarEstado() {
  let s = lerJSON(CHAVE);
  if (!s) {
    const v1 = lerJSON(CHAVE_ANTIGA);
    s = v1 ? migrarV1(v1) : estadoNovo();
  }
  if (!MODOS.includes(s.modo)) s.modo = "normal";
  if (!["normal", "dificil", "misto"].includes(s.ultimoAcento)) s.ultimoAcento = "normal";
  s.modos = s.modos || {};
  s.geral = { gustavo: 0, analf: 0, ...(s.geral || {}) };
  estado = s;
  MODOS.forEach((m) => {
    const me = modoEstado(m);
    me.placar = { ...placarZerado(), ...me.placar };
    me.baralho = (me.baralho || []).filter((id) => LISTAS[m].includes(id));
    if (me.atual && !LISTAS[m].includes(me.atual)) me.atual = null;
  });
  salvar();
}

function salvar() {
  try { localStorage.setItem(CHAVE, JSON.stringify(estado)); } catch (_) { /* sem storage: joga sem salvar */ }
}

function embaralhar(lista) {
  const a = lista.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function itemAtual() {
  const me = modoEstado();
  if (!me.atual) {  // recarregar a página não troca a palavra
    if (!me.baralho.length) me.baralho = embaralhar(LISTAS[estado.modo]);
    me.atual = me.baralho.pop();
    salvar();
  }
  return ITENS.get(me.atual);
}

/* ================= tela ================= */
function renderTopo() {
  const g = estado.geral;
  $("#b-gustavo").textContent = g.gustavo;
  $("#b-analf").textContent = g.analf;
  const total = g.gustavo + g.analf;
  $("#b-barra").style.width = `${total ? (100 * g.gustavo) / total : 50}%`;

  const me = modoEstado();
  $("#p-pontos").textContent = me.placar.pontos;
  $("#p-seq").textContent = me.placar.sequencia;
  $("#p-recorde").textContent = me.recorde;
  $("#p-melhor").textContent = me.melhorSeq;

  const orto = estado.modo === "ortografia";
  $$(".modo").forEach((b) => b.classList.toggle("ativo", b.dataset.grupo === (orto ? "ortografia" : "acento")));
  $$(".nivel").forEach((b) => b.classList.toggle("ativo", b.dataset.modo === estado.modo));
  $("#niveis").hidden = orto;
  $("#desc-modo").textContent = DESCRICOES[estado.modo];
  $("#regras-pontos").innerHTML = orto
    ? "<b>Acertou:</b> +2 · <b>Errou:</b> −1"
    : "<b>Tudo certo:</b> +2 · <b>Tem acento, lugar errado:</b> +1 · <b>Errou:</b> −1";
  $("#nota-modo").textContent = orto
    ? "Aqui a palavra já vem com os acentos — só falta a letra."
    : "Só contam acento agudo (´) e circunflexo (^). O til (~) e o ç já aparecem na palavra.";
}

function mostrarFase(nome) {
  fase = nome;
  $("#fase-pergunta").hidden = nome !== "pergunta";
  $("#fase-local").hidden = nome !== "local";
  $("#fase-opcoes").hidden = nome !== "opcoes";
  $("#fase-resultado").hidden = nome !== "resultado";
}

function tile(texto, classes = [], aoClicar = null) {
  const el = document.createElement(aoClicar ? "button" : "div");
  el.className = ["letra", ...classes].join(" ");
  el.textContent = texto;
  if (aoClicar) { el.type = "button"; el.addEventListener("click", aoClicar); }
  return el;
}

function animar(box) { box.classList.remove("pop"); void box.offsetWidth; box.classList.add("pop"); }

function desenharAcento(texto, { clicavel = false, certa = null, errada = null } = {}) {
  const box = $("#palavra");
  box.innerHTML = "";
  Array.from(texto).forEach((ch, i) => {
    const cls = [];
    if (i === certa) cls.push("certa");
    if (i === errada) cls.push("errada");
    const el = tile(ch, cls, clicavel ? () => responderAcento(true, i) : null);
    if (clicavel) el.title = "O acento fica aqui";
    box.appendChild(el);
  });
  animar(box);
}

function desenharOrto(item, preenchida = null, acertou = null) {
  const box = $("#palavra");
  box.innerHTML = "";
  Array.from(item.antes).forEach((ch) => box.appendChild(tile(ch)));
  const cls = ["slot"];
  if (acertou === true) cls.push("certa");
  if (acertou === false) cls.push("revelada");
  box.appendChild(tile(preenchida ?? "?", cls));
  Array.from(item.depois).forEach((ch) => box.appendChild(tile(ch)));
  animar(box);
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

function perguntaAcento(item) {
  return item.frase ? `${NOME}, nessa frase a palavra tem acento?` : `${NOME}, essa palavra tem acento?`;
}

function proxima() {
  renderTopo();
  const item = itemAtual();
  desenharFrase(item.frase);
  if (item.tipo === "acento") {
    desenharAcento(item.mostrada);
    $("#instrucao").textContent = perguntaAcento(item);
    mostrarFase("pergunta");
  } else {
    desenharOrto(item);
    $("#instrucao").textContent = item.frase ? `${NOME}, o que completa a palavra nessa frase?` : `${NOME}, o que completa a palavra?`;
    const box = $("#fase-opcoes");
    box.innerHTML = "";
    embaralhar(item.opcoes).forEach((op, i) => {
      const b = document.createElement("button");
      b.className = "btn opcao";
      b.dataset.opcao = op;
      b.innerHTML = `${op.toUpperCase()} <kbd>${i + 1}</kbd>`;
      b.addEventListener("click", () => responderOrto(op));
      box.appendChild(b);
    });
    mostrarFase("opcoes");
  }
}

function pedirLocal() {
  $("#instrucao").textContent = `Em qual letra fica o acento, ${NOME}? Toque nela.`;
  desenharAcento(ITENS.get(modoEstado().atual).mostrada, { clicavel: true });
  mostrarFase("local");
}

function voltar() {
  const item = ITENS.get(modoEstado().atual);
  $("#instrucao").textContent = perguntaAcento(item);
  desenharAcento(item.mostrada);
  mostrarFase("pergunta");
}

/* ================= pontuação ================= */
function registrar(resultado) {
  const me = modoEstado();
  const s = me.placar;
  const recordeAntes = me.recorde;
  s.pontos += PONTOS[resultado];
  s.rodadas += 1;
  if (resultado === "tudo") { s.acertos += 1; s.sequencia += 1; }
  else { s[resultado === "parcial" ? "parciais" : "erros"] += 1; s.sequencia = 0; }
  me.melhorSeq = Math.max(me.melhorSeq, s.sequencia);
  me.recorde = Math.max(me.recorde, s.pontos);
  if (resultado === "erro") estado.geral.analf += 1; else estado.geral.gustavo += 1;
  me.atual = null;  // impede responder a mesma palavra duas vezes

  const extras = [];
  if (resultado === "tudo" && s.sequencia >= 5 && s.sequencia % 5 === 0) extras.push(`🔥 ${s.sequencia} seguidas, ${NOME}!`);
  if (me.recorde > recordeAntes && recordeAntes > 0 && !s.bateuRecorde) {
    s.bateuRecorde = true;
    extras.push(`🏆 Novo recorde, ${NOME}!`);
  }
  salvar();
  return extras;
}

function mostrarResultado(item, resultado, extras, detalhe = null) {
  const fb = $("#feedback");
  fb.className = `feedback ${resultado}`;
  fb.innerHTML = "";
  fb.append(`${sortear(FRASES[resultado])} ${sinal(PONTOS[resultado])}`);
  if (detalhe) {
    const d = document.createElement("span");
    d.className = "detalhe";
    d.textContent = detalhe;
    fb.appendChild(d);
  }
  const correta = document.createElement("span");
  correta.className = "correta";
  correta.textContent = item.palavra;
  fb.appendChild(correta);
  extras.forEach((t) => {
    const e = document.createElement("span");
    e.className = "combo";
    e.textContent = t;
    fb.appendChild(e);
  });

  $("#par").hidden = !item.par;
  $("#par").textContent = item.par || "";
  $("#regra").textContent = item.tipo === "acento" ? REGRAS[item.regra] : ORTO_REGRAS[item.regra];
  renderTopo();
  mostrarFase("resultado");
  $("#btn-proxima").focus();
}

function responderAcento(disseQueTem, posicao = null) {
  if (fase !== "pergunta" && fase !== "local") return;
  const item = ITENS.get(modoEstado().atual);
  const tem = item.pos !== null;
  let resultado;
  if (!tem) resultado = disseQueTem ? "erro" : "tudo";
  else if (!disseQueTem) resultado = "erro";
  else resultado = posicao === item.pos ? "tudo" : "parcial";

  const extras = registrar(resultado);
  const escolhida = disseQueTem ? posicao : null;
  desenharAcento(item.mostrada, { certa: item.pos, errada: escolhida !== null && escolhida !== item.pos ? escolhida : null });
  desenharFrase(item.frase, item.palavra);
  $("#instrucao").textContent = tem ? "O acento fica na letra destacada." : "Aqui ela não tem acento.";
  mostrarResultado(item, resultado, extras);
}

function responderOrto(opcao) {
  if (fase !== "opcoes") return;
  const item = ITENS.get(modoEstado().atual);
  const acertou = opcao === item.correta;
  const resultado = acertou ? "tudo" : "erro";
  const extras = registrar(resultado);
  desenharOrto(item, item.correta, acertou);
  desenharFrase(item.frase, item.palavra);
  $("#instrucao").textContent = `Com ${item.correta.toUpperCase()}.`;
  const detalhe = acertou ? null : `Você marcou ${opcao.toUpperCase()}, mas é ${item.correta.toUpperCase()}.`;
  mostrarResultado(item, resultado, extras, detalhe);
}

/* ================= navegação ================= */
function trocarModo(m) {
  if (fase === "carregando" || m === estado.modo) return;
  estado.modo = m;
  if (m !== "ortografia") estado.ultimoAcento = m;
  salvar();
  proxima();  // cada modo guarda o próprio progresso
}

function zerar() {
  if (fase === "carregando") return;
  const me = modoEstado();
  if (me.placar.rodadas > 0 && !confirm(`Zerar a partida deste modo, ${NOME}? Recordes e o placar geral continuam.`)) return;
  me.placar = placarZerado();
  me.baralho = [];
  me.atual = null;
  salvar();
  proxima();
}

$$(".modo").forEach((b) => b.addEventListener("click", () => {
  trocarModo(b.dataset.grupo === "ortografia" ? "ortografia" : estado.ultimoAcento);
}));
$$(".nivel").forEach((b) => b.addEventListener("click", () => trocarModo(b.dataset.modo)));
$("#btn-sim").addEventListener("click", pedirLocal);
$("#btn-nao").addEventListener("click", () => responderAcento(false));
$("#btn-voltar").addEventListener("click", voltar);
$("#btn-proxima").addEventListener("click", proxima);
$("#btn-reiniciar").addEventListener("click", zerar);

document.addEventListener("keydown", (e) => {
  const k = e.key.toLowerCase();
  if (fase === "pergunta" && k === "s") pedirLocal();
  else if (fase === "pergunta" && k === "n") responderAcento(false);
  else if (fase === "local" && k === "escape") voltar();
  else if (fase === "opcoes" && /^[1-9]$/.test(k)) {
    const b = $$("#fase-opcoes .opcao")[Number(k) - 1];
    if (b) b.click();
  } else if (fase === "resultado" && k === "enter") { e.preventDefault(); proxima(); }
});

/* ================= início ================= */
async function iniciar() {
  try {
    const r = await fetch("words.json", { cache: "no-cache" });
    const dados = await r.json();
    REGRAS = dados.regras;
    ORTO_REGRAS = dados.orto_regras;
    dados.palavras.forEach((p) => ITENS.set(p.palavra, { ...p, id: p.palavra, tipo: "acento" }));
    dados.ortografia.forEach((o) => ITENS.set(o.id, { ...o, tipo: "ortografia" }));
    LISTAS = {
      normal: dados.palavras.filter((p) => p.nivel === "normal").map((p) => p.palavra),
      dificil: dados.palavras.filter((p) => p.nivel === "dificil").map((p) => p.palavra),
      misto: dados.palavras.map((p) => p.palavra),
      ortografia: dados.ortografia.map((o) => o.id),
    };
    $$("[data-contagem]").forEach((el) => { el.textContent = LISTAS[el.dataset.contagem].length; });
    carregarEstado();
    proxima();
  } catch (e) {
    $("#instrucao").textContent = `Deu ruim pra carregar as palavras, ${NOME}. Recarrega a página.`;
    console.error(e);
  }
}

iniciar();
