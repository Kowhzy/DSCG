"""Génère graphiques (04_graphiques) et rapports PDF (05_rapports) pour UE2, UE3, UE5."""
import os, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from stats import compute, write, YEARS, techniques, sensitivity, SCENARIOS
import csv as _csv
from referentiel import RUBRIQUES, JURY, COURS, COURS_NOTE, BO_REF, PARTIES_NOTE
from contenu import TITRES, EPREUVE, SYNTHESE, SURPRISES, TROUS, ANNALES, METHODE_COMMUNE

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image,
                                PageBreak, KeepTogether, CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
G = os.path.join(BASE, '04_graphiques'); os.makedirs(G, exist_ok=True)
R = os.path.join(BASE, '05_rapports'); os.makedirs(R, exist_ok=True)
DATE = datetime.date(2026, 9, 24).strftime('%d/%m/%Y')

# --- palette (référence dataviz, mode clair) ---
INK, INK2, MUTED, GRID, SURF = '#0b0b0b', '#52514e', '#8a8984', '#e4e3df', '#fcfcfb'
CAT = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#4a3aa7', '#e34948']
SEQ = {100: '#cde2fb', 250: '#86b6ef', 350: '#5598e7', 450: '#2a78d6', 550: '#1c5cab', 650: '#104281'}
CATCOL = {'PRIORITÉ MAXIMALE': SEQ[650], 'PRIORITÉ TRÈS ÉLEVÉE': SEQ[550], 'PRIORITÉ ÉLEVÉE': SEQ[450],
          'À MAÎTRISER': SEQ[350], 'COMPLÉMENT': SEQ[250]}
CATS = list(CATCOL)
REUSSITE = {  # taux de réussite après délibération — rapports du jury 2020 (p.4), 2021 (p.4), 2024 et 2025 (p.18-19)
 'UE2': [31.43, 39.69, 23.86, 52.49, 14.75, 30.99, 43.00],
 'UE3': [40.01, 36.26, 38.49, 37.49, 40.47, 50.14, 17.28],
 'UE5': [66.87, 67.84, 55.10, 60.46, 57.27, 57.85, 38.87]}
RY = list(range(2019, 2026))
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.edgecolor': GRID, 'axes.labelcolor': INK2,
                     'xtick.color': INK2, 'ytick.color': INK2, 'axes.titlecolor': INK, 'figure.facecolor': 'white',
                     'axes.facecolor': 'white'})

def short(t, n=46):
    return t if len(t) <= n else t[:n - 1] + '…'

def charts(ue, res, rows):
    out = {}
    order = sorted(res, key=lambda r: [int(x) for x in r['code'].split('.')])
    # 1. heatmap rubrique × année
    fig, ax = plt.subplots(figsize=(7.2, 0.28 * len(order) + 1.2))
    for i, r in enumerate(order):
        for j, y in enumerate(YEARS):
            v, a = r['years'][y], r['yearsA'][y]
            c = SEQ[550] if v >= 1 else SEQ[350] if v > 0 else SEQ[100] if a > 0 else 'white'
            ax.add_patch(plt.Rectangle((j + .06, i + .08), .88, .84, color=c, lw=0))
            if c == 'white':
                ax.add_patch(plt.Rectangle((j + .06, i + .08), .88, .84, fill=False, ec=GRID, lw=.6))
    ax.set_xlim(0, len(YEARS)); ax.set_ylim(len(order), 0)
    ax.set_xticks([j + .5 for j in range(len(YEARS))]); ax.set_xticklabels(YEARS)
    ax.set_yticks([i + .5 for i in range(len(order))])
    ax.set_yticklabels([f"{r['code']}  {short(r['titre'], 40)}" for r in order], fontsize=7)
    ax.axvline(4, color=INK2, lw=1, ls=(0, (3, 2)))
    ax.text(4.05, -0.25, 'programme 2019 →', fontsize=7, color=INK2, va='bottom')
    ax.text(3.95, -0.25, '← ancien programme', fontsize=7, color=MUTED, va='bottom', ha='right')
    ax.tick_params(length=0); [s.set_visible(False) for s in ax.spines.values()]
    hd = [Patch(color=SEQ[550], label='principal')] + [Patch(color=SEQ[100], label='secondaire / toile de fond')]
    ax.legend(handles=hd, loc='upper center',
              bbox_to_anchor=(.45, -0.035 * 20 / len(order)), ncol=3, frameon=False, fontsize=7)
    fig.tight_layout(); p = os.path.join(G, f'{ue}_heatmap.png'); fig.savefig(p, dpi=200); plt.close(fig); out['heatmap'] = p
    # 2. fréquence historique vs programme actuel
    srt = sorted(res, key=lambda r: -r['ipr'])
    fig, ax = plt.subplots(figsize=(7.2, 0.26 * len(srt) + 1.0))
    ys = range(len(srt)); h = .36
    ax.barh([y - h / 2 - .02 for y in ys], [r['f10'] * 100 for r in srt], height=h, color=CAT[0], label='2016-2025 (10 sessions)')
    ax.barh([y + h / 2 + .02 for y in ys], [r['fcur'] * 100 for r in srt], height=h, color=CAT[1], label='2020-2025 (programme actuel, 6 sessions)')
    ax.set_yticks(list(ys)); ax.set_yticklabels([f"{r['code']}  {short(r['titre'], 38)}" for r in srt], fontsize=7)
    ax.invert_yaxis(); ax.set_xlim(0, 105); ax.set_xlabel('% des sessions où la rubrique est mobilisée en principal')
    ax.grid(axis='x', color=GRID, lw=.6); ax.set_axisbelow(True); [ax.spines[s].set_visible(False) for s in ('top', 'right')]
    ax.legend(loc='lower right', frameon=False, fontsize=7)
    fig.tight_layout(); p = os.path.join(G, f'{ue}_frequences.png'); fig.savefig(p, dpi=200); plt.close(fig); out['freq'] = p
    # 3. IPR
    fig, ax = plt.subplots(figsize=(7.2, 0.25 * len(srt) + 1.0))
    ax.barh(list(ys), [r['ipr'] for r in srt], color=[CATCOL[r['cat']] for r in srt], height=.68)
    for y, r in zip(ys, srt):
        ax.text(r['ipr'] + 1, y, f"{r['ipr']:.1f}".replace('.', ','), va='center', fontsize=7, color=INK2)
    ax.set_yticks(list(ys)); ax.set_yticklabels([f"{r['code']}  {short(r['titre'], 38)}" for r in srt], fontsize=7)
    ax.invert_yaxis(); ax.set_xlim(0, 100); ax.set_xlabel('Indice de priorité de révision (0-100) — ce n\'est pas une probabilité')
    for t in (20, 32, 45, 60):
        ax.axvline(t, color=GRID, lw=.8, ls=(0, (2, 2)))
    [ax.spines[s].set_visible(False) for s in ('top', 'right')]
    ax.legend(handles=[Patch(color=CATCOL[c], label=c.replace('PRIORITÉ ', '').capitalize()) for c in CATS],
              loc='lower right', frameon=False, fontsize=7, title='Catégorie', title_fontsize=7)
    fig.tight_layout(); p = os.path.join(G, f'{ue}_ipr.png'); fig.savefig(p, dpi=200); plt.close(fig); out['ipr'] = p
    # 4. poids des parties du programme par session (programme actuel + ancien)
    parties = []
    for _, pa, *_ in RUBRIQUES[ue]:
        if pa not in parties: parties.append(pa)
    code2p = {c: pa for c, pa, *_ in RUBRIQUES[ue]}
    import collections
    share = collections.defaultdict(lambda: collections.defaultdict(float))
    for r in rows:
        for c in r['P']:
            share[r['y']][code2p[c]] += 100 * r['w_subject'] * r['share'] / len(r['P'])
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    bottom = [0] * len(YEARS)
    for k, pa in enumerate(parties):
        vals = [share[y][pa] for y in YEARS]
        ax.bar(range(len(YEARS)), vals, bottom=bottom, color=CAT[k], width=.7, label=short(pa, 42), edgecolor='white', linewidth=1.5)
        bottom = [b + v for b, v in zip(bottom, vals)]
    ax.set_xticks(range(len(YEARS))); ax.set_xticklabels(YEARS); ax.set_ylim(0, 100)
    ax.set_ylabel('% du barème (réparti entre rubriques principales)')
    ax.axvline(3.5, color=INK2, lw=1, ls=(0, (3, 2)))
    ax.grid(axis='y', color=GRID, lw=.6); ax.set_axisbelow(True); [ax.spines[s].set_visible(False) for s in ('top', 'right')]
    ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0), frameon=False, fontsize=7)
    fig.tight_layout(); p = os.path.join(G, f'{ue}_parties.png'); fig.savefig(p, dpi=200); plt.close(fig); out['parties'] = p
    # 5. taux de réussite (UE en couleur, autres UE en contexte gris)
    fig, ax = plt.subplots(figsize=(7.2, 2.8))
    labs = sorted([(REUSSITE[o][-1], o) for o in ('UE2', 'UE3', 'UE5')])
    ypos = {}; prev = -99
    for v, o in labs:
        y = max(v, prev + 6); ypos[o] = y; prev = y
    for o in ('UE2', 'UE3', 'UE5'):
        if o == ue: continue
        ax.plot(RY, REUSSITE[o], color='#bdbcb6', lw=1.2)
        ax.text(2025.15, ypos[o], o, fontsize=7, color=MUTED, va='center')
    ax.plot(RY, REUSSITE[ue], color=CAT[0], lw=2, marker='o', ms=5)
    for x, v in zip(RY, REUSSITE[ue]):
        ax.text(x, v + 2.5, f"{v:.1f}".replace('.', ','), ha='center', fontsize=7, color=INK)
    ax.text(2025.15, ypos[ue], ue, fontsize=8, color=INK, va='center', weight='bold')
    ax.set_ylim(0, 80); ax.set_xlim(2018.7, 2025.75); ax.set_ylabel('taux de réussite (%)')
    ax.grid(axis='y', color=GRID, lw=.6); ax.set_axisbelow(True); [ax.spines[s].set_visible(False) for s in ('top', 'right')]
    fig.tight_layout(); p = os.path.join(G, f'{ue}_reussite.png'); fig.savefig(p, dpi=200); plt.close(fig); out['reussite'] = p
    return out

# ---------------- PDF ----------------
pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('DV', normal='DV', bold='DVB', italic='DV', boldItalic='DVB')
ACC = colors.HexColor('#1c5cab'); LIGHT = colors.HexColor('#eef4fc'); LINE = colors.HexColor('#d7d6d1')
st = {
 'title': ParagraphStyle('title', fontName='DVB', fontSize=19, leading=24, textColor=colors.HexColor(INK), spaceAfter=10),
 'sub': ParagraphStyle('sub', fontName='DV', fontSize=10, leading=14, textColor=colors.HexColor(INK2)),
 'h1': ParagraphStyle('h1', fontName='DVB', fontSize=14, leading=18, textColor=ACC, spaceBefore=4, spaceAfter=8),
 'h2': ParagraphStyle('h2', fontName='DVB', fontSize=11, leading=14, textColor=colors.HexColor(INK), spaceBefore=8, spaceAfter=4),
 'h2n': ParagraphStyle('h2n', fontName='DVB', fontSize=11, leading=14, spaceBefore=8, spaceAfter=4),
 'h3': ParagraphStyle('h3', fontName='DVB', fontSize=9.5, leading=12, textColor=ACC, spaceBefore=6, spaceAfter=2),
 'p': ParagraphStyle('p', fontName='DV', fontSize=8.6, leading=11.8, textColor=colors.HexColor(INK), spaceAfter=4),
 'b': ParagraphStyle('b', fontName='DV', fontSize=8.6, leading=11.8, leftIndent=10, bulletIndent=2, spaceAfter=2.5),
 'small': ParagraphStyle('small', fontName='DV', fontSize=7, leading=9, textColor=colors.HexColor(INK2)),
 'cell': ParagraphStyle('cell', fontName='DV', fontSize=6.8, leading=8.4),
 'cellb': ParagraphStyle('cellb', fontName='DVB', fontSize=6.8, leading=8.4),
 'hdr': ParagraphStyle('hdr', fontName='DVB', fontSize=6.8, leading=8.4, textColor=colors.white),
 'toc1': ParagraphStyle('toc1', fontName='DV', fontSize=9.5, leading=14, leftIndent=0),
 'toc2': ParagraphStyle('toc2', fontName='DV', fontSize=8, leading=11, leftIndent=14, textColor=colors.HexColor(INK2)),
 'box': ParagraphStyle('box', fontName='DV', fontSize=8.4, leading=11.4),
}

class Doc(BaseDocTemplate):
    def __init__(self, fn, ue, **kw):
        super().__init__(fn, pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm, topMargin=18 * mm, bottomMargin=16 * mm,
                         title=TITRES[ue], author='Étude DSCG 2026 — Sacha', **kw)
        self.ue = ue
        fr = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='f')
        self.addPageTemplates([PageTemplate('p', [fr], onPage=self.deco)])
    def deco(self, c, d):
        c.saveState(); c.setFont('DV', 7); c.setFillColor(colors.HexColor(INK2))
        if d.page > 1:
            c.drawString(16 * mm, A4[1] - 11 * mm, TITRES[self.ue].split(' — Analyse')[0])
            c.drawRightString(A4[0] - 16 * mm, A4[1] - 11 * mm, f'mis à jour le {DATE}')
            c.setStrokeColor(LINE); c.line(16 * mm, A4[1] - 12.5 * mm, A4[0] - 16 * mm, A4[1] - 12.5 * mm)
        c.drawRightString(A4[0] - 16 * mm, 9 * mm, f'page {d.page}')
        c.drawString(16 * mm, 9 * mm, "Indice de priorité ≠ probabilité de tomber · données : DSCG_2026_ANALYSE/02_data")
        c.restoreState()
    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and f.style.name in ('h1', 'h2'):
            lvl = 0 if f.style.name == 'h1' else 1
            txt = f.getPlainText(); key = f'k{id(f)}'
            self.canv.bookmarkPage(key); self.canv.addOutlineEntry(txt, key, level=lvl, closed=lvl > 0)
            self.notify('TOCEntry', (lvl, txt, self.page, key))

def P(t, s='p'): return Paragraph(t, st[s])
def B(t): return Paragraph(t, st['b'], bulletText='•')
def tbl(data, widths, head=True, zebra=True, fs=None):
    rows = []
    for i, r in enumerate(data):
        rows.append([c if not isinstance(c, str) else Paragraph(c, st['hdr'] if (head and i == 0) else st['cell']) for c in r])
    t = Table(rows, colWidths=widths, repeatRows=1 if head else 0)
    sty = [('GRID', (0, 0), (-1, -1), .3, LINE), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
           ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3),
           ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]
    if head: sty.append(('BACKGROUND', (0, 0), (-1, 0), ACC))
    if zebra:
        for i in range(1 if head else 0, len(rows)):
            if i % 2 == 0: sty.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f6f6f4')))
    t.setStyle(TableStyle(sty)); return t
def img(p, w=178 * mm):
    from PIL import Image as PI
    W, H = PI.open(p).size
    return Image(p, width=w, height=w * H / W)
def box(txt):
    t = Table([[Paragraph(txt, st['box'])]], colWidths=[178 * mm])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), LIGHT), ('BOX', (0, 0), (-1, -1), .6, ACC),
                           ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                           ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]))
    return t
def pct(x): return f"{x * 100:.0f} %"
def fr(x, d=1): return f"{x:.{d}f}".replace('.', ',')

def reason(r):
    lab = {'f_hist': 'fréquence 2016-2025', 'f_cur': 'fréquence depuis 2020', 'f_rec': 'présence récente (2023-2025)',
           'poids': 'poids dans le barème', 'jury': 'citations du jury', 'diff': 'difficultés signalées par le jury',
           'transv': 'transversalité', 'bo': 'volume horaire au programme', 'gap': 'absence récente (zone à ne pas négliger)'}
    from stats import W
    contrib = sorted(((W[k] * v, k) for k, v in r['comp'].items()), reverse=True)
    top = [f"{lab[k]} ({fr(c, 1)} pts)" for c, k in contrib[:3] if c > 0]
    s = "Contributions principales à l'IPR : " + ', '.join(top) + '.'
    if r.get('regle'): s += ' Catégorie ' + r['regle'] + '.'
    return s

def attendus(ue):
    p = os.path.join(BASE, '02_data', f'{ue}_attendus_corriges.csv')
    return list(_csv.DictReader(open(p, encoding='utf-8'), delimiter=';'))

def attendus_rubrique(ue, r, rows, att, n=3):
    keys = {(x['annee'], x['dossier']) for x in rows if r['code'] in x['P'] and x['y'] >= 2020}
    out = [a for a in att if (a['annee'], a['dossier']) in keys or any((a['annee'], d) in keys for d in a['dossier'].split('-'))]
    out = [a for a in out if a['source'] != 'Non vérifié']
    out.sort(key=lambda a: a['annee'], reverse=True)
    return out[:n]

def annales_rubrique(ue, r, rows):
    items = []
    for row in sorted(rows, key=lambda x: x['annee'], reverse=True):
        if r['code'] in row['P']:
            tag = ' (sujet annulé, entraînement)' if row['w_subject'] == 0 else '' if row['y'] >= 2020 else ' (ancien programme)'
            items.append(f"<b>{row['annee']} D{row['dossier']}</b>{tag} — {row['intitule']}")
    return items[:5]

def build(ue):
    rows, res = compute(ue); write(ue, rows, res)
    tech = techniques(ue); sens = sensitivity(ue, res); att = attendus(ue)
    sens_by = {x['code']: x for x in sens}
    ch = charts(ue, res, rows)
    srt = sorted(res, key=lambda r: -r['ipr'])
    fn = os.path.join(R, f'DSCG_2026_{ue}.pdf')
    doc = Doc(fn, ue)
    S = []
    # --- couverture + sommaire
    S += [Spacer(1, 30 * mm), P(TITRES[ue], 'title'),
          P(f"Étude documentaire et statistique — sessions 2016 à 2025 — préparée pour Sacha, le {DATE}.", 'sub'), Spacer(1, 6 * mm),
          box("<b>Question directrice.</b> Compte tenu du programme officiel, des attentes du jury, des annales et de tes ressources, "
              "quelles compétences maîtriser en priorité pour être prêt au mieux en 2026 ? <br/><b>Avertissement.</b> Cet indice hiérarchise un effort de révision : "
              "il ne prédit pas le sujet. Le jury le rappelle : « aucun point du programme du DSCG ne peut être considéré comme mineur » [Rapports du jury 2020, 2021, 2022, 2024, 2025]."),
          Spacer(1, 4 * mm), P(f"<b>Épreuve.</b> {EPREUVE[ue]}", 'p'), Spacer(1, 6 * mm), P('Sommaire', 'h2n')]
    toc = TableOfContents(); toc.levelStyles = [st['toc1'], st['toc2']]; toc.dotsMinLevel = 0
    S += [toc, PageBreak()]
    # --- 1. synthèse
    S.append(P('1. Synthèse exécutive', 'h1'))
    S.append(P('Les constats clés', 'h2'))
    S += [B(t) for t in SYNTHESE[ue]]
    S.append(P('Le top 10 des priorités 2026 (indice de priorité de révision)', 'h2'))
    data = [['#', 'Rubrique officielle', 'Catégorie', 'IPR', 'Sessions 2016-25', 'Depuis 2020', '3 dernières', 'Dernière']]
    for i, r in enumerate(srt[:10], 1):
        data.append([str(i), f"<b>{r['code']}</b> {r['titre']}", r['cat'].replace('PRIORITÉ ', '').capitalize(), fr(r['ipr'], 1),
                     f"{fr(r['sessions_10'])}/10", f"{fr(r['sessions_cur'])}/6", pct(r['f3']), str(r['last'] or '—')])
    S.append(tbl(data, [7 * mm, 68 * mm, 24 * mm, 11 * mm, 19 * mm, 17 * mm, 16 * mm, 16 * mm]))
    nt = -(-len(res) // 3); rob = [r['code'] for r in srt[:10] if sens_by[r['code']]['top_tiers'] == len(SCENARIOS)]
    S.append(P(f"<b>Robustesse.</b> Sous {len(SCENARIOS)} jeux de pondérations différents, les rubriques {', '.join(rob) or 'aucune'} restent toujours dans le premier tiers du classement (rang ≤ {nt}) : ces priorités ne dépendent pas du choix des pondérations. Détail en section 5.5."))
    alert = [a for a in att if 'ALERTE' in a['pieges_et_vigilance'] or 'ALERTE' in a['attendus_du_corrige']]
    if alert:
        S.append(P(f"<b>Corrigés à lire avec prudence.</b> {len(alert)} point(s) des éléments de corrigé semblent erronés ou dépassés : " + ' ; '.join(f"{a['annee']} D{a['dossier']} ({a['question'][:45]})" for a in alert) + ". Détail en section 10.3."))
    S.append(P('Surprises et points d\'attention', 'h2'))
    S += [B(t) for t in SURPRISES[ue]]
    S.append(P('Zones à ne pas négliger (faible fréquence mais toujours au programme)', 'h2'))
    S.append(P(', '.join(f"<b>{c}</b>" for c in TROUS[ue]) + " — détail en section 7.3. Le jury rappelle que ce n'est pas parce qu'un point n'a pas fait l'objet d'un sujet qu'il ne pourra pas en faire l'objet [Rapport du jury 2025, p. 21]."))
    S.append(P('Principales remarques du jury', 'h2'))
    S += [B(f"[{a}, {pg}] {o}") for (a, pg, o, rub, pb, cons) in JURY[ue] if a >= 2024 and pb][:4]
    S.append(P('Ton point de départ (statut déclaré dans Notion)', 'h2'))
    top = srt[:10]
    faibles = [f"{r['code']}" for r in top if COURS[ue].get(r['code'], ('', ''))[1].startswith('I')]
    S.append(P(("Parmi les 10 priorités, aucune preuve de travail n'est enregistrée pour : <b>" + ', '.join(faibles) + "</b> (statut « I » = inconnu). "
                if faibles else "Toutes les priorités du top 10 ont au moins une trace de travail dans Notion. ")
               + "Commence par ces rubriques. Le statut « A » (travail guidé) ne vaut pas maîtrise ; vise une restitution sans aide."))
    S.append(P('Annales à refaire en priorité', 'h2'))
    S += [B(f"<b>{a}</b> — {t}") for a, t in ANNALES[ue][:4]]
    S.append(CondPageBreak(150 * mm))
    # --- 2. méthodologie
    S.append(P('2. Méthodologie', 'h1'))
    for t, x in METHODE_COMMUNE:
        S.append(P(f"<b>{t}.</b> {x}"))
    S.append(P('Hiérarchie des sources utilisées', 'h2'))
    S += [B("Niveau 1 : rapports du jury DSCG 2020, 2021, 2022, 2024 et 2025 (lus intégralement) ; sujets des sessions 2016-2025 (PDF officiels ou copies FicheBEN des sujets officiels, lus question par question) ; programme de l'arrêté du 13 février 2019 (texte relu dans sa reproduction en tête des manuels Dunod UE2/UE3 et dans le document « Programme MSI 19-20 » pour l'UE5) ; éléments indicatifs de corrigé 2020-2025 (lus question par question, pour les 3 UE)."),
          B("Niveau 2 (contrôle) : Compta Online (articles « Pronostic DSCG … thèmes récurrents », « réforme ») via les extraits de moteur de recherche, le site étant inaccessible ; tes notes Drive (UE5-01 à UE5-07) ; ta base Notion (héritée d'un modèle, donc utilisée comme index et non comme preuve)."),
          B("Contrôle croisé : les structures des sujets 2020, 2021, 2022, 2024 et 2025 ont été vérifiées contre la description qu'en donne le rapport du jury correspondant (concordance constatée).")]
    S.append(CondPageBreak(170 * mm))
    # --- 3. programme
    S.append(P('3. Programme officiel applicable', 'h1'))
    S.append(P(f"<b>Référence.</b> {BO_REF[ue]}. Programme applicable aux sessions 2020 à 2026 ; remplacé à partir de la session 2027 (arrêté du 4 août 2025, BO ESR du 28 août 2025). {PARTIES_NOTE[ue]}"))
    S.append(P("Arborescence : partie (volume horaire officiel) → rubrique officielle → notions et contenus (résumé fidèle du texte officiel). Toutes les rubriques restent au programme 2026."))
    data = [['Partie', 'Rubrique', 'Notions et contenus officiels (résumé)']]
    for c, pa, t, n, b in RUBRIQUES[ue]:
        data.append([pa, f"<b>{c}</b> {t}", n])
    S.append(tbl(data, [40 * mm, 55 * mm, 83 * mm]))
    S.append(CondPageBreak(170 * mm))
    # --- 4. historique
    S.append(P('4. Historique des annales 2016-2025', 'h1'))
    S.append(P("Carte thermique : pour chaque rubrique officielle, présence en principal (bleu foncé) ou en toile de fond (bleu clair) dans le sujet de chaque session. La ligne pointillée marque l'entrée en vigueur du programme 2019 (session 2020)."))
    S.append(img(ch['heatmap']))
    S.append(PageBreak())
    S.append(P('Tableau complet des dossiers', 'h2'))
    data = [['Session', 'D.', 'Intitulé', 'Pts', 'Questions (résumé)', 'Rubr. P', 'Rubr. s', 'Nature']]
    for r in sorted(rows, key=lambda x: (x['annee'], int(x['dossier'])), reverse=False)[::-1]:
        pts = f"{r['points']}/{r['total_points']}" if r['points'] else 'n.v.'
        data.append([r['annee'], r['dossier'], r['intitule'], pts, r['questions_resume'], ' '.join(r['P']), ' '.join(r['S']), r['nature']])
    S.append(tbl(data, [13 * mm, 6 * mm, 31 * mm, 12 * mm, 68 * mm, 17 * mm, 13 * mm, 18 * mm]))
    S.append(P("n.v. = non vérifié. Points : barème indiqué sur le sujet. Source de chaque ligne : colonne « source » de 02_data/" + ue + "_dossiers.csv.", 'small'))
    S.append(CondPageBreak(170 * mm))
    # --- 5. stats
    S.append(P('5. Analyse statistique', 'h1'))
    S.append(P('5.1 Fréquences : historique vs programme actuel', 'h2'))
    S.append(img(ch['freq']))
    S.append(P('5.2 Tableau statistique par rubrique', 'h2'))
    data = [['Rubrique', 'Sess. /10', 'Fréq. 10', 'Fréq. 2020-25', 'Fréq. 5 dern.', 'Fréq. 3 dern.', 'Dernière (écart)', 'Poids quand présent', 'Nb doss.', 'Transv.']]
    for r in sorted(res, key=lambda r: [int(x) for x in r['code'].split('.')]):
        data.append([f"<b>{r['code']}</b> {short(r['titre'], 34)}", fr(r['sessions_10']), pct(r['f10']), pct(r['fcur']), pct(r['f5']), pct(r['f3']),
                     f"{r['last']} ({r['since']} an{'s' if (r['since'] or 0) > 1 else ''})" if r['last'] else 'jamais', pct(r['w_when']) if r['w_when'] else '—',
                     str(r['n_dossiers']), str(r['transv'])])
    S.append(tbl(data, [52 * mm, 12 * mm, 13 * mm, 17 * mm, 15 * mm, 15 * mm, 19 * mm, 16 * mm, 10 * mm, 9 * mm]))
    S.append(P("Poids quand présent = part moyenne du barème (2020-2025) attribuée à la rubrique les années où elle est interrogée. Transv. = nombre d'autres rubriques mobilisées dans les mêmes dossiers depuis 2020.", 'small'))
    S.append(CondPageBreak(90 * mm))
    S.append(P('5.3 Poids des parties du programme dans chaque sujet', 'h2'))
    S.append(img(ch['parties'], 170 * mm))
    S.append(CondPageBreak(80 * mm))
    S.append(P('5.4 Taux de réussite (après délibération)', 'h2'))
    S.append(img(ch['reussite'], 165 * mm))
    S.append(P("Sources : rapports du jury 2020 (p. 4), 2021 (p. 4), 2024 et 2025 (p. 18-19). Les autres UE sont affichées en gris pour contexte.", 'small'))
    S.append(CondPageBreak(120 * mm))
    S.append(P('5.5 Robustesse du classement (test de sensibilité)', 'h2'))
    S.append(P(f"L'IPR dépend de pondérations choisies par l'analyste. Pour vérifier que le classement n'en est pas un artefact, il a été recalculé sous {len(SCENARIOS)} scénarios : "
               + ' ; '.join(f"<i>{k}</i>" for k in SCENARIOS) + ". Colonne « 1er tiers » : nombre de scénarios où la rubrique est classée parmi les "
               + f"{-(-len(res) // 3)} premières."))
    data = [['Rubrique', 'IPR', 'Rang (référence)', 'Rang min', 'Rang max', '1er tiers', 'Lecture']]
    for x in sens:
        lec = ('priorité robuste' if x['top_tiers'] == x['n_scen'] else 'dépend des pondérations' if x['top_tiers'] > 0 else
               'jamais prioritaire' if x['rmin'] > 2 * -(-len(res) // 3) else 'rang intermédiaire stable' if x['rmax'] - x['rmin'] <= 3 else 'rang variable')
        data.append([f"<b>{x['code']}</b> {short(x['titre'], 40)}", fr(x['ipr'], 1), str(x['rank_ref']), str(x['rmin']), str(x['rmax']), f"{x['top_tiers']}/{x['n_scen']}", lec])
    S.append(tbl(data, [70 * mm, 12 * mm, 20 * mm, 15 * mm, 15 * mm, 15 * mm, 31 * mm]))
    S.append(P("Détail par scénario : 03_analyses/" + ue + "_sensibilite.csv.", 'small'))
    S.append(CondPageBreak(120 * mm))
    S.append(P('5.6 Les techniques les plus mobilisées', 'h2'))
    S.append(P("Les rubriques du programme sont larges. Ce tableau compte les techniques et outils précis demandés dans les dossiers (une fois par session), indépendamment de la rubrique. Il indique ce qu'il faut savoir faire, pas seulement ce qu'il faut connaître."))
    data = [['Technique / outil', 'Sessions 2016-25', 'Depuis 2020', '2023-2025', 'Dernière', 'Dossiers (récents d\'abord)']]
    for x in tech[:24]:
        data.append([x['label'], fr(x['s10'], 1).replace(',0', ''), fr(x['scur'], 1).replace(',0', ''), fr(x['s3'], 1).replace(',0', ''), str(x['last']),
                     ', '.join(sorted(x['dossiers'], reverse=True)[:6]) + (' …' if len(x['dossiers']) > 6 else '')])
    S.append(tbl(data, [56 * mm, 18 * mm, 16 * mm, 15 * mm, 15 * mm, 58 * mm]))
    S.append(P(f"Liste complète ({len(tech)} techniques) : 03_analyses/{ue}_techniques.csv." + (" Le sujet 2022-S1 (annulé) est exclu des comptages." if ue == 'UE2' else ''), 'small'))
    S.append(CondPageBreak(170 * mm))
    # --- 6. jury
    S.append(P('6. Analyse des rapports du jury', 'h1'))
    S.append(P("Rapports lus : sessions 2020, 2021, 2022, 2024, 2025 (aucun rapport n'a été publié pour la session 2023, selon toi ; non vérifié sur le site officiel). Observations en paraphrase fidèle ; les citations entre guillemets sont verbatim. Pages = pagination imprimée."))
    data = [['Année', 'Page', 'Observation du jury', 'Rubriques', 'Pb candidats', 'Conséquence pour ta révision']]
    for (an, pg, o, rub, pb, cons) in JURY[ue]:
        data.append([str(an), pg, o, rub.replace('|', ' ') or 'général', 'oui' if pb else '—', cons])
    S.append(tbl(data, [11 * mm, 12 * mm, 78 * mm, 20 * mm, 13 * mm, 44 * mm]))
    S.append(P('Thèmes cités par plusieurs jurys successifs', 'h2'))
    rec = [r for r in srt if r['jury_n'] >= 2]
    S += [B(f"<b>{r['code']} {r['titre']}</b> — cité dans {r['jury_n']} rapports ({', '.join(str(a) for a in sorted({j[0] for j in r['jury']}))})"
            + (f", dont {r['diff_n']} difficulté(s) de candidats signalée(s)" if r['diff_n'] else '') + '.') for r in rec]
    S.append(P('Constantes méthodologiques (tous rapports)', 'h2'))
    S += [B("Contextualiser : ne pas « réciter son cours » ni plaquer des « morceaux de cours » [2024 UE3 p. 25 ; 2024 UE5 p. 29 ; 2025 UE3 p. 29]."),
          B("Mobiliser explicitement le corpus théorique (auteurs, modèles, référentiels) [2024 UE2 p. 23 ; 2025 UE2 p. 27 ; 2025 UE5 p. 37]."),
          B("Soigner la forme : orthographe, présentation, tableaux (flux de trésorerie, amortissements) [2024 UE2 p. 24 ; 2025 UE2 p. 27]."),
          B("Gérer le temps : lecture complète du sujet, ne pas sacrifier un dossier fortement doté [2025 UE2 p. 26 ; 2020-2021 UE3 p. 7-8]."),
          B("Aucune impasse : « un point retenu pour une session qui présente un niveau trop faible peut être retenu dès l'année suivante » [2025, p. 21].")]
    S.append(CondPageBreak(170 * mm))
    # --- 7. croisement
    S.append(P('7. Croisement programme / jury / annales / tes ressources', 'h1'))
    S.append(P('7.1 Indice de priorité de révision', 'h2'))
    S.append(img(ch['ipr']))
    S.append(PageBreak())
    S.append(P('7.2 Matrice de croisement', 'h2'))
    data = [['Rubrique', 'Partie', 'Annales (2020-25 / 3 dern.)', 'Jury (cit. / diff.)', 'Tes cours (support)', 'Statut déclaré', 'IPR', 'Catégorie']]
    for r in srt:
        cs, stt = COURS[ue].get(r['code'], ('—', '—'))
        data.append([f"<b>{r['code']}</b> {short(r['titre'], 30)}", 'Partie ' + r['partie'].split('.')[0], f"{pct(r['fcur'])} / {pct(r['f3'])}", f"{r['jury_n']} / {r['diff_n']}",
                     cs, stt, fr(r['ipr'], 1), r['cat'].replace('PRIORITÉ ', '').capitalize()])
    S.append(tbl(data, [42 * mm, 16 * mm, 20 * mm, 15 * mm, 43 * mm, 13 * mm, 10 * mm, 19 * mm]))
    S.append(P(COURS_NOTE, 'small'))
    S.append(P('7.3 Les « trous » du programme', 'h2'))
    S.append(P("Rubriques rarement ou jamais évaluées récemment mais toujours au programme : ce sont des zones potentielles à ne pas négliger malgré leur faible fréquence historique, et non des prédictions."))
    data = [['Rubrique', 'Dernière apparition (principal)', 'Commentaire et effort minimal conseillé']]
    for c, t in TROUS[ue].items():
        r = next(x for x in res if x['code'] == c)
        data.append([f"<b>{c}</b> {r['titre']}", str(r['last'] or 'jamais (2016-2025)'), t])
    S.append(tbl(data, [55 * mm, 28 * mm, 95 * mm]))
    S.append(CondPageBreak(170 * mm))
    # --- 8. priorités
    S.append(P('8. Priorités 2026', 'h1'))
    for cat in CATS:
        lst = [r for r in srt if r['cat'] == cat]
        if not lst: continue
        S.append(P(cat.capitalize() if cat.startswith('À') or cat == 'COMPLÉMENT' else cat.capitalize(), 'h2'))
        for r in lst:
            S.append(B(f"<b>{r['code']} {r['titre']}</b> (IPR {fr(r['ipr'], 1)}) — {r['notions']}."))
    S.append(CondPageBreak(170 * mm))
    # --- 9. thème par thème
    S.append(P('9. Analyse détaillée thème par thème', 'h1'))
    S.append(P("Rubriques classées par indice décroissant. Les annales listées sont celles où la rubrique est mobilisée en principal (les 5 plus récentes)."))
    for r in srt:
        cs, stt = COURS[ue].get(r['code'], ('—', '—'))
        blk = [P(f"{r['code']} — {r['titre']}", 'h2'),
               tbl([['Partie du programme', 'Catégorie / IPR', 'Fréq. 2016-25', 'Fréq. 2020-25', 'Fréq. 3 dern.', 'Dernière', 'Poids quand présent'],
                    [r['partie'], f"{r['cat'].replace('PRIORITÉ ', '').capitalize()} / {fr(r['ipr'], 1)}", pct(r['f10']), pct(r['fcur']), pct(r['f3']),
                     str(r['last'] or 'jamais'), pct(r['w_when']) if r['w_when'] else '—']],
                   [44 * mm, 30 * mm, 19 * mm, 19 * mm, 18 * mm, 16 * mm, 32 * mm]),
               Spacer(1, 2),
               P(f"<b>Années concernées (principal) :</b> {', '.join(str(y) for y in YEARS if r['years'][y] > 0) or 'aucune'} ; "
                 f"<b>en toile de fond :</b> {', '.join(str(y) for y in YEARS if r['yearsA'][y] > 0 and r['years'][y] == 0) or 'aucune'}."),
               P(f"<b>Compétences concrètes à maîtriser :</b> {r['notions']}."),
               P(f"<b>Remarques du jury :</b> " + (' '.join(f"[{a}, {pg}] {o}" for a, pg, o, pb, c in r['jury']) if r['jury'] else "aucune remarque spécifique dans les rapports consultés.")),
               P(f"<b>Raison du classement :</b> {reason(r)}"),
               P(f"<b>Dans tes ressources :</b> {cs} — statut déclaré dans Notion : {stt}."),
               P("<b>Annales à refaire :</b> " + ('<br/>'.join(annales_rubrique(ue, r, rows)) or "aucune annale 2016-2025 en principal : travailler sur le cours et un mini-cas.")),
               P("<b>Ce qu'attendaient les corrigés officiels :</b> " + ('<br/>'.join(f"<b>{a['annee']} D{a['dossier']} — {a['question']}</b> : {a['attendus_du_corrige']}"
                  + (f" <i>Vigilance : {a['pieges_et_vigilance']}</i>" if a['pieges_et_vigilance'] else '') for a in attendus_rubrique(ue, r, rows, att))
                  or "aucun corrigé 2020-2025 ne mobilise cette rubrique en principal.")),
               Spacer(1, 3)]
        S.append(KeepTogether(blk[:3])); S += blk[3:]
    S.append(CondPageBreak(170 * mm))
    # --- 10. annales
    S.append(P('10. Annales recommandées', 'h1'))
    S.append(P("Ordre conseillé : du plus récent (format et attentes actuels) vers l'ancien programme, en conditions réelles pour au moins un sujet complet."))
    data = [['Annale', 'Compétences travaillées et intérêt pédagogique']] + [[f"<b>{a}</b>", t] for a, t in ANNALES[ue]]
    S.append(tbl(data, [42 * mm, 136 * mm]))
    S.append(P('10.1 Par thème prioritaire', 'h2'))
    for r in [x for x in srt if x['cat'] in CATS[:3]]:
        a = annales_rubrique(ue, r, rows)
        if a: S.append(P(f"<b>{r['code']} {r['titre']}</b><br/>" + '<br/>'.join('→ ' + x for x in a)))
    S.append(CondPageBreak(120 * mm))
    S.append(P('10.2 Ce qu\'attendent les corrigés officiels (2020-2025, question par question)', 'h2'))
    S.append(P("Synthèse des éléments indicatifs de corrigé : résultats chiffrés de référence, notions attendues et pièges. Les corrigés sont « indicatifs » : d'autres réponses argumentées sont acceptées. Les chiffres ont été recalculés quand c'était possible."))
    data = [['Session', 'Question', 'Barème', 'Attendus du corrigé', 'Pièges et vigilance']]
    for a in sorted(att, key=lambda a: (a['annee'], a['dossier']), reverse=True):
        data.append([f"{a['annee']} D{a['dossier']}", a['question'], a['bareme'], a['attendus_du_corrige'], a['pieges_et_vigilance']])
    S.append(tbl(data, [15 * mm, 30 * mm, 14 * mm, 75 * mm, 44 * mm]))
    S.append(P(f"Source : 02_data/{ue}_attendus_corriges.csv (colonne source : fichier du corrigé). n.c. = barème par question non communiqué.", 'small'))
    alert = [a for a in att if 'ALERTE' in a['pieges_et_vigilance'] or 'ALERTE' in a['attendus_du_corrige']]
    S.append(P('10.3 Corrigés à lire avec prudence', 'h2'))
    if alert:
        S.append(P("Points où le corrigé semble contenir une erreur ou une information dépassée. Ne pas apprendre le chiffre ou la règle du corrigé sans vérification dans ton cours ou auprès de ton enseignant."))
        S += [B(f"<b>{a['annee']} D{a['dossier']} — {a['question']}</b> : {a['pieges_et_vigilance'] if 'ALERTE' in a['pieges_et_vigilance'] else a['attendus_du_corrige']}") for a in alert]
    else:
        S.append(P("Aucune anomalie relevée dans les corrigés lus."))
    S.append(CondPageBreak(170 * mm))
    # --- 11. checklist
    S.append(P('11. Checklist de révision', 'h1'))
    S.append(P("Coche une case seulement après une restitution correcte, sans aide, sur une question d'annale (règle reprise de ta méthode Notion : « repéré ≠ étudié ; étudié ≠ réussi seul »)."))
    for cat in CATS:
        lst = [r for r in srt if r['cat'] == cat]
        if not lst: continue
        S.append(P(cat.capitalize(), 'h3'))
        for r in lst:
            items, buf, depth = [], '', 0
            for ch_ in r['notions']:
                depth += (ch_ == '(') - (ch_ == ')')
                if ch_ == ',' and depth == 0:
                    items.append(buf.strip()); buf = ''
                else:
                    buf += ch_
            items.append(buf.strip()); items = [x for x in items if x]
            S.append(P(f"<b>{r['code']} {r['titre']}</b>"))
            S.append(P('&nbsp;&nbsp;'.join(f"☐ {x}" for x in items), 'b'))
    S.append(P('Méthode (toutes rubriques)', 'h3'))
    S += [P(x, 'b') for x in ["☐ Un sujet complet en temps réel", "☐ Définir chaque concept demandé avant de l'appliquer",
                              "☐ Citer un auteur, un modèle ou un référentiel par réponse rédigée", "☐ Contextualiser chaque argument au cas",
                              "☐ Présenter les calculs en tableaux, avec leurs formules", "☐ Relire la copie (orthographe) pendant 5 minutes"]]
    S.append(CondPageBreak(170 * mm))
    # --- 12. sources
    S.append(P('12. Sources', 'h1'))
    src = SOURCES(ue, rows)
    data = [['Source', 'Organisme', 'Année', 'Lien ou chemin']] + src
    S.append(tbl(data, [64 * mm, 30 * mm, 15 * mm, 69 * mm]))
    doc.multiBuild(S)
    return fn, res

def link(u, label=None):
    return f'<link href="{u}" color="#1c5cab"><u>{label or u}</u></link>'

CORR = {
 'UE2': {'2025': '1VyyKcpbKQMFO1Q1HWEsJ7ePS-8i3p0Xm', '2024': '1Ynbj96O5VQmAWUJtCLxwL9_Q_PhQb774', '2023': '1Sy9p7pZ5Xb7p85ZXfRkcykmnSeA7ZmPP',
         '2022-S1': '1DK-UytkLXYDX3jO-zr8sqjaBR9ceQDVv', '2022-S2': '195xbM4fcoUkDgDG42BCNn0Xb1hAIsRqd', '2021': '1fayxXx8Yd_7y5iHW_hFzLiv_SxLpbEVO', '2020': '1agfC5cyoSYfiForcBlRWb04t1QbOyRR4'},
 'UE3': {'2025': '1irKIEaezI8N3EG1xgiJGNVG50ZhSAgV4', '2024': '183QNpAJ0I1tPmx22_Gx-bkJGOwxixLZ2', '2023': '1TsDftRM2UUzNSuKA92-_ayHUVFE0bp3e', '2022': '1_Bx33FaSMe6wD9KiLurXEnkfOZ01qV--',
         '2021': '1WS2cRZP5ysjQMWEzOHfbq6kp8oJCwBYo', '2020': '1ql7hwyfHiHC_lvRp7McdXzAN103_6u1T'},
 'UE5': {'2025': '1BEsDUzNE4onNpgm4tRLulqtNtfiuy9WP', '2024': '1QQ_uF8gU-bwjMuZ4iRuKXqdAVb1M8Lib', '2023': '1CR9tu9QcKhTYPWpSFmTUTfL_vjeQSUrH',
         '2022': '1JuMyuPIJ2yRa8Wm2X4SuTtbtPM_nKX_E', '2021': '1moGNzX5oR_n-Z0vmQze3SRwDE3U_pn4j', '2020': '1Cq8YX9LolnuaS21GS64M5o_rv2lMZ9AT'},
}
PROG = {
 'UE2': ["Programme officiel UE2 Finance (texte de l'annexe reproduit en tête du manuel)", "Dunod, manuel DSCG 2 Finance", "—", "Drive / 07_ressources ; extrait : 00_sources_officielles/bulletin_officiel/programme_UE2_via_Dunod.txt"],
 'UE3': ["Programme officiel UE3 Management et contrôle de gestion (texte de l'annexe reproduit en tête du manuel)", "Dunod, manuel DSCG 3", "—", "Drive / 07_ressources ; extrait : 00_sources_officielles/bulletin_officiel/programme_UE3_via_Dunod.txt"],
 'UE5': ["Programme officiel UE5 MSI — document « Programme MSI 19-20 » (6 p.)", "Enseignante (dossier Drive « Rapports de jury et programme MSI »)", "2019", "transcription : 00_sources_officielles/bulletin_officiel/programme_UE5_transcription.txt"],
}

def SOURCES(ue, rows):
    d = 'https://drive.google.com/file/d/'
    s = [
     ["Rapport du jury du DSCG — session 2020", "Jury national DSCG (MESR)", "2020", link(d + '1QwiqmpNS9gU9UQja4WPZ8D7fiL9fDxw2/view', 'Drive : Rapport_jury_DSCG_2020.pdf')],
     ["Rapport du jury du DSCG — session 2022", "Jury national DSCG (MESR)", "2023", link(d + '1xJNRdr0s2NEAtMP24U0rJaI8el5WsmiS/view', 'Drive : rapport-du-jury-sur-la-session-2022-du-dscg-39080.pdf')],
     ["Rapport du jury du DSCG — session 2021", "Jury national DSCG (MESR)", "2021", link(d + '1Op95l3PKyXaIgv_fjIO_1GZItCaDUKzU/view', 'Drive : Rapport_jury_DSCG_2021.pdf') + ' ; ' + link('https://www.ac-strasbourg.fr/media/15311/download', 'ac-strasbourg')],
     ["Rapport du jury national du DSCG — session 2024", "Jury national DSCG (MESR)", "2025", link('https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2025-03/rapport-du-jury-national-du-dscg---2024-36344.pdf', 'enseignementsup-recherche.gouv.fr') + ' ; ' + link(d + '163LAI9oQuAkTwVgxUHy6yB_mDZcfLttA/view', 'copie Drive')],
     ["Rapport du jury national du DSCG — session 2025", "Jury national DSCG (MESR)", "2026", link('https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2026-03/rapport-du-jury-national-du-dscg---2025-39591.pdf', 'enseignementsup-recherche.gouv.fr') + ' ; ' + link(d + '16PrV4HSQGDYq5aY9_nYwl9-_lsRB2Old/view', 'copie Drive')],
     ["Arrêté du 13 février 2019 — annexe II (programme DSCG), BO ESR n°25 du 20 juin 2019", "MESR", "2019", link('https://cache.media.education.gouv.fr/file/25/01/7/ensup135_annexe2_1142017.pdf', 'ensup135_annexe2_1142017.pdf') + " (non ouvert : domaine bloqué ; texte relu via la reproduction ci-dessous)"],
     PROG[ue],
     ["Arrêté du 4 août 2025 réformant les programmes DSCG (application session 2027)", "MESR (BO ESR 28/08/2025)", "2025", "texte officiel non consulté ; " + link('https://www.compta-online.com/reforme-du-dscg-ao8849', 'Compta Online — réforme du DSCG')],
     ["Page Notion « Programme officiel 2026 — couverture et preuves de Sacha »", "Notion (Sacha)", "2026", link('https://app.notion.com/p/3e49f8997e9f813285d6efb00aed4ad1', 'Notion')],
     ["Page Notion « Annales 2020–2025 — Couverture et priorités » (base héritée, index uniquement)", "Notion (Sacha)", "2026", link('https://app.notion.com/p/6129f8997e9f8267a08b81758d44b47c', 'Notion')],
    ]
    if ue == 'UE2':
        s += [["Annulation de l'épreuve de finance session 2022 et nouvelle date", "MESR, BO ESR n°46 (2022)", "2022", link('https://www.enseignementsup-recherche.gouv.fr/fr/bo/22/Hebdo46/ESRS2233990A.htm', 'ESRS2233990A') + " (repéré par recherche, non ouvert)"],
              ["Pronostic DSCG UE2 Finance : thèmes récurrents sur 12 ans (contrôle secondaire)", "Compta Online", "2025-26", link('https://www.compta-online.com/analyse-des-sujets-du-dscg-ue2-finance-ao4627')],
              ["Fascicules INTEC UE212 Finance, cours 1 à 4 (2025/2026)", "Cnam-Intec", "2025", "Drive, dossier COURS 1-4 ; /Users/sacha/Documents/DSCG/UE 2 - Finance/Cours INTEC/"]]
    if ue == 'UE3':
        s += [["Pronostic DSCG UE3 : thèmes récurrents sur 12 sessions (contrôle secondaire)", "Compta Online", "2025-26", link('https://www.compta-online.com/analyse-des-sujets-du-dscg-ue3-management-et-controle-de-gestion-ao4628')],
              ["Livre Dunod MCG UE3 ; cours de l'enseignante", "Dunod ; établissement", "—", "/Users/sacha/Documents/DSCG/UE 3 - MCG/"],
              ["Page Notion « UE3 2024 — apprendre » (découpage des questions 2024)", "Notion (Sacha)", "2026", link('https://app.notion.com/p/06b9f8997e9f8241a71281b43468d614', 'Notion')]]
    if ue == 'UE5':
        s += [["Pronostic DSCG UE5 : thèmes récurrents sur 12 sessions (contrôle secondaire)", "Compta Online", "2025-26", link('https://www.compta-online.com/analyse-des-sujets-du-dscg-ue5-management-des-systemes-information-ao4630')],
              ["Notes Drive UE5-01 à UE5-07 (cadrage, matrice, sécurité moderne)", "Sacha (session Claude du 27/08/2026)", "2026", link('https://docs.google.com/document/d/1GPQsrbp1XjcbGl4-jc6M_O_Ao3vcs5SXiu0qLdEjd0I/edit', 'UE5-01 cadrage')],
              ["Cours et fiches UE5 (enseignante), Expert DSCG UE5", "établissement ; éditeur", "—", "/Users/sacha/Documents/DSCG/UE 5 - MSI/ ; Drive « Expert DSCG UE 5.pdf »"]]
    s.append([f"Éléments indicatifs de corrigé DSCG {ue} sessions 2020-2025 [Corrigé {ue} année]", "Jury national (copies FicheBEN / Drive)", "2020-25",
              ' ; '.join(link(d + i + '/view', a) for a, i in sorted(CORR[ue].items(), reverse=True))])
    seen = set()
    anc = sorted({r['annee'] for r in rows if r['y'] < 2020})
    s.append([f"Sujets DSCG {ue} sessions {anc[0]} à {anc[-1]} (ancien programme) [DSCG {ue} {anc[0]}-{anc[-1]}]", "SIEC / MESR (sujets nationaux)", f"{anc[0]}-{anc[-1][2:]}",
              ' ; '.join(link(d + __import__('re').search(r'id ([A-Za-z0-9_-]{20,})', next(x['source'] for x in rows if x['annee'] == a)).group(1) + '/view', a) for a in anc) + " — copies FicheBEN (Drive)"])
    seen |= set(anc)
    for r in sorted(rows, key=lambda x: x['annee'], reverse=True):
        if r['annee'] in seen: continue
        seen.add(r['annee'])
        src = r['source']
        import re
        m = re.search(r'id ([A-Za-z0-9_-]{20,})', src)
        lk = link(d + m.group(1) + '/view', 'Drive') if m else ''
        if 'transcription' in src and 'md' in src:
            lk = link('https://docs.google.com/document/d/1g__P49S4v7SlFi60ml47MOeCecoZISj5bAdFNCqv_u4/edit', 'Drive (transcription)')
        s.append([f"Sujet DSCG {ue} session {r['annee']} [DSCG {ue} {r['annee']}]", "SIEC / MESR (sujet national)", r['annee'][:4],
                  (lk + ' — ' if lk else '') + r['statut_source'].split(' ; ')[0]])
    return s

if __name__ == '__main__':
    for ue in sys.argv[1:] or ['UE2', 'UE3', 'UE5']:
        fn, res = build(ue)
        print('OK', fn)
