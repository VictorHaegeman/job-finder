#!/usr/bin/env python3
"""Génère un CV et une lettre de motivation (PDF, 1 page, Helvetica, non compressés)
pour chaque fichier JSON d'entreprise d'un dossier, à partir du profil du candidat.

Usage :
    python3 generate_docs.py --profile profil.json --jobs dossier_jobs/

Les PDF sont non compressés pour que Gmail indexe leur texte : c'est ce qui permet
de vérifier, avant l'envoi, que les bonnes pièces jointes sont dans le brouillon.
Si le contenu dépasse une page, la taille de police est réduite automatiquement
(jusqu'à 84 %) ; au-delà, le script s'arrête en erreur et il faut raccourcir le texte.
"""
import argparse, json, os, sys
from reportlab import rl_config
rl_config.useA85 = 0
rl_config.invariant = 1
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth

W, H = A4
LM, RM = 42, 42
BOTTOM = 28
ACCENT = (0.12, 0.2, 0.36)
LINK = (0.05, 0.25, 0.6)
SCALES = [1.0, 0.96, 0.92, 0.88, 0.84]


def wrap(text, font, size, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if stringWidth(t, font, size) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class Doc:
    def __init__(self, path, title, author, k=1.0):
        self.c = canvas.Canvas(path, pagesize=A4, pageCompression=0, invariant=1)
        self.c.setTitle(title)
        self.c.setAuthor(author)
        self.k = k
        self.y = H - 40

    def text(self, s, font="Helvetica", size=9.5, lead=None, x=LM, width=None, after=2, color=(0, 0, 0)):
        size *= self.k
        lead = (lead * self.k) if lead else size * 1.22
        width = width or (W - RM - x)
        self.c.setFillColorRGB(*color)
        for ln in wrap(s, font, size, width):
            self.c.setFont(font, size)
            self.c.drawString(x, self.y, ln)
            self.y -= lead
        self.y -= after * self.k
        self.c.setFillColorRGB(0, 0, 0)

    def bullet(self, s, size=9.3):
        size *= self.k
        lead = size * 1.22
        lines = wrap(s, "Helvetica", size, W - LM - RM - 12)
        self.c.setFont("Helvetica", size)
        self.c.drawString(LM + 2, self.y, u"•")
        for ln in lines:
            self.c.drawString(LM + 12, self.y, ln)
            self.y -= lead
        self.y -= 1

    def heading(self, s):
        self.y -= 3 * self.k
        self.c.setFillColorRGB(*ACCENT)
        self.c.setFont("Helvetica-Bold", 10.2 * self.k)
        self.c.drawString(LM, self.y, s.upper())
        self.y -= 3 * self.k
        self.c.setStrokeColorRGB(*ACCENT)
        self.c.setLineWidth(0.7)
        self.c.line(LM, self.y, W - RM, self.y)
        self.y -= 11 * self.k
        self.c.setFillColorRGB(0, 0, 0)

    def link_line(self, links, sep="   |   ", size=9):
        size *= self.k
        x = LM
        self.c.setFont("Helvetica", size)
        for i, l in enumerate(links):
            if i:
                self.c.setFillColorRGB(0, 0, 0)
                self.c.drawString(x, self.y, sep)
                x += stringWidth(sep, "Helvetica", size)
            t, u = l["label"], l["url"]
            w = stringWidth(t, "Helvetica", size)
            self.c.setFillColorRGB(*LINK)
            self.c.drawString(x, self.y, t)
            self.c.linkURL(u, (x, self.y - 2, x + w, self.y + size), relative=0)
            x += w
        self.c.setFillColorRGB(0, 0, 0)
        self.y -= size * 1.3

    def save(self):
        self.c.save()


def pick(items, catalog):
    """Accepte soit des clés du catalogue du profil, soit du texte libre."""
    return [catalog.get(i, i) for i in items]


def make_cv(p, d, path, k):
    idt, cv = p["identite"], p["cv"]
    full = f'{idt["prenom"]} {idt["nom"]}'
    doc = Doc(path, f"CV {full}", full, k)
    c = doc.c
    c.setFont("Helvetica-Bold", 17 * k)
    c.drawString(LM, doc.y, full.upper())
    doc.y -= 19 * k
    c.setFillColorRGB(*ACCENT)
    c.setFont("Helvetica-Bold", 11 * k)
    c.drawString(LM, doc.y, d["cv_title"])
    doc.y -= 14 * k
    c.setFillColorRGB(0, 0, 0)
    contact = "  |  ".join(x for x in [idt.get("telephone"), idt.get("email"), idt.get("ville"), idt.get("mobilite")] if x)
    doc.text(contact, size=9, after=0)
    if idt.get("liens"):
        doc.link_line(idt["liens"])
    doc.heading(cv.get("titre_profil", "Profil"))
    doc.text(d["cv_profile"], size=9.3)
    doc.heading("Compétences clés")
    for b in pick(d["cv_skills"], cv.get("competences_cles", {})):
        doc.bullet(b)
    doc.heading("Formation")
    for b in cv["formation"]:
        doc.bullet(b)
    projets = pick(d.get("cv_projects", []), cv.get("projets", {}))
    if projets:
        doc.heading("Projets")
        for b in projets:
            doc.bullet(b)
    if cv.get("experiences"):
        doc.heading("Expériences")
        for b in cv["experiences"]:
            doc.bullet(b)
    if cv.get("competences_techniques"):
        doc.heading("Compétences techniques")
        doc.text(d.get("cv_tech", cv["competences_techniques"]), size=9)
    if cv.get("langues_interets"):
        doc.text(cv["langues_interets"], size=9)
    doc.save()
    return doc.y


def make_lm(p, d, path, k):
    idt = p["identite"]
    full = f'{idt["prenom"]} {idt["nom"]}'
    doc = Doc(path, f"Lettre de motivation {full}", full, k)
    c = doc.c
    c.setFont("Helvetica-Bold", 12 * k)
    c.drawString(LM, doc.y, full)
    doc.y -= 13 * k
    if p.get("accroche_entete"):
        doc.text(p["accroche_entete"], size=9, after=0)
    doc.text(" – ".join(x for x in [idt.get("telephone"), idt.get("email"), idt.get("ville")] if x), size=9, after=0)
    if idt.get("liens"):
        doc.link_line(idt["liens"], sep="  –  ")
    doc.y -= 6 * k
    xr = W - RM - 230
    for ln in d["lm_dest"]:
        doc.text(ln, size=9.5, after=0, x=xr, width=230)
    doc.y -= 4 * k
    doc.text(f'{idt.get("ville_lettre", idt.get("ville", ""))}, le {d["date_fr"]}', size=9.5, x=xr, width=230)
    doc.y -= 4 * k
    doc.text("Objet : " + d["lm_objet"], font="Helvetica-Bold", size=9.8, after=6)
    for para in d["body"].split("\n\n"):
        doc.text(para, size=9.8, lead=12.6, after=5)
    doc.text(d["lm_closing"], size=9.8, lead=12.6, after=10)
    doc.text(full, font="Helvetica-Bold", size=10)
    doc.save()
    return doc.y


def fit(maker, p, d, path):
    for k in SCALES:
        if maker(p, d, path, k) >= BOTTOM:
            return k
    raise SystemExit(f"ERREUR : {os.path.basename(path)} dépasse une page même réduit à 84 % – raccourcir le texte.")


def safe(s):
    return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in s.replace(" ", "_")).strip("_")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--jobs", required=True)
    a = ap.parse_args()
    p = json.load(open(a.profile, encoding="utf-8"))
    base = safe(f'{p["identite"]["prenom"]}_{p["identite"]["nom"]}')
    for fn in sorted(os.listdir(a.jobs)):
        if not fn.endswith(".json"):
            continue
        d = json.load(open(os.path.join(a.jobs, fn), encoding="utf-8"))
        slug = safe(d["slug"])
        cvp = os.path.join(a.jobs, f"CV_{base}_{slug}.pdf")
        lmp = os.path.join(a.jobs, f"LM_{base}_{slug}.pdf")
        k1 = fit(make_cv, p, d, cvp)
        k2 = fit(make_lm, p, d, lmp)
        print(f"{fn}: CV échelle {k1:.2f} -> {os.path.basename(cvp)} | LM échelle {k2:.2f} -> {os.path.basename(lmp)}")


if __name__ == "__main__":
    main()
