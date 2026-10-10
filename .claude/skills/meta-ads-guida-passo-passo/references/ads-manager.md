# Gestione inserzioni, i passi

I nomi dei pulsanti sono quelli dell'interfaccia italiana al momento della scrittura. Meta li cambia spesso:
se lo studente non trova una voce, chiedi uno screenshot e guidalo da quello che vede.
Ogni blocco qui sotto è **un passo**: un messaggio, poi la verifica indicata.

---

## A. Libreria contenuti multimediali (Fase 2, manuale)

Il caricamento lo fa lo studente a mano: Claude non può caricare file su Meta.

**A1 · Aprire la libreria**
Gestione inserzioni → menu "Tutti gli strumenti" (le nove linee in alto a sinistra) → "Contenuti multimediali".
Controlla in alto che l'account selezionato sia quello del setup.
Verifica: screenshot con il nome dell'account visibile.

**A2 · Caricare i file**
"Carica" → seleziona tutti i file di una fase (prima PROSPECTING, poi RETARGETING) → attendi la fine.
I video restano "in elaborazione" per qualche minuto.
Verifica: screenshot della libreria filtrata per i file caricati (connettore: `ads_get_ad_images` / `ads_get_ad_videos`).
Controlla che i nomi coincidano con quelli dei file. Se Meta ha aggiunto un numero in coda a un nome
(`..._10_2026_2`), esiste già un file con lo stesso nome: vedi `errori-gia-pagati.md`.

---

## B. Campagna (Fase 4)

**B1 · Nuova campagna**
Gestione inserzioni → scheda "Campagne" → "+ Crea" → obiettivo "Contatti" (Lead) o "Vendite" → "Continua".
Se Meta propone una configurazione "Advantage+" o "consigliata", scegli la **configurazione manuale**.

**B2 · Impostazioni della campagna**
- Nome campagna: quello confermato nel piano, copiato esatto.
- "Budget della campagna Advantage+": **disattivato** (il budget va sui gruppi).
- Lascia il resto com'è e vai avanti al gruppo di inserzioni.
Verifica: screenshot del pannello campagna (nome e budget di campagna spento).

---

## C. Gruppo di inserzioni

**C1 · Nome, conversione, pixel**
- Nome del gruppo come da piano (`naming.md`, sezione 4).
- "Luogo della conversione": Sito web.
- "Obiettivo di prestazioni": Massimizza il numero di conversioni.
- "Dataset" (pixel): quello del setup. "Evento di conversione": Lead o Acquisto.
Verifica: screenshot della sezione.

**C2 · Offerta e attribuzione**
- "Strategia di offerta": Volume più alto (nessun obiettivo di costo).
- Impostazione di attribuzione (spesso sotto "Mostra altre opzioni"): Lead = clic di 1 giorno e
  visualizzazione di 1 giorno · Vendite = clic di 7 giorni e visualizzazione di 1 giorno.
Verifica: screenshot.

**C3 · Budget e date**
- Budget giornaliero del piano per questo gruppo.
- Data di inizio e data di fine del piano.
Verifica: screenshot.

**C4 · Pubblico**
- Luoghi: i paesi del setup. Nessuna lingua.
- Prospecting: nessun pubblico personalizzato e nessun interesse, nemmeno come suggerimento.
- Retargeting: se compare "Pubblico Advantage+", passa alle **opzioni di pubblico originali** (o disattivalo),
  poi in "Pubblici personalizzati" aggiungi quelli del gruppo: `Visite al sito` da solo, oppure Engage Instagram
  + Engage Facebook insieme.
- Vendite: in "Escludi" aggiungi la lista clienti del setup.
Verifica: screenshot del riepilogo pubblico (connettore: `ads_get_ad_entities` livello adset, campo `targeting`).

**C5 · Posizionamenti**
"Posizionamenti Advantage+". Nessuna esclusione manuale.

**C6 · Trasparenza UE (inserzionista e pagante)**
Cerca la sezione su inserzionista/beneficiario e pagante (di solito in fondo al gruppo). Se è precompilata con
un nome diverso dal setup, correggila: inserzionista e pagante del setup.
Verifica: screenshot di questa sezione, sempre (non si legge dall'API).

---

## D. Inserzione

**D1 · Nome e identità**
- Nome: dalla lista inserzioni della Fase 1, copiato esatto.
- "Identità": Pagina Facebook e account Instagram del setup.

**D2 · Formato e contenuti**
- Formato: "Immagine o video singoli". Se c'è un'opzione "Formato flessibile" o "Raccolta", non usarla.
- "Configura contenuto multimediale" → scegli dalla libreria il file **story** (o `.jpg` / `+1`) e il file
  **feed** (o `.png` / originale).
- Nella schermata dei posizionamenti, assegna: file feed ai posizionamenti **Feed** (feed, esplora, ricerca,
  video in-stream), file story a **Storie e Reel**. Controlla l'anteprima: nessun quadrato nelle Storie,
  nessuna banda nera enorme.
Verifica: screenshot dell'anteprima con i due gruppi di posizionamenti visibili.

**D3 · Testi**
- "Testo principale": aggiungi le varianti approvate (fino a 5) con "Aggiungi opzione di testo".
- "Titolo": le varianti approvate (fino a 5).
- "Descrizione": vuota. Se Meta la riempie da sola con il testo della pagina, segnalalo.
- "Invito all'azione": quello del setup.

**D4 · Destinazione e parametri**
- "URL del sito web": il link del piano, **senza** `?utm_...` attaccato.
- "Parametri URL" (sezione monitoraggio, in fondo): incolla i parametri del setup.
- "Link visualizzato": vuoto.
Verifica: screenshot del campo "Parametri URL", sempre (non si legge dall'API).

**D5 · Miglioramenti e opzioni**
- "Miglioramenti delle creatività Advantage+": apri l'elenco e disattiva **tutto**.
- "Ottimizza il testo per persona" o simili: disattivato.
- "Inserzioni con più inserzionisti": attivo.
- Componenti aggiuntivi del browser: nessuno.
Verifica: screenshot dell'elenco miglioramenti aperto.

**D6 · Pubblicare in pausa**
Disattiva l'interruttore di campagna, gruppo e inserzione (o verifica che siano spenti), poi "Pubblica".
Dopo qualche minuto guarda la colonna "Consegna": nessun errore. Per la prima inserzione con immagini e la prima
con video, aspetta questo controllo prima di creare le altre.

**D7 · Le altre inserzioni del gruppo**
Crea ogni inserzione con "+ Crea" dentro il gruppo, ripetendo D1-D5: testi uguali, file e nome diversi.
Niente "Duplica": il metodo crea tutto da zero (perché in `errori-gia-pagati.md`).

---

## E. Attivazione (solo dopo la Fase 5)

Accendi nell'ordine: campagna → gruppi → inserzioni. Dall'alto verso il basso ogni livello parte solo quando
quello sopra è già acceso e controllato, e non c'è mai un pezzo che spende prima che il resto sia pronto.
