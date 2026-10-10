#!/usr/bin/env python3
"""Controlla che mio-setup.md sia compilato e valido.

Uso:
  python3 controlla_setup.py          -> stampa OK oppure INCOMPLETO + primo campo da compilare
  python3 controlla_setup.py --hook   -> come sopra, ma stampa solo se il setup NON e' completo
                                         (usato dagli hook di .claude/settings.json)

Solo libreria standard. Non modifica nessun file.
"""
import os
import re
import sys

VUOTO = {"", "___", "-", "?", "da compilare"}
NESSUNO = {"nessuno", "nessuna", "no"}

RE_CIFRE = re.compile(r"^\d{6,20}$")
RE_VALUTA = re.compile(r"^[A-Z]{3}$")
RE_PAESI = re.compile(r"^[A-Z]{2}(\s*,\s*[A-Z]{2})*$")
RE_RISOLUZIONI = re.compile(r"^\d{3,5}x\d{3,5}(\s*,\s*\d{3,5}x\d{3,5})*$")


def v_testo(val):
    if val.startswith("{") or val.startswith("<"):
        return "contiene ancora un segnaposto"
    return None


def v_testo_o_nessuno(val):
    return v_testo(val)


def v_cifre(val):
    if val.lower().startswith("act_"):
        return "togli il prefisso act_ e lascia solo i numeri"
    if not RE_CIFRE.match(val):
        return "deve contenere solo numeri (da 6 a 20 cifre), senza spazi"
    return None


def v_valuta(val):
    if not RE_VALUTA.match(val):
        return "scrivi il codice di 3 lettere maiuscole (es. EUR)"
    return None


def v_paesi(val):
    if not RE_PAESI.match(val):
        return "scrivi i codici paese di 2 lettere maiuscole separati da virgola (es. IT oppure IT, CH)"
    return None


def v_risoluzioni(val):
    if not RE_RISOLUZIONI.match(val.replace("×", "x").replace(" x ", "x")):
        return "scrivi larghezza x altezza in pixel, separate da virgola (es. 1080x1080, 1080x1350)"
    return None


def v_lista(val):
    voci = [v.strip() for v in val.split(",") if v.strip()]
    if not voci:
        return "serve almeno una voce"
    return None


def v_scelta(*ammessi):
    def _v(val):
        if val.lower() not in ammessi:
            return "valori ammessi: " + " oppure ".join(ammessi)
        return None
    return _v


def v_utm(val):
    if "utm_source=" not in val or "utm_campaign=" not in val:
        return "deve contenere almeno utm_source= e utm_campaign="
    if val.startswith("?") or val.startswith("http"):
        return "solo i parametri, senza ? iniziale e senza indirizzo del sito"
    return None


# (chiave, validatore, accetta "nessuno")  in ordine di setup
CAMPI = [
    ("modalita_controlli", v_scelta("screenshot", "connettore"), False),
    ("nome_brand", v_testo, False),
    ("nome_account_pubblicitario", v_testo, False),
    ("id_account_pubblicitario", v_cifre, False),
    ("valuta", v_valuta, False),
    ("nome_pixel", v_testo, False),
    ("id_pixel", v_cifre, False),
    ("pagina_facebook", v_testo, False),
    ("account_instagram", v_testo_o_nessuno, True),
    ("inserzionista", v_testo, False),
    ("pagante", v_testo, False),
    ("paesi_target", v_paesi, False),
    ("prefisso_campagne", v_testo_o_nessuno, True),
    ("pubblico_visite_sito", v_testo_o_nessuno, True),
    ("pubblico_engage_instagram", v_testo_o_nessuno, True),
    ("pubblico_engage_facebook", v_testo_o_nessuno, True),
    ("lista_clienti_esclusione", v_testo_o_nessuno, True),
    ("tipologie_creative", v_lista, False),
    ("risoluzioni_feed", v_risoluzioni, False),
    ("risoluzioni_story", v_risoluzioni, False),
    ("parametri_url", v_utm, False),
    ("invito_all_azione", v_testo, False),
]

RE_RIGA = re.compile(r"^\s*-\s*([a-z_]+)\s*:\s*(.*?)\s*$")
RE_FLAG = re.compile(r"^\s*setup_completato\s*:\s*(.*?)\s*$", re.I)


def radice_progetto():
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and os.path.isfile(os.path.join(env, "mio-setup.md")):
        return env
    # scripts -> skill -> skills -> .claude -> progetto
    qui = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(qui, "..", "..", "..", ".."))


def leggi(percorso):
    valori, flag = {}, None
    with open(percorso, encoding="utf-8") as f:
        for riga in f:
            m = RE_FLAG.match(riga)
            if m:
                flag = m.group(1).strip().lower()
                continue
            m = RE_RIGA.match(riga)
            if m:
                val = m.group(2).strip().strip("`").strip()
                valori[m.group(1)] = val
    return valori, flag


def controlla(percorso):
    """Ritorna (stato, messaggi). stato: OK | INCOMPLETO | DA_CONFERMARE | MANCANTE"""
    if not os.path.isfile(percorso):
        return "MANCANTE", ["Il file mio-setup.md non esiste nella cartella del progetto."]
    valori, flag = leggi(percorso)
    problemi = []
    for chiave, valida, ammette_nessuno in CAMPI:
        val = valori.get(chiave)
        if val is None:
            problemi.append((chiave, "la riga manca dal file"))
            continue
        if val.lower() in VUOTO:
            problemi.append((chiave, "ancora da compilare"))
            continue
        if ammette_nessuno and val.lower() in NESSUNO:
            continue
        errore = valida(val)
        if errore:
            problemi.append((chiave, errore))
    if problemi:
        msg = ["Campi da sistemare: %d su %d." % (len(problemi), len(CAMPI)),
               "Prossimo campo: %s (%s)." % problemi[0]]
        if len(problemi) > 1:
            msg.append("Dopo: " + ", ".join(p[0] for p in problemi[1:6]) + (" ..." if len(problemi) > 6 else ""))
        return "INCOMPLETO", msg
    if flag not in ("sì", "si", "yes"):
        return "DA_CONFERMARE", ["Tutti i campi sono validi. Manca la conferma finale: "
                                 "mostra il riepilogo, chiedi l'OK e scrivi setup_completato: sì."]
    return "OK", ["Setup completo."]


def main():
    hook = "--hook" in sys.argv
    percorso = os.path.join(radice_progetto(), "mio-setup.md")
    stato, msg = controlla(percorso)
    if hook:
        if stato == "OK":
            return 0
        print("[Controllo setup] STATO: %s. %s" % (stato, " ".join(msg)))
        print("Regola del progetto: finche' il setup non e' OK si lavora SOLO sul setup guidato "
              "(skill meta-ads-guida-passo-passo, Passo 0, references/setup-guidato.md). "
              "Niente rinomina, niente campagne, anche se lo studente lo chiede: spiegagli il perche' in una riga.")
        return 0
    print(stato)
    for m in msg:
        print(m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
