#!/usr/bin/env python3
"""Legge le creativita' nella cartella creativita/ e controlla i nomi. Non rinomina e non sposta nulla.

Uso:
  python3 creativita.py elenco  [cartella]   -> per ogni file: fase, tipologia, risoluzione, formato, audio
  python3 creativita.py verifica [cartella]  -> controlla i nomi dopo la rinomina e stampa la lista inserzioni

Cartella di default: creativita/ nella radice del progetto.
Solo libreria standard: funziona su Mac e Windows senza installare nulla.
"""
import os
import re
import struct
import sys
from collections import defaultdict

IMMAGINI = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO = {".mp4", ".mov", ".m4v"}
SCARTA = {".ds_store", "thumbs.db", "desktop.ini"}


# ---------------------------------------------------------------- risoluzioni

def dim_png(f):
    f.seek(0)
    h = f.read(24)
    if h[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", h[16:24])


def dim_jpeg(f):
    f.seek(0)
    if f.read(2) != b"\xff\xd8":
        return None
    while True:
        b = f.read(1)
        while b and b != b"\xff":
            b = f.read(1)
        while b == b"\xff":
            b = f.read(1)
        if not b:
            return None
        marker = b[0]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            continue
        lung = struct.unpack(">H", f.read(2))[0]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            dati = f.read(5)
            h, w = struct.unpack(">HH", dati[1:5])
            return w, h
        f.seek(lung - 2, 1)


def dim_webp(f):
    f.seek(0)
    h = f.read(30)
    if h[:4] != b"RIFF" or h[8:12] != b"WEBP":
        return None
    tipo = h[12:16]
    if tipo == b"VP8 ":
        w, hh = struct.unpack("<HH", h[26:30])
        return w & 0x3FFF, hh & 0x3FFF
    if tipo == b"VP8L":
        b = h[21:25]
        w = 1 + (((b[1] & 0x3F) << 8) | b[0])
        hh = 1 + (((b[3] & 0x0F) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
        return w, hh
    if tipo == b"VP8X":
        w = 1 + int.from_bytes(h[24:27], "little")
        hh = 1 + int.from_bytes(h[27:30], "little")
        return w, hh
    return None


def box(f, inizio, fine):
    """Scorre i box MP4/MOV tra inizio e fine: (tipo, inizio_dati, fine_box)."""
    pos = inizio
    while pos + 8 <= fine:
        f.seek(pos)
        testa = f.read(8)
        if len(testa) < 8:
            return
        taglia, tipo = struct.unpack(">I4s", testa)
        dati = pos + 8
        if taglia == 1:
            taglia = struct.unpack(">Q", f.read(8))[0]
            dati += 8
        elif taglia == 0:
            taglia = fine - pos
        if taglia < 8:
            return
        yield tipo, dati, pos + taglia
        pos += taglia


def info_video(f, dimensione):
    """Ritorna ((larghezza, altezza) gia' ruotate, ha_audio)."""
    for tipo, d, e in box(f, 0, dimensione):
        if tipo != b"moov":
            continue
        risoluzione, audio = None, False
        for t2, d2, e2 in box(f, d, e):
            if t2 != b"trak":
                continue
            tk, handler = None, None
            for t3, d3, e3 in box(f, d2, e2):
                if t3 == b"tkhd":
                    f.seek(d3)
                    versione = f.read(1)[0]
                    salto = 4 + (32 if versione == 1 else 20) + 16
                    f.seek(d3 + salto)
                    matrice = struct.unpack(">9i", f.read(36))
                    w, h = struct.unpack(">II", f.read(8))
                    w, h = w >> 16, h >> 16
                    if matrice[0] == 0 and matrice[1] != 0:  # ruotato di 90 o 270 gradi
                        w, h = h, w
                    tk = (w, h)
                elif t3 == b"mdia":
                    for t4, d4, e4 in box(f, d3, e3):
                        if t4 == b"hdlr":
                            f.seek(d4 + 8)
                            handler = f.read(4)
            if handler == b"vide" and tk and tk[0] and risoluzione is None:
                risoluzione = tk
            elif handler == b"soun":
                audio = True
        return risoluzione, audio
    return None, False


def leggi_file(percorso):
    est = os.path.splitext(percorso)[1].lower()
    with open(percorso, "rb") as f:
        if est in VIDEO:
            return info_video(f, os.path.getsize(percorso))
        for funz in (dim_png, dim_jpeg, dim_webp):
            try:
                r = funz(f)
            except (struct.error, IndexError):
                r = None
            if r:
                return r, None
    return None, None


# ---------------------------------------------------------------- formato

def formato(w, h):
    r = w / h
    if abs(r - 9 / 16) < 0.02:
        return "story"
    if abs(r - 1) < 0.02 or abs(r - 4 / 5) < 0.02:
        return "feed"
    return "?"


def leggi_setup(radice):
    valori = {}
    p = os.path.join(radice, "mio-setup.md")
    if os.path.isfile(p):
        with open(p, encoding="utf-8") as f:
            for riga in f:
                m = re.match(r"^\s*-\s*([a-z_]+)\s*:\s*(.*?)\s*$", riga)
                if m:
                    valori[m.group(1)] = m.group(2)
    def ris(chiave):
        out = set()
        for v in valori.get(chiave, "").replace("×", "x").split(","):
            m = re.match(r"^\s*(\d+)\s*x\s*(\d+)\s*$", v)
            if m:
                out.add((int(m.group(1)), int(m.group(2))))
        return out
    return ris("risoluzioni_feed"), ris("risoluzioni_story")


# ---------------------------------------------------------------- cartelle

def radice_progetto():
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and os.path.isdir(env):
        return env
    qui = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(qui, "..", "..", "..", ".."))


def fase_da_cartelle(parti):
    for p in parti:
        pl = p.lower()
        if "prospect" in pl:
            return "PROSPECTING"
        if "retarget" in pl:
            return "RETARGETING"
    return ""


def scansiona(cartella):
    righe = []
    for base, dirs, files in os.walk(cartella):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for nome in sorted(files):
            if nome.startswith(".") or nome.lower() in SCARTA:
                continue
            est = os.path.splitext(nome)[1].lower()
            if est not in IMMAGINI | VIDEO:
                continue
            percorso = os.path.join(base, nome)
            rel = os.path.relpath(percorso, cartella)
            parti = rel.split(os.sep)[:-1]
            fase = fase_da_cartelle(parti)
            tip_parti = [p for p in parti if not fase_da_cartelle([p])]
            tipologia = tip_parti[-1] if tip_parti else ""
            try:
                ris, audio = leggi_file(percorso)
            except (OSError, struct.error, IndexError):
                ris, audio = None, None
            righe.append({
                "rel": rel, "nome": nome, "est": est, "fase": fase, "tipologia": tipologia,
                "ris": ris, "audio": audio, "video": est in VIDEO,
            })
    return righe


# ---------------------------------------------------------------- comandi

def cmd_elenco(cartella, radice):
    feed_ok, story_ok = leggi_setup(radice)
    righe = scansiona(cartella)
    if not righe:
        print("Nessuna immagine o video trovato in %s" % cartella)
        return
    print("file | fase | tipologia (cartella) | risoluzione | formato | audio | note")
    for r in righe:
        note = []
        if r["ris"]:
            w, h = r["ris"]
            fmt = formato(w, h)
            ris = "%dx%d" % (w, h)
            attese = feed_ok if fmt == "feed" else story_ok if fmt == "story" else set()
            if fmt == "?":
                note.append("rapporto non riconosciuto: chiedere allo studente")
            elif attese and (w, h) not in attese:
                note.append("risoluzione fuori da quelle del setup")
        else:
            ris, fmt = "illeggibile", "?"
            note.append("non riesco a leggere la risoluzione")
        audio = ("si" if r["audio"] else "NO") if r["video"] else "-"
        if r["video"] and not r["audio"]:
            note.append("video senza traccia audio: segnalarlo")
        if not r["tipologia"]:
            note.append("file fuori da una cartella tipologia")
        print("%s | %s | %s | %s | %s | %s | %s" % (
            r["rel"], r["fase"] or "-", r["tipologia"] or "-", ris, fmt, audio, "; ".join(note) or "ok"))


RE_NOME = re.compile(
    r"^(?:(?P<fase>PROSPECTING|RETARGETING)_)?(?P<base>.+?)_(?P<pos>feed|story)_(?P<mm>\d{2})_(?P<aaaa>\d{4})(?P<piu>\+1)?$")


def cmd_verifica(cartella, radice):
    righe = scansiona(cartella)
    if not righe:
        print("Nessuna immagine o video trovato in %s" % cartella)
        return
    errori, avvisi = [], []
    gruppi = defaultdict(list)
    mesi = set()
    for r in righe:
        radice_nome = os.path.splitext(r["nome"])[0]
        m = RE_NOME.match(radice_nome)
        if not m:
            errori.append("%s: il nome non segue lo schema {Tipologia}_{n}_{feed|story}_{MM}_{AAAA}" % r["rel"])
            continue
        if " " in radice_nome:
            errori.append("%s: ci sono spazi nel nome, usa _ al loro posto" % r["rel"])
        fase_nome = m.group("fase") or ""
        if r["fase"] and fase_nome != r["fase"]:
            errori.append("%s: sta in una cartella %s ma il nome %s" % (
                r["rel"], r["fase"], "non ha il prefisso di fase" if not fase_nome else "dice " + fase_nome))
        mesi.add((m.group("mm"), m.group("aaaa")))
        chiave = (fase_nome, m.group("base"), m.group("mm"), m.group("aaaa"))
        gruppi[chiave].append((r, m.group("pos"), bool(m.group("piu"))))

    if len(mesi) > 1:
        avvisi.append("nel lotto ci sono mesi diversi: %s" % ", ".join("%s_%s" % x for x in sorted(mesi)))

    for (fase, base, mm, aaaa), files in sorted(gruppi.items()):
        nome_ad = "%s%s_%s_%s" % (fase + "_" if fase else "", base, mm, aaaa)
        for r, pos, _ in files:
            if r["ris"]:
                reale = formato(*r["ris"])
                if reale != "?" and reale != pos:
                    errori.append("%s: il nome dice %s ma il file e' %dx%d (%s)" % (r["rel"], pos, r["ris"][0], r["ris"][1], reale))
        if len(files) == 1:
            errori.append("%s: c'e' un solo file, ne servono due (Feed + Story, oppure il gemello: .png+.jpg per le immagini, copia +1 per i video)" % nome_ad)
            continue
        if len(files) > 2:
            errori.append("%s: %d file con lo stesso nome base, ne servono esattamente due" % (nome_ad, len(files)))
            continue
        (a, pa, piu_a), (b, pb, piu_b) = files
        if {pa, pb} == {"feed", "story"}:
            continue
        if pa == pb == "story":
            if a["video"] and b["video"] and piu_a != piu_b:
                continue
            ext = {a["est"].replace(".jpeg", ".jpg"), b["est"].replace(".jpeg", ".jpg")}
            if not a["video"] and ext == {".png", ".jpg"}:
                continue
        errori.append("%s: la coppia di file non e' valida (%s, %s)" % (nome_ad, a["nome"], b["nome"]))

    # numerazione per fase + tipologia
    numeri = defaultdict(set)
    for (fase, base, _, _) in gruppi:
        m = re.match(r"^(.*)_(\d+)$", base)
        if m:
            numeri[(fase, m.group(1))].add(int(m.group(2)))
    for (fase, tip), ns in sorted(numeri.items()):
        mancanti = sorted(set(range(1, max(ns) + 1)) - ns)
        if mancanti:
            avvisi.append("%s%s: numerazione con buchi, mancano %s" % (fase + " " if fase else "", tip, ", ".join(map(str, mancanti))))

    print("ERRORI: %d" % len(errori))
    for e in errori:
        print("  - " + e)
    print("AVVISI: %d" % len(avvisi))
    for a in avvisi:
        print("  - " + a)

    # lista inserzioni, per fase e per cartella tipologia
    print("\nLISTA INSERZIONI")
    per_fase = defaultdict(lambda: defaultdict(list))
    for (fase, base, mm, aaaa), files in sorted(gruppi.items()):
        tip = files[0][0]["tipologia"] or "senza cartella"
        per_fase[fase or "UNICA"][tip].append("%s%s_%s_%s" % (fase + "_" if fase else "", base, mm, aaaa))
    con_fasi = any(f != "UNICA" for f in per_fase)
    for fase in sorted(per_fase, key=lambda x: {"PROSPECTING": 0, "RETARGETING": 1}.get(x, 2)):
        if fase != "UNICA":
            print("\n## %s" % fase)
        elif con_fasi:
            print("\n## SENZA FASE (da sistemare)")
        for tip, nomi in per_fase[fase].items():
            print("\n%s" % tip.upper().replace("_", " "))
            for n in sorted(set(nomi), key=lambda s: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]):
                print(n)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("elenco", "verifica"):
        print(__doc__)
        return 1
    radice = radice_progetto()
    cartella = sys.argv[2] if len(sys.argv) > 2 else os.path.join(radice, "creativita")
    if not os.path.isdir(cartella):
        print("Cartella non trovata: %s" % cartella)
        return 1
    if sys.argv[1] == "elenco":
        cmd_elenco(cartella, radice)
    else:
        cmd_verifica(cartella, radice)
    return 0


if __name__ == "__main__":
    sys.exit(main())
