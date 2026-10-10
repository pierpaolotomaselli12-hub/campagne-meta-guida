# Naming: file, inserzioni, gruppi, campagne

Nomi coerenti servono a tre cose: trovare il file giusto in libreria, leggere i report senza aprire ogni
inserzione, e far tornare i conti nei parametri URL.

## 1. File delle creatività

```
{FASE_}{Tipologia}_{n}_{feed|story}_{MM}_{AAAA}.{estensione}
```

| Pezzo | Regola | Esempio |
|---|---|---|
| `FASE_` | Solo se il lotto è diviso in cartelle `Prospecting/` e `Retargeting/`: `PROSPECTING_` o `RETARGETING_`, maiuscolo, in testa | `PROSPECTING_` |
| `Tipologia` | Dal nome della cartella. Iniziale maiuscola per ogni parola, `_` al posto degli spazi, via emoji e numeri iniziali (`01_note` → `Note`, `video long` → `Video_Long`) | `Tweet` |
| `n` | Numero progressivo della creatività, da 1, per tipologia (e per fase). Feed e Story della stessa creatività hanno **lo stesso numero** | `3` |
| `feed` / `story` | Dal rapporto reale del file, mai dal nome originale: 1:1 o 4:5 = feed, 9:16 = story | `story` |
| `MM_AAAA` | Mese e anno della campagna (non per forza quello di oggi: se il lotto è per il mese prossimo, vale quello) | `10_2026` |

Se il nome originale descrive l'angolo della creatività (`non-fa-per-me`, `otto-ore-seduta`), si può tenere al
posto di `{Tipologia}_{n}`: `PROSPECTING_non-fa-per-me_story_10_2026.mp4`. Nei report si legge meglio di un numero.

## 2. Servono sempre due file per creatività

Ogni inserzione usa due file distinti: uno va sui posizionamenti Feed, l'altro su Storie e Reel.

| Cosa hai | Cosa fai | Esempio |
|---|---|---|
| Feed + Story | Niente di speciale | `Tweet_1_feed_10_2026.png` + `Tweet_1_story_10_2026.png` |
| Solo un'immagine verticale | Salvala anche nell'altro formato (PNG + JPG) con lo stesso nome | `Tweet_2_story_10_2026.png` + `Tweet_2_story_10_2026.jpg` |
| Solo un video verticale | Duplicalo e aggiungi `+1` in fondo, prima dell'estensione | `Video_1_story_10_2026.mp4` + `Video_1_story_10_2026+1.mp4` |

Mai ritagliare un verticale in quadrato e mai mettere un quadrato sulle Storie: il verticale si può usare
ovunque, il quadrato nelle Storie esce con bande enormi.

## 3. Inserzioni

Il nome dell'inserzione è il nome del file **senza** `feed`/`story`, senza `+1` e senza estensione.
Il prefisso di fase resta.

```
PROSPECTING_Tweet_1_feed_10_2026.png  ┐
PROSPECTING_Tweet_1_story_10_2026.png ┘→ inserzione  PROSPECTING_Tweet_1_10_2026
```

Lo script `creativita.py verifica` stampa la lista esatta: si copia da lì, non si riscrive a mano.

## 4. Gruppi di inserzioni

| Tipo campagna | Nome gruppo | Esempio |
|---|---|---|
| Prospecting | `Broad \| {Paese} \| {Tipologia}` | `Broad \| IT \| Tweet` |
| Retargeting | `{Pubblico} - {Tipologia}` | `Visite al sito - Tweet`, `Engage social - Tweet` |

Nel nome del gruppo la tipologia va con gli spazi (`Video Long`), come la leggerebbe una persona.

## 5. Campagne

Tutto in maiuscolo:

```
{PREFISSO}{PROSPECTING|RETARGETING} | {ACQUISIZIONE|VENDITA} {BRAND} {LEAD MAGNET o PRODOTTO} | {MESE} '{AA}
```

- `ACQUISIZIONE` per raccogliere contatti, `VENDITA` per vendere.
- Lead magnet o prodotto: il nome esatto, chiesto allo studente, mai inventato.
- Mese per esteso in italiano: `OTTOBRE '26`.

Esempi con dati di fantasia:
- `PROSPECTING | ACQUISIZIONE BRAND DEMO GUIDA GRATUITA | OTTOBRE '26`
- `[MR] RETARGETING | VENDITA BRAND DEMO CORSO BASE | NOVEMBRE '26`
