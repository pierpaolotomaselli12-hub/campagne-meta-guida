# Setup guidato

Si fa una volta sola. Una scheda per messaggio, nell'ordine qui sotto (è lo stesso ordine dello script).
Per ogni scheda:

1. Spiega cosa serve e dove trovarlo (le righe "Dove" e "Come deve essere").
2. Aspetta la risposta dello studente. Se manda uno screenshot, leggi tu il valore e fattelo confermare.
3. Controlla il formato. Se è sbagliato, spiega l'errore tipico e richiedi.
4. Scrivi il valore in `mio-setup.md` (radice del progetto), al posto di `___`.
5. Riesegui `controlla_setup.py` e passa al campo che indica.

Se lo studente non trova un dato, non bloccarlo a lungo: chiedi uno screenshot della schermata in cui si
trova e guidalo da lì. Mai inventare o "stimare" un valore.

---

## Scheda 0 · Python (solo se manca)

Gli script della guida usano Python 3.

- **Mac**: fai aprire l'app Terminale e scrivere `xcode-select --install`, poi premere Invio. Si apre una
  finestra di Apple: "Installa", accetta la licenza, attendi la fine (qualche minuto). Poi chiudi e riapri
  la conversazione.
- **Windows**: fai scaricare Python da python.org (pulsante "Download Python"), e durante l'installazione
  spuntare **"Add python.exe to PATH"**. Poi chiudi e riapri l'app Claude.

Verifica: rilancia `controlla_setup.py`. Se risponde, Python c'è.

## Scheda 1 · `modalita_controlli`

- **Cosa**: come verifico il tuo lavoro su Meta.
- **Opzioni**: `screenshot` (mi mandi le schermate, funziona sempre) oppure `connettore` (leggo io da Meta in
  sola lettura; serve il connettore Meta Ads collegato al tuo account Claude, da claude.ai → Impostazioni →
  Connettori).
- **Verifica**: se sceglie `connettore`, prova a leggere i suoi account pubblicitari. Se non funziona, scrivi
  `screenshot` e spiega che può cambiarlo in seguito.

## Scheda 2 · `nome_brand`

- **Cosa**: il nome del brand che pubblicizzi, come vuoi che compaia nel nome delle campagne.
- **Come deve essere**: testo libero. Andrà in maiuscolo nel nome campagna.

## Scheda 3 · `nome_account_pubblicitario`

- **Dove**: Gestione inserzioni (adsmanager.facebook.com), menu a tendina in alto a sinistra: il nome
  dell'account selezionato.
- **Errore tipico**: scrivere il nome del Business Manager o della Pagina invece di quello dell'account.

## Scheda 4 · `id_account_pubblicitario`

- **Dove**: stesso menu a tendina, il numero sotto il nome. Oppure nell'indirizzo del browser, dopo `act=`.
- **Come deve essere**: solo numeri. Se inizia con `act_`, togli quella parte.
- **Errore tipico**: copiare l'ID del Business Manager (si trova in Impostazioni dell'azienda, è un altro numero).

## Scheda 5 · `valuta`

- **Dove**: Gestione inserzioni → menu dell'account → "Impostazioni dell'account pubblicitario" → valuta.
- **Come deve essere**: codice di 3 lettere maiuscole (EUR, USD, CHF).
- **Perché**: i budget che inserirai sono in questa valuta, e non si cambia dopo.

## Scheda 6 · `nome_pixel`

- **Dove**: Gestione eventi (business.facebook.com/events_manager) → "Origini dei dati": l'elenco dei
  dataset/pixel. Quello giusto è collegato al sito su cui atterra la campagna.
- **Errore tipico**: se ce ne sono più di uno, scegliere quello sbagliato. Chiedi su quale sito è installato.

## Scheda 7 · `id_pixel`

- **Dove**: stessa schermata, il numero "ID" sotto il nome del pixel.
- **Come deve essere**: solo numeri.

## Scheda 8 · `pagina_facebook`

- **Dove**: la Pagina con cui pubblicherai le inserzioni (in Gestione inserzioni, livello inserzione, sezione
  "Identità"). Se non è sicuro, fagli aprire business.facebook.com → Impostazioni → Account → Pagine.
- **Come deve essere**: il nome esatto della Pagina.

## Scheda 9 · `account_instagram`

- **Dove**: Impostazioni dell'azienda → Account → Account Instagram.
- **Come deve essere**: il nome utente, senza @. Se non c'è un profilo Instagram collegato, scrivi `nessuno`
  e spiega che le inserzioni su Instagram usciranno comunque, a nome della Pagina Facebook.

## Scheda 10 · `inserzionista`

- **Cosa**: per le inserzioni che raggiungono persone nell'Unione Europea, Meta mostra pubblicamente chi è
  l'inserzionista (il brand che fa pubblicità) e chi paga. Restano visibili un anno nella Libreria inserzioni.
- **Come deve essere**: il nome del brand o della persona per cui fai pubblicità.
- **Avviso da dare subito**: Meta spesso precompila questi campi con la ragione sociale dell'azienda che
  gestisce il Business Manager (per esempio l'agenzia). È sbagliato, e va corretto su ogni gruppo di inserzioni.

## Scheda 11 · `pagante`

- **Cosa**: chi paga le inserzioni. Spesso coincide con l'inserzionista: chiedi se è così.

## Scheda 12 · `paesi_target`

- **Cosa**: i paesi in cui mostrare le inserzioni.
- **Come deve essere**: codici di 2 lettere maiuscole, separati da virgola (IT oppure IT, CH).

## Scheda 13 · `prefisso_campagne`

- **Cosa**: una sigla davanti al nome delle campagne, utile se sull'account lavorano più persone
  (es. `[MR] `). Facoltativo: `nessuno` va bene.

## Scheda 14 · `pubblico_visite_sito`

- **Dove**: Gestione inserzioni → menu "Tutti gli strumenti" → "Pubblici". Cerca un pubblico personalizzato
  di tipo "Sito web" (di solito "tutti i visitatori", 180 giorni).
- **Come deve essere**: il nome esatto, come compare nell'elenco.
- **Se non c'è**: scrivi `nessuno` e spiega che senza questo pubblico la campagna di retargeting sulle visite
  al sito non si può fare. Se vuole, guidalo a crearlo: "Crea pubblico" → "Pubblico personalizzato" →
  "Sito web" → pixel della scheda 6 → "Tutti i visitatori del sito web" → 180 giorni → nome chiaro → "Crea".

## Scheda 15 · `pubblico_engage_instagram`

- **Dove**: stesso elenco, pubblico personalizzato di tipo "Account Instagram" (chi ha interagito col profilo,
  di solito 365 giorni).
- **Se non c'è**: come sopra, oppure crealo: "Pubblico personalizzato" → "Instagram" → "Tutte le persone che
  hanno interagito con questo account professionale" → 365 giorni.

## Scheda 16 · `pubblico_engage_facebook`

- **Dove**: stesso elenco, tipo "Pagina Facebook" (chi ha interagito con la Pagina, 365 giorni).
- **Se non c'è**: "Pubblico personalizzato" → "Pagina Facebook" → "Tutte le persone che hanno interagito con
  la tua Pagina" → 365 giorni.

## Scheda 17 · `lista_clienti_esclusione`

- **Cosa**: un pubblico con chi ha già comprato, da escludere nelle campagne di vendita.
- **Dove**: stesso elenco, tipo "Lista clienti".
- **Se non c'è**: `nessuna`. Spiega che nelle campagne di vendita si mostrerà l'offerta anche a chi l'ha già
  comprata, e che si può aggiungere in seguito.

## Scheda 18 · `tipologie_creative`

- **Cosa**: le famiglie di creatività che usa di solito, una per stile grafico (es. Tweet, Note, Promemoria,
  Video_Short, Video_Long, Fake_Story). Ogni tipologia diventerà un gruppo di inserzioni.
- **Come deve essere**: elenco separato da virgole, ogni parola con l'iniziale maiuscola, `_` al posto degli
  spazi. È un punto di partenza: ogni campagna può usarne solo alcune.

## Scheda 19 · `risoluzioni_feed`

- **Cosa**: le dimensioni in pixel delle creatività quadrate o verticali 4:5.
- **Come deve essere**: `larghezza x altezza`, separate da virgola. Proponi `1080x1080, 1080x1350` e chiedi
  se il grafico consegna queste.

## Scheda 20 · `risoluzioni_story`

- **Cosa**: le dimensioni delle creatività verticali 9:16 (Storie e Reel).
- **Come deve essere**: proponi `1080x1920`. Aggiungi le altre se il grafico consegna anche 1440x2560 o
  2160x3840.

## Scheda 21 · `parametri_url`

- **Cosa**: i parametri che dicono al tuo sito e a Google Analytics da quale campagna, gruppo e inserzione
  arriva ogni visita. Le parti tra `{{ }}` le riempie Meta da solo.
- **Già compilato** con il valore del metodo. Spiegalo in due righe e chiedi se lo tiene così.

## Scheda 22 · `invito_all_azione`

- **Cosa**: il pulsante dell'inserzione. **Già compilato** con "Scopri di più". Chiedi se lo tiene.

---

## Conferma finale

Quando lo script risponde `DA_CONFERMARE`: mostra tutti i valori in una tabella, chiedi allo studente di
ricontrollarli uno per uno, poi scrivi `setup_completato: sì` e rilancia lo script. Con `OK` il setup è
chiuso: spiega che potrà correggere un dato in qualsiasi momento chiedendolo.

---

## Modello del file (se `mio-setup.md` manca)

Ricrealo nella radice del progetto con questo contenuto, poi riparti dalla scheda 1.

```
# Il mio setup

setup_completato: no

## 1. Come controlliamo il lavoro
- modalita_controlli: ___

## 2. Account e brand
- nome_brand: ___
- nome_account_pubblicitario: ___
- id_account_pubblicitario: ___
- valuta: ___
- nome_pixel: ___
- id_pixel: ___
- pagina_facebook: ___
- account_instagram: ___

## 3. Trasparenza UE
- inserzionista: ___
- pagante: ___

## 4. Dove e come si chiamano le campagne
- paesi_target: ___
- prefisso_campagne: ___

## 5. Pubblici
- pubblico_visite_sito: ___
- pubblico_engage_instagram: ___
- pubblico_engage_facebook: ___
- lista_clienti_esclusione: ___

## 6. Creatività
- tipologie_creative: ___
- risoluzioni_feed: ___
- risoluzioni_story: ___

## 7. Inserzioni
- parametri_url: utm_source=social-adv&utm_medium={{placement}}&utm_campaign={{campaign.name}}&utm_content={{adset.name}}-{{ad.name}}
- invito_all_azione: Scopri di più
```
