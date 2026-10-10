#!/bin/sh
# Lanciato dagli hook in .claude/settings.json a inizio sessione e a ogni messaggio.
# Se il setup non e' completo, stampa un avviso che Claude riceve nel contesto.
# Se Python manca, lo dice invece di fallire in silenzio.

DIR="$(cd "$(dirname "$0")" && pwd)"
PY=""

for c in /opt/homebrew/bin/python3 /usr/local/bin/python3 /Library/Frameworks/Python.framework/Versions/Current/bin/python3; do
  if [ -x "$c" ]; then PY="$c"; break; fi
done

if [ -z "$PY" ]; then
  if [ "$(uname)" = "Darwin" ]; then
    # Su Mac /usr/bin/python3 esiste sempre, ma funziona solo con gli strumenti da riga di comando installati
    if xcode-select -p >/dev/null 2>&1 && [ -x /usr/bin/python3 ]; then PY="/usr/bin/python3"; fi
  else
    for c in python3 python; do
      if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)" >/dev/null 2>&1; then
        PY="$c"; break
      fi
    done
  fi
fi

if [ -z "$PY" ]; then
  echo "[Controllo setup] STATO: PYTHON_MANCANTE. Python 3 non e' installato su questo computer e serve agli script della guida."
  echo "Regola del progetto: prima di tutto guida lo studente all'installazione (references/setup-guidato.md, scheda 0). Niente rinomina, niente campagne finche' non e' risolto."
  exit 0
fi

exec "$PY" "$DIR/controlla_setup.py" --hook
