"""
Banco de palavras do Acentua Aí.

- Só acento AGUDO (´) e CIRCUNFLEXO (^) contam como "acento" no jogo.
- Til (~) e cedilha (ç) aparecem sempre na palavra mostrada.

Dois níveis:
- WORDS  (nível Normal):  (palavra, regra)
- PARES  (nível Difícil): (palavra, regra, frase_de_contexto, par)
  Palavras que, sem o acento, viram OUTRA palavra (pôde/pode, sábia/sabia/sabiá...).
  Só dá pra acertar lendo a frase. O "par" aparece no resultado pra fixar a diferença.

O app valida tudo ao iniciar: regra inexistente, palavra repetida, ou regra que não bate
com a palavra ter/não ter acento derrubam a inicialização com uma mensagem clara.
"""

# codigo: (tem_acento, explicação)
RULES = {
    # ---------- COM acento ----------
    "PROPAROX": (True, "Proparoxítona (tônica na antepenúltima sílaba): TODAS levam acento."),
    "OXI_AEO": (True, "Oxítona terminada em a(s), e(s), o(s), em, ens: leva acento."),
    "MONO_AEO": (True, "Monossílabo tônico terminado em a(s), e(s), o(s): leva acento."),
    "PAROX_TERM": (True, "Paroxítona terminada em l, n, r, x, ps, ã(s), ão(s), i(s), us, um, uns ou ditongo: leva acento."),
    "HIATO_IU": (True, "I ou U tônico em hiato com a vogal anterior, sozinho na sílaba (ou com s): leva acento (sa-ú-de, pa-ís)."),
    "DITONGO_OXI": (True, "Ditongos abertos éi, éu, ói em oxítonas e monossílabos continuam com acento (herói, chapéu, céu)."),
    "DIFERENCIAL": (True, "Acento diferencial que sobreviveu ao Novo Acordo: pôde (passado), pôr (verbo), têm e vêm (plural)."),
    # ---------- SEM acento ----------
    "PAROX_COMUM": (False, "Paroxítona terminada em a(s), e(s), o(s), em, ens: NÃO leva acento — é o caso mais comum da língua."),
    "OXI_OUTRAS": (False, "Oxítona terminada em i(s), u(s), l, r, z, im, um: NÃO leva acento (tatu, funil, jardim)."),
    "MONO_OUTROS": (False, "Monossílabo terminado em l, r, z, m etc. NÃO leva acento — só os terminados em a, e, o (com ou sem s)."),
    "MONO_ATONO": (False, "Monossílabo átono (fraco na fala, se apoia na palavra vizinha): NÃO leva acento — no, da, nos, por, e."),
    "DITONGO_SEM": (False, "Aqui o i forma ditongo com o a (pais = uma sílaba só), então não é hiato e não leva acento. Já pa-ís tem hiato e leva."),
    "DITONGO_PAROX": (False, "Ditongos abertos ei e oi em PAROXÍTONAS perderam o acento no Novo Acordo (ideia, heroico, joia)."),
    "HIATO_DOBRADO": (False, "Hiatos oo e ee perderam o acento no Novo Acordo (voo, enjoo, leem, veem)."),
    "HIATO_IU_SEM": (False, "I/U em hiato NÃO leva acento quando forma sílaba com l, m, n, r, z (ru-im, ju-iz, ca-ir) ou vem antes de nh (ra-i-nha)."),
    "IU_POS_DITONGO": (False, "Em paroxítonas, i/u tônico logo depois de ditongo perdeu o acento no Novo Acordo (fei-u-ra, bai-u-ca)."),
    "DIFERENCIAL_EXTINTO": (False, "Esse acento diferencial caiu no Novo Acordo: para, pelo, pera, polo ficam sem acento."),
    "DIFERENCIAL_SEM": (False, "Sem acento: tem/vem (singular) e pode (presente). O acento só aparece em têm/vêm (plural) e pôde (passado)."),
    "TIL": (False, "Til (~) não é acento gráfico — ele marca nasalização. Não tem agudo nem circunflexo aqui."),
}

# =====================================================================
# NÍVEL NORMAL — a palavra sozinha já diz tudo
# =====================================================================
WORDS = [
    # ===== PROPAROXÍTONAS =====
    ("lâmpada", "PROPAROX"),
    ("pássaro", "PROPAROX"),
    ("árvore", "PROPAROX"),
    ("sílaba", "PROPAROX"),
    ("matemática", "PROPAROX"),
    ("física", "PROPAROX"),
    ("química", "PROPAROX"),
    ("fôlego", "PROPAROX"),
    ("pêssego", "PROPAROX"),
    ("rápido", "PROPAROX"),
    ("cômodo", "PROPAROX"),
    ("ônibus", "PROPAROX"),
    ("relâmpago", "PROPAROX"),
    ("sábado", "PROPAROX"),
    ("xícara", "PROPAROX"),
    ("lágrima", "PROPAROX"),
    ("próximo", "PROPAROX"),
    ("árabe", "PROPAROX"),
    ("polígono", "PROPAROX"),
    ("triângulo", "PROPAROX"),
    ("hipótese", "PROPAROX"),
    ("crisântemo", "PROPAROX"),

    # ===== OXÍTONAS com acento =====
    ("café", "OXI_AEO"),
    ("sofá", "OXI_AEO"),
    ("jacaré", "OXI_AEO"),
    ("avô", "OXI_AEO"),
    ("avó", "OXI_AEO"),
    ("você", "OXI_AEO"),
    ("maracujá", "OXI_AEO"),
    ("cajá", "OXI_AEO"),
    ("também", "OXI_AEO"),
    ("parabéns", "OXI_AEO"),
    ("armazém", "OXI_AEO"),
    ("alguém", "OXI_AEO"),
    ("picolé", "OXI_AEO"),
    ("vovó", "OXI_AEO"),
    ("robô", "OXI_AEO"),
    ("português", "OXI_AEO"),
    ("inglês", "OXI_AEO"),
    ("francês", "OXI_AEO"),

    # ===== MONOSSÍLABOS com acento =====
    ("pé", "MONO_AEO"),
    ("pá", "MONO_AEO"),
    ("só", "MONO_AEO"),
    ("já", "MONO_AEO"),
    ("chá", "MONO_AEO"),
    ("pó", "MONO_AEO"),
    ("mês", "MONO_AEO"),
    ("três", "MONO_AEO"),
    ("fé", "MONO_AEO"),

    # ===== PAROXÍTONAS com acento =====
    ("fácil", "PAROX_TERM"),
    ("difícil", "PAROX_TERM"),
    ("açúcar", "PAROX_TERM"),
    ("lápis", "PAROX_TERM"),
    ("táxi", "PAROX_TERM"),
    ("júri", "PAROX_TERM"),
    ("tênis", "PAROX_TERM"),
    ("vírus", "PAROX_TERM"),
    ("bônus", "PAROX_TERM"),
    ("álbum", "PAROX_TERM"),
    ("hífen", "PAROX_TERM"),
    ("pólen", "PAROX_TERM"),
    ("tórax", "PAROX_TERM"),
    ("bíceps", "PAROX_TERM"),
    ("órfã", "PAROX_TERM"),
    ("órgão", "PAROX_TERM"),
    ("sótão", "PAROX_TERM"),
    ("bênção", "PAROX_TERM"),
    ("ímã", "PAROX_TERM"),
    ("história", "PAROX_TERM"),
    ("série", "PAROX_TERM"),
    ("água", "PAROX_TERM"),
    ("régua", "PAROX_TERM"),
    ("ciência", "PAROX_TERM"),
    ("imóvel", "PAROX_TERM"),
    ("amável", "PAROX_TERM"),
    ("possível", "PAROX_TERM"),
    ("caráter", "PAROX_TERM"),
    ("fóssil", "PAROX_TERM"),
    ("útil", "PAROX_TERM"),
    ("jóquei", "PAROX_TERM"),
    ("vôlei", "PAROX_TERM"),

    # ===== HIATO i/u com acento =====
    ("saúde", "HIATO_IU"),
    ("baú", "HIATO_IU"),
    ("egoísta", "HIATO_IU"),
    ("juíza", "HIATO_IU"),
    ("saída", "HIATO_IU"),
    ("viúva", "HIATO_IU"),
    ("conteúdo", "HIATO_IU"),
    ("faísca", "HIATO_IU"),
    ("raízes", "HIATO_IU"),
    ("juízes", "HIATO_IU"),
    ("heroína", "HIATO_IU"),
    ("proíbe", "HIATO_IU"),
    ("graúdo", "HIATO_IU"),

    # ===== DITONGOS ABERTOS em oxítonas/monossílabos =====
    ("herói", "DITONGO_OXI"),
    ("chapéu", "DITONGO_OXI"),
    ("papéis", "DITONGO_OXI"),
    ("anéis", "DITONGO_OXI"),
    ("céu", "DITONGO_OXI"),
    ("réu", "DITONGO_OXI"),
    ("dói", "DITONGO_OXI"),
    ("constrói", "DITONGO_OXI"),
    ("troféu", "DITONGO_OXI"),
    ("pastéis", "DITONGO_OXI"),
    ("lençóis", "DITONGO_OXI"),

    # ===== SEM acento: paroxítonas comuns (inclui pegadinhas) =====
    ("casa", "PAROX_COMUM"),
    ("menino", "PAROX_COMUM"),
    ("escola", "PAROX_COMUM"),
    ("cadeira", "PAROX_COMUM"),
    ("janela", "PAROX_COMUM"),
    ("bonito", "PAROX_COMUM"),
    ("amigo", "PAROX_COMUM"),
    ("rubrica", "PAROX_COMUM"),
    ("recorde", "PAROX_COMUM"),
    ("gratuito", "PAROX_COMUM"),
    ("ibero", "PAROX_COMUM"),
    ("item", "PAROX_COMUM"),
    ("itens", "PAROX_COMUM"),
    ("hifens", "PAROX_COMUM"),
    ("jovens", "PAROX_COMUM"),
    ("homem", "PAROX_COMUM"),
    ("nuvem", "PAROX_COMUM"),
    ("ontem", "PAROX_COMUM"),
    ("viagem", "PAROX_COMUM"),
    ("garagem", "PAROX_COMUM"),
    ("imagem", "PAROX_COMUM"),

    # ===== SEM acento: oxítonas =====
    ("tatu", "OXI_OUTRAS"),
    ("urubu", "OXI_OUTRAS"),
    ("caqui", "OXI_OUTRAS"),
    ("abacaxi", "OXI_OUTRAS"),
    ("bambu", "OXI_OUTRAS"),
    ("saci", "OXI_OUTRAS"),
    ("funil", "OXI_OUTRAS"),
    ("amor", "OXI_OUTRAS"),
    ("feliz", "OXI_OUTRAS"),
    ("jardim", "OXI_OUTRAS"),
    ("sutil", "OXI_OUTRAS"),
    ("anzol", "OXI_OUTRAS"),
    ("capuz", "OXI_OUTRAS"),
    ("pudim", "OXI_OUTRAS"),
    ("comum", "OXI_OUTRAS"),

    # ===== SEM acento: monossílabos =====
    ("mel", "MONO_OUTROS"),
    ("sol", "MONO_OUTROS"),
    ("flor", "MONO_OUTROS"),
    ("paz", "MONO_OUTROS"),
    ("mar", "MONO_OUTROS"),
    ("cruz", "MONO_OUTROS"),
    ("luz", "MONO_OUTROS"),
    ("bom", "MONO_OUTROS"),
    ("sim", "MONO_OUTROS"),
    ("vez", "MONO_OUTROS"),

    # ===== SEM acento: Novo Acordo (ditongos abertos em paroxítonas) =====
    ("ideia", "DITONGO_PAROX"),
    ("heroico", "DITONGO_PAROX"),
    ("assembleia", "DITONGO_PAROX"),
    ("plateia", "DITONGO_PAROX"),
    ("boia", "DITONGO_PAROX"),
    ("jiboia", "DITONGO_PAROX"),
    ("joia", "DITONGO_PAROX"),
    ("europeia", "DITONGO_PAROX"),
    ("geleia", "DITONGO_PAROX"),
    ("paranoia", "DITONGO_PAROX"),
    ("colmeia", "DITONGO_PAROX"),

    # ===== SEM acento: oo / ee =====
    ("voo", "HIATO_DOBRADO"),
    ("enjoo", "HIATO_DOBRADO"),
    ("perdoo", "HIATO_DOBRADO"),
    ("leem", "HIATO_DOBRADO"),
    ("creem", "HIATO_DOBRADO"),
    ("deem", "HIATO_DOBRADO"),

    # ===== SEM acento: hiato i/u que não acentua =====
    ("ruim", "HIATO_IU_SEM"),
    ("juiz", "HIATO_IU_SEM"),
    ("raiz", "HIATO_IU_SEM"),
    ("rainha", "HIATO_IU_SEM"),
    ("bainha", "HIATO_IU_SEM"),
    ("tainha", "HIATO_IU_SEM"),
    ("moinho", "HIATO_IU_SEM"),
    ("cair", "HIATO_IU_SEM"),
    ("sair", "HIATO_IU_SEM"),
    ("ainda", "HIATO_IU_SEM"),
    ("contribuinte", "HIATO_IU_SEM"),

    # ===== SEM acento: i/u depois de ditongo =====
    ("feiura", "IU_POS_DITONGO"),
    ("baiuca", "IU_POS_DITONGO"),
    ("bocaiuva", "IU_POS_DITONGO"),

    # ===== SEM acento: diferenciais que caíram =====
    ("para", "DIFERENCIAL_EXTINTO"),
    ("pelo", "DIFERENCIAL_EXTINTO"),
    ("pera", "DIFERENCIAL_EXTINTO"),
    ("polo", "DIFERENCIAL_EXTINTO"),

    # ===== SEM acento: só til =====
    ("irmã", "TIL"),
    ("maçã", "TIL"),
    ("coração", "TIL"),
    ("limão", "TIL"),
    ("avião", "TIL"),
    ("pão", "TIL"),
]

# =====================================================================
# NÍVEL DIFÍCIL — sem acento vira outra palavra; só a frase decide
# (palavra, regra, frase, par)
# =====================================================================
PARES = [
    # ---- pode / pôde
    ("pôde", "DIFERENCIAL", "Ontem ele não ___ vir.", "pôde (passado) × pode (presente)"),
    ("pode", "DIFERENCIAL_SEM", "Hoje ele ___ sair mais cedo.", "pôde (passado) × pode (presente)"),
    # ---- tem / têm
    ("têm", "DIFERENCIAL", "Eles ___ dois cachorros.", "ele tem × eles têm"),
    ("tem", "DIFERENCIAL_SEM", "Ela ___ um gato.", "ele tem × eles têm"),
    # ---- vem / vêm / veem
    ("vêm", "DIFERENCIAL", "Eles ___ amanhã para a festa.", "ele vem × eles vêm (vir) × eles veem (ver)"),
    ("vem", "DIFERENCIAL_SEM", "Ele ___ amanhã para a festa.", "ele vem × eles vêm (vir) × eles veem (ver)"),
    ("veem", "HIATO_DOBRADO", "Eles ___ TV todo dia.", "ele vem × eles vêm (vir) × eles veem (ver)"),
    # ---- por / pôr
    ("pôr", "DIFERENCIAL", "Vou ___ a mesa para o jantar.", "pôr (verbo) × por (preposição)"),
    ("por", "MONO_ATONO", "Passei ___ aqui ontem.", "pôr (verbo) × por (preposição)"),
    # ---- sábia / sabia / sabiá
    ("sábia", "PAROX_TERM", "Minha avó é uma mulher muito ___.", "sábia (sabedoria) × sabia (verbo saber) × sabiá (pássaro)"),
    ("sabia", "PAROX_COMUM", "Ele ___ a resposta da questão.", "sábia (sabedoria) × sabia (verbo saber) × sabiá (pássaro)"),
    ("sabiá", "OXI_AEO", "O ___ cantou na janela.", "sábia (sabedoria) × sabia (verbo saber) × sabiá (pássaro)"),
    # ---- secretária / secretaria
    ("secretária", "PAROX_TERM", "A ___ atendeu o telefone.", "secretária (a pessoa) × secretaria (o setor)"),
    ("secretaria", "PAROX_COMUM", "A ___ da escola fecha às 17h.", "secretária (a pessoa) × secretaria (o setor)"),
    # ---- prática / pratica
    ("prática", "PROPAROX", "A ___ leva à perfeição.", "prática (substantivo) × pratica (verbo praticar)"),
    ("pratica", "PAROX_COMUM", "Ela ___ natação toda semana.", "prática (substantivo) × pratica (verbo praticar)"),
    # ---- dúvida / duvida
    ("dúvida", "PROPAROX", "Tenho uma ___ na questão 3.", "dúvida (substantivo) × duvida (verbo duvidar)"),
    ("duvida", "PAROX_COMUM", "Ele ___ de tudo que eu falo.", "dúvida (substantivo) × duvida (verbo duvidar)"),
    # ---- fábrica / fabrica
    ("fábrica", "PROPAROX", "Meu tio trabalha numa ___ de sapatos.", "fábrica (lugar) × fabrica (verbo fabricar)"),
    ("fabrica", "PAROX_COMUM", "Essa empresa ___ celulares.", "fábrica (lugar) × fabrica (verbo fabricar)"),
    # ---- número / numero
    ("número", "PROPAROX", "Qual é o seu ___ de telefone?", "número (substantivo) × numero (verbo numerar)"),
    ("numero", "PAROX_COMUM", "Eu ___ as páginas do caderno.", "número (substantivo) × numero (verbo numerar)"),
    # ---- público / publico
    ("público", "PROPAROX", "O ___ aplaudiu de pé.", "público (plateia) × publico (verbo publicar)"),
    ("publico", "PAROX_COMUM", "Eu ___ um vídeo novo toda semana.", "público (plateia) × publico (verbo publicar)"),
    # ---- cálculo / calculo
    ("cálculo", "PROPAROX", "Fiz um ___ difícil na prova.", "cálculo (substantivo) × calculo (verbo calcular)"),
    ("calculo", "PAROX_COMUM", "Eu ___ tudo de cabeça.", "cálculo (substantivo) × calculo (verbo calcular)"),
    # ---- está / esta
    ("está", "OXI_AEO", "Ele ___ cansado hoje.", "está (verbo estar) × esta (essa aqui)"),
    ("esta", "PAROX_COMUM", "___ casa é minha.", "está (verbo estar) × esta (essa aqui)"),
    # ---- é / e
    ("é", "MONO_AEO", "O céu ___ azul.", "é (verbo ser) × e (ligação: arroz e feijão)"),
    ("e", "MONO_ATONO", "Comi arroz ___ feijão.", "é (verbo ser) × e (ligação: arroz e feijão)"),
    # ---- dá / da
    ("dá", "MONO_AEO", "Ele ___ comida ao cachorro.", "dá (verbo dar) × da (de + a)"),
    ("da", "MONO_ATONO", "Esse livro é ___ Maria.", "dá (verbo dar) × da (de + a)"),
    # ---- nó / no
    ("nó", "MONO_AEO", "Dei um ___ no cadarço.", "nó (laço) × no (em + o)"),
    ("no", "MONO_ATONO", "Deixei o livro ___ armário.", "nó (laço) × no (em + o)"),
    # ---- nós / nos
    ("nós", "MONO_AEO", "___ vamos à praia amanhã.", "nós (a gente) × nos (pronome: ele nos chamou)"),
    ("nos", "MONO_ATONO", "O professor ___ chamou.", "nós (a gente) × nos (pronome: ele nos chamou)"),
    # ---- país / pais
    ("país", "HIATO_IU", "O Brasil é um ___ enorme.", "país (nação, pa-ís) × pais (pai e mãe, uma sílaba)"),
    ("pais", "DITONGO_SEM", "Meus ___ viajaram no fim de semana.", "país (nação, pa-ís) × pais (pai e mãe, uma sílaba)"),
    # ---- bebê / bebe
    ("bebê", "OXI_AEO", "O ___ está dormindo.", "bebê (criança) × bebe (verbo beber)"),
    ("bebe", "PAROX_COMUM", "Ele ___ muita água.", "bebê (criança) × bebe (verbo beber)"),
    # ---- babá / baba
    ("babá", "OXI_AEO", "A ___ cuida das crianças.", "babá (quem cuida) × baba (verbo babar)"),
    ("baba", "PAROX_COMUM", "O cachorro ___ quando vê comida.", "babá (quem cuida) × baba (verbo babar)"),
    # ---- camelô / camelo
    ("camelô", "OXI_AEO", "Comprei um fone no ___ da esquina.", "camelô (vendedor) × camelo (animal)"),
    ("camelo", "PAROX_COMUM", "O ___ atravessou o deserto.", "camelô (vendedor) × camelo (animal)"),
    # ---- revólver / revolver
    ("revólver", "PAROX_TERM", "O policial guardou o ___.", "revólver (arma) × revolver (verbo: mexer, remexer)"),
    ("revolver", "OXI_OUTRAS", "É preciso ___ a terra antes de plantar.", "revólver (arma) × revolver (verbo: mexer, remexer)"),
    # ---- sem par direto, mas a frase decide
    ("música", "PROPAROX", "Gosto de ouvir ___ alta.", "música (som) × musica (verbo musicar, raro)"),
    ("médico", "PROPAROX", "Fui ao ___ ontem.", "médico (profissional) × medico (verbo medicar)"),
    ("último", "PROPAROX", "Fui o ___ a chegar.", "último (o do final) × ultimo (verbo ultimar, raro)"),
    ("lá", "MONO_AEO", "Ele mora ___ longe.", "lá (lugar) × la (pronome: vou chamá-la)"),
]
