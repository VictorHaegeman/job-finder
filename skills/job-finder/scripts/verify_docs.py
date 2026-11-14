#!/usr/bin/env python3
"""Vérifie les PDF générés avant tout envoi.

Usage :
    python3 verify_docs.py --profile profil.json --jobs dossier_jobs/

Contrôles, pour chaque paire CV / LM :
  - exactement 1 page, texte extractible ;
  - le mot-témoin du CV est dans le CV et pas dans la lettre ;
  - le mot-témoin de la lettre est dans la lettre et pas dans le CV ;
  - aucun outil / compétence listé dans « non_maitrise » n'apparaît ;
  - le nom du candidat est présent.
Code de sortie 1 si un contrôle échoue : dans ce cas, ne rien envoyer.
"""
import argparse, json, os, re, sys
from pypdf import PdfReader


def text_of(path):
    r = PdfReader(path)
    return len(r.pages), " ".join((pg.extract_text() or "") for pg in r.pages)


def has_word(text, word, case=False):
    flags = 0 if case else re.I
    return re.search(r"(?<![\w+#.])" + re.escape(word) + r"(?![\w+#])", text, flags) is not None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--jobs", required=True)
    a = ap.parse_args()
    p = json.load(open(a.profile, encoding="utf-8"))
    t_cv, t_lm = p["mot_temoin_cv"], p["mot_temoin_lm"]
    banned = p.get("non_maitrise", [])
    nom = p["identite"]["nom"]
    ok = True
    files = sorted(f for f in os.listdir(a.jobs) if f.endswith(".pdf"))
    for f in files:
        path = os.path.join(a.jobs, f)
        n, txt = text_of(path)
        errs = []
        if n != 1:
            errs.append(f"{n} pages")
        if len(txt.strip()) < 200:
            errs.append("texte non extractible")
        if nom.lower() not in txt.lower():
            errs.append("nom absent")
        if f.startswith("CV_"):
            if not has_word(txt, t_cv): errs.append(f"mot-témoin CV « {t_cv} » absent")
            if has_word(txt, t_lm): errs.append(f"mot-témoin LM « {t_lm} » présent dans le CV")
        elif f.startswith("LM_"):
            if not has_word(txt, t_lm): errs.append(f"mot-témoin LM « {t_lm} » absent")
            if has_word(txt, t_cv): errs.append(f"mot-témoin CV « {t_cv} » présent dans la lettre")
        for b in banned:
            if has_word(txt, b, case=True):  # sensible à la casse : « Tableau » (outil) ≠ « tableau de bord »
                errs.append(f"mentionne « {b} » (non maîtrisé)")
        size = os.path.getsize(path)
        status = "OK" if not errs else "ÉCHEC : " + " ; ".join(errs)
        ok &= not errs
        print(f"{f} ({size} o) : {status}")
    if not files:
        print("Aucun PDF trouvé."); ok = False
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
