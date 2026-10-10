# Fase 1 · Rinomina, i passi

Regole dei nomi in `naming.md`. Qui ci sono i passi da dare allo studente, uno per messaggio.

## Passo 1 · Mettere i file al posto giusto

Lo studente apre la cartella del progetto (`Campagne-Meta`) e dentro `creativita/` crea una sottocartella per
ogni tipologia del lotto (`tweet`, `note`, `video short`...), poi ci trascina i file.
Se il lotto ha creatività diverse per pubblico freddo e caldo, sopra le tipologie crea `Prospecting/` e
`Retargeting/`.

Se i file arrivano in uno zip: doppio clic per estrarlo (Windows: tasto destro → "Estrai tutto"), poi sposta
il contenuto.

**Verifica**: `creativita.py elenco`. Ogni file deve avere una tipologia. Se un file sta fuori da una
sottocartella, fallo spostare.

## Passo 2 · La tabella dei nomi nuovi

Dall'output di `elenco` costruisci la tabella `nome attuale → nome nuovo`, una tipologia per volta.
Coppie Feed + Story: stesso numero. L'ordine dei file originali non dice nulla su quale sia Feed o Story:
decide solo la risoluzione.

Prima di mostrarla, segnala:
- file con rapporto non riconosciuto (né 1:1, 4:5 o 9:16): chiedi cosa sono, non indovinare
- risoluzioni diverse da quelle del setup: chiedi se è giusto così
- video senza traccia audio: segnalalo sempre, può essere voluto o un errore di esportazione
- creatività senza secondo file: spiega cosa fare (passo 4)
- file doppi del browser (`nome (1).jpg`): chiedi se sono copie da scartare

## Passo 3 · Rinominare (una tipologia alla volta)

- **Mac**: clic sul file, poi Invio, scrivi il nuovo nome, Invio. Se il Finder chiede "Mantieni .png" o simili,
  l'estensione deve restare quella originale.
- **Windows**: clic sul file, poi F2, scrivi il nuovo nome, Invio. Se le estensioni non si vedono: Esplora file
  → "Visualizza" → "Mostra" → "Estensioni nomi file".

**Verifica**: `creativita.py verifica`. Gli errori della tipologia appena fatta vanno corretti prima di passare
alla successiva. Quando il nome è sbagliato, mostra il nome atteso esatto, così lo studente lo copia.

## Passo 4 · Il secondo file, quando manca

- **Immagine solo verticale**:
  - Mac: apri con Anteprima → "File" → "Esporta" → Formato JPEG (se l'originale è PNG) o PNG (se è JPG) →
    stesso nome → "Salva".
  - Windows: apri con Paint → "File" → "Salva con nome" → l'altro formato → stesso nome.
- **Video solo verticale**:
  - Mac: tasto destro → "Duplica", poi rinomina la copia togliendo " copia" e aggiungendo `+1` prima di `.mp4`.
  - Windows: copia e incolla nella stessa cartella, poi rinomina togliendo " - Copia" e aggiungendo `+1`.

**Verifica**: `creativita.py verifica`.

## Passo 5 · Lista inserzioni

Con zero errori, copia in un blocco di codice la "LISTA INSERZIONI" stampata dallo script, divisa per fase e
tipologia. È la lista che lo studente userà per nominare le inserzioni. Scrivila anche in `lavoro-in-corso.md`.
