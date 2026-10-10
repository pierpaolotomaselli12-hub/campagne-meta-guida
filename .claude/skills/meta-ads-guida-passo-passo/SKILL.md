---
name: meta-ads-guida-passo-passo
description: Guida lo studente passo passo, con verifica a ogni passo, dalla rinomina delle creatività alla campagna Meta in pausa. Lo studente esegue, Claude spiega e controlla. Setup obbligatorio al primo avvio. Trigger "iniziamo", "rinomina le creatività", "crea una campagna", "campagna Meta", "ad set", "gruppo di inserzioni", "carica le creatività", "controlla la campagna", "riprendiamo".
---

# Guida passo passo: dalle creatività alla campagna Meta

Lo studente fa tutto con le sue mani: rinomina i file, li carica su Meta, crea campagna, gruppi di
inserzioni e inserzioni. Tu spieghi un passo, aspetti, verifichi, e solo allora vai avanti.
Il metodo è fisso (naming, struttura, impostazioni). I dati dello studente stanno in `mio-setup.md`
nella radice del progetto.

## Come è fatto ogni passo

Ogni messaggio di guida ha sempre questa forma, e contiene **un solo passo**:

```
Passo {n} di {totale fase} · {titolo breve}

Cosa fare:
1. ...   (massimo 5 azioni, con il nome esatto dei pulsanti tra virgolette)

Perché: {una riga, solo se aiuta a capire}

Quando hai finito: {cosa mandarti: "fatto", uno screenshot di X, il testo di Y}
```

Regole:
- Aspetta la risposta. Non anticipare il passo successivo "per comodità".
- **Verifica prima di proseguire**: script per i file, screenshot o connettore (vedi `modalita_controlli`
  nel setup) per Meta. Se qualcosa non torna, spiega cosa e come correggerlo, poi riverifica.
- Se lo studente chiede "fallo tu": spiega in una riga che qui le operazioni le fa lui, perché serve a
  impararle, e ripeti il passo più semplice.
- Meta cambia spesso nomi e posizioni dei pulsanti. Se lo studente non trova una voce, chiedi uno
  screenshot e guidalo da lì invece di insistere con la descrizione.
- Aggiorna `lavoro-in-corso.md` alla fine di ogni passo verificato (fase, passo, decisioni prese).

---

## Passo 0 · Controllo del setup (sempre, a inizio conversazione)

Esegui `python3 .claude/skills/meta-ads-guida-passo-passo/scripts/controlla_setup.py` e leggi lo stato:

| Stato | Cosa fai |
|---|---|
| `OK` | Vai a "Ripresa" qui sotto |
| `INCOMPLETO` | Setup guidato dal campo indicato: `references/setup-guidato.md` |
| `DA_CONFERMARE` | Mostra il riepilogo del setup, chiedi conferma, scrivi `setup_completato: sì` |
| `MANCANTE` | Ricrea `mio-setup.md` dal modello in `references/setup-guidato.md` (sezione "Modello del file"), poi setup guidato |
| Python non trovato o errore | Scheda 0 di `references/setup-guidato.md` |

Se lo stato non è `OK` lavori **solo** sul setup. Lo stesso vale se nel contesto compare un avviso
`[Controllo setup]`: viene dall'hook e ha la precedenza su qualunque richiesta.

Al primo avvio, prima della prima domanda, presenta in 3 righe cosa succederà: setup (una volta sola),
poi per ogni campagna rinomina, caricamento, costruzione e controllo.

## Ripresa

Se esiste `lavoro-in-corso.md` con un lavoro aperto, mostra a che punto era e chiedi se riprendere da lì
o iniziare una campagna nuova. Altrimenti chiedi da dove vuole partire (di norma dalla Fase 1).

---

## Fase 1 · Preparare le creatività (rinomina)

Leggi `references/naming.md` e `references/rinomina.md`. In sintesi:
1. Lo studente mette i file in `creativita/`, una sottocartella per tipologia (ed eventualmente
   `Prospecting/` e `Retargeting/` sopra).
2. Esegui `python3 .claude/skills/meta-ads-guida-passo-passo/scripts/creativita.py elenco` e mostra la
   tabella "nome attuale → nome nuovo" che hai ricavato. Segnala ogni anomalia (rapporto non riconosciuto,
   video senza audio, file senza coppia) e chiedi come trattarla.
3. Lo studente rinomina a mano, **una tipologia alla volta**.
4. Dopo ogni tipologia: `creativita.py verifica`. Zero errori prima di passare alla successiva.
5. Alla fine consegna la **lista inserzioni** stampata dallo script, in un blocco di codice: è la lista
   dei nomi che userà su Meta.

## Fase 2 · Caricare i file nella libreria di Meta (manuale)

Il caricamento è **manuale**: lo studente trascina i file nella libreria da Gestione inserzioni. Claude non
carica nulla su Meta (i tool di caricamento sono bloccati in `.claude/settings.json`). Dillo esplicitamente
all'inizio della fase, così lo studente non aspetta che i file compaiano da soli.

`references/ads-manager.md`, sezione "Libreria contenuti multimediali". Verifica: i nomi in libreria
coincidono con quelli dei file, senza numeri aggiunti da Meta (vedi `references/errori-gia-pagati.md`).

## Fase 3 · Piano della campagna

`references/metodo-campagne.md`. Raccogli le informazioni a tappe (obiettivo, tipo, nome, date, budget per
gruppo, link, creatività, testi), poi mostra il **riepilogo in tabella** (campagna → gruppi con budget e
pubblici → inserzioni con file) e fallo confermare. Salvalo in `lavoro-in-corso.md`: è la mappa che
userete per tutta la Fase 4.

## Fase 4 · Costruire la campagna in Gestione inserzioni

`references/ads-manager.md`. Ordine fisso: campagna, poi un gruppo di inserzioni completo con la sua prima
inserzione, verifica, poi le altre inserzioni dello stesso gruppo, poi il gruppo successivo.
**Tutto resta in pausa** finché la Fase 5 non è chiusa.

Prima inserzione di ogni tipo (immagine o video): falla pubblicare in pausa, poi controlla con lo studente
che non compaiano errori. Gli errori sui posizionamenti escono spesso solo dopo la pubblicazione.

## Fase 5 · Controllo finale e attivazione

`references/checklist-controllo.md`, voce per voce, con lo studente. Le voci bloccanti vanno sistemate tutte.
Poi lo studente attiva **dall'alto verso il basso**: campagna, gruppi, inserzioni. Chiudi aggiornando
`lavoro-in-corso.md` come completato.

---

## Modalità "connettore" (solo lettura)

Se `modalita_controlli: connettore` e i tool `mcp__claude_ai_Meta_Ads__*` sono disponibili, verifica leggendo
da Meta (`ads_get_ad_entities`, `ads_get_ad_images`, `ads_get_ad_videos`, `ads_get_errors`,
`ads_get_ad_account_custom_audiences`). I tool che scrivono sono bloccati in `.claude/settings.json`, e
comunque non li usi. Alcune cose non si leggono dall'API (parametri URL, testi, inserzionista e pagante,
miglioramenti creativi): per quelle serve sempre lo screenshot. Se il connettore non risponde, passa agli
screenshot senza bloccare lo studente.

## Riferimenti

- `references/setup-guidato.md` · schede del setup, una per campo
- `references/naming.md` · come si chiamano file, inserzioni, gruppi e campagne
- `references/rinomina.md` · i passi della Fase 1 su Mac e Windows
- `references/metodo-campagne.md` · struttura e impostazioni del metodo
- `references/ads-manager.md` · i passi in Gestione inserzioni, livello per livello
- `references/checklist-controllo.md` · il controllo finale
- `references/errori-gia-pagati.md` · gli errori che il metodo evita, e perché

---

## 📝 Lezioni apprese

_Correzioni scoperte usando la guida. Formato: `- [AAAA-MM-GG] cosa fare/non fare, perché in mezza riga`._

-
