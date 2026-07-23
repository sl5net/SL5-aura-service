# config/maps/plugins/sikulix/pt-BR/FUZZY_MAP_pre.py
import os
import re
from pathlib import Path

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

CONFIG_DIR = Path(__file__).parent
sikulix_windows = ['sikulixide', 'SikuliX', 'Sikuli', 'oculixide', 'OculiX']

FUZZY_MAP_pre = [
    #################################################
    # 2. ative esta regra (atrás da primeira regra que você deseja otimizar)

    #################################################

    # EXAMPLE: clique duplo
    ('doubleClick("image.png")', r'^\s*(clique\s*duplo|duplo\s*clique|dois\s*cliques|double\s*click)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: botão direito / clique direito
    ('rightClick("image.png")', r'^\s*(clique\s*direito|botão\s*direito|botao\s*direito|clica\s*direito|right\s*click)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: clique / clica
    ('click("image.png")', r'^\s*(clique|clica|clicar|clic|click|pressiona|batida)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: espere desaparecer (wait vanish)
    ('waitVanish("image.png", 10)', r'^\s*(espere\s*desaparecer|esperar\s*sumir|aguarde\s*sair|espere\s*limpar|wait\s*vanish)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: espera / aguarda (wait)
    ('wait("image.png", 10)', r'^\s*(espera|esperar|aguarda|aguardar|espere|pausa|pare|aguarde|wait)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: encontre todos (find all)
    ('for m in findAll("image.png"):', r'^\s*(encontre\s*todos|encontrar\s*todos|buscar\s*todos|acha\s*todos|localizar\s*todos|find\s*all)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: encontre / acha (find)
    ('find("image.png")', r'^\s*(encontre|encontrar|acha|achar|busque|buscar|localiza|procura|find)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: existe
    ('if exists("image.png"):', r'^\s*(existe|existir|está\s*lá|está\s*na\s*tela|tem|aparece|exists?)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: escreve / digita (type)
    ('type("text")', r'^\s*(escreve|escrever|digita|digitar|digite|tecle|teclado|type|write)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: colar (paste)
    ('paste("text")', r'^\s*(cola|colar|cole|inserir|paste)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: passar o mouse (hover)
    ('hover("image.png")', r'^\s*(passar\s*o\s*mouse|sobrepor|posiciona|hover)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: arrastar e soltar (drag drop)
    ('dragDrop("source.png", "target.png")', r'^\s*(arrastar\s*e\s*soltar|arrasta\s*e\s*solta|puxar|drag\s*drop)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: rolar (scroll)
    ('wheel("image.png", WHEEL_DOWN, 3)', r'^\s*(rola|rolar|descer|subir|girar\s*roda|scroll|wheel)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: dormir (sleep)
    ('sleep(1)', r'^\s*(dorme|dormir|espera\s*um\s*segundo|descanso|sleep)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),

    # EXAMPLE: capturar tela (capture)
    ('capture(SCREEN)', r'^\s*(capturar|print|captura|foto\s*da\s*tela|screenshot)\s*$', 85, {
        'command_flags': re.IGNORECASE, 'only_in_windows': sikulix_windows,
    }),
]
