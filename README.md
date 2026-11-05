# 📡 PopCulture Radar

Un assistente che **legge le notizie di cultura pop al posto vostro**, le raggruppa, le valuta con un punteggio da 0 a 10 e vi manda una notifica su Telegram (o Discord/Slack) quando ne esce una che vale la pena cavalcare **finché è ancora fresca**.

Costa **0 euro**: gira gratis su GitHub, usa modelli gratuiti (Google Gemini e/o Groq) e notifica con Telegram. Non devi installare nulla sul tuo computer e non servono competenze di programmazione.

Una notifica arriva così:

```
🔥 8.4/10 · 🎌 Anime · Trade
One Piece, confermata la data del nuovo arco: debutto nel 2027
💡 Annuncio ufficiale su un franchise di punta, ancora nessuna testata italiana.
✍️ Taglio: news breve + "cosa sappiamo finora" sull'arco
📰 1 fonte (Anime News Network) · nessuna testata italiana · ⏱ 12 min fa
📊 Impatto 9 · Pubblico 9 · Traffico 8
🔗 Anime News Network
```

> **Stato del collaudo.** Il codice è coperto da 58 test automatici e da una prova completa con rete simulata (feed, rating, notifiche, deduplica, riepilogo, salvataggio della memoria). Dall'ambiente in cui è stato scritto non era possibile collegarsi a Internet: **i feed reali e le API di Google, Groq e Telegram vanno quindi verificati da te** con i quattro controlli del Passo 5 (ci vogliono 5 minuti e sono pensati apposta).

---

## Cosa ti serve (tutto gratuito)

| Cosa | A cosa serve | Dove |
|---|---|---|
| Account **GitHub** | Fa girare il Radar ogni 20 minuti | github.com |
| Account **Telegram** | Riceve le notifiche | telegram.org |
| Account **Google** | Chiave gratuita per Gemini (il "cervello" che valuta) | aistudio.google.com |
| Account **Groq** *(consigliato)* | Seconda chiave gratuita: se Gemini finisce i limiti, usa questa | console.groq.com |

---

## Installazione (circa 25 minuti)

### Passo 1 · Crea il progetto su GitHub

1. Su GitHub clicca **New repository**. Chiamalo `popculture-radar`.
2. Scegli **Public** (consigliato: i minuti di esecuzione sono illimitati e gratuiti). Le tue chiavi **non** saranno visibili a nessuno: restano nei "Secrets" (Passo 4). Saranno visibili solo la lista delle fonti e il profilo della redazione. Se preferisci **Private** va bene lo stesso, ma leggi la nota sui minuti più sotto.
3. Nella pagina del repository clicca **Add file → Upload files** e trascina dentro **tutti i file di questa cartella tranne `.github`** (cioè `radar.py`, `demo.py`, `config.json`, `prompt_rating.md`, `profilo_redazione.md`, `README.md`, `.env.example`, `.gitignore`). Le cartelle `tests` e `workflow` sono facoltative: la seconda contiene solo una copia visibile del file del Passo 4, che ti serve da leggere. Poi **Commit changes**.
4. Ora il file di automazione, che sta in una cartella nascosta: clicca **Add file → Create new file**. Nel campo del nome scrivi esattamente `.github/workflows/radar.yml` (le barre creano le cartelle da sole). Apri il file `workflow/radar.yml` di questo pacchetto, copia tutto il contenuto, incollalo e clicca **Commit changes**.

> **Repository privato?** GitHub regala 2000 minuti al mese. Ogni esecuzione ne consuma circa 1: ogni 20 minuti sono ~2160 minuti, un po' sopra il limite. Nel file `radar.yml` cambia `*/20` in `*/30` e sei al sicuro (~1440 minuti).

### Passo 2 · Crea il bot Telegram

1. Su Telegram cerca **@BotFather**, scrivi `/newbot` e segui le istruzioni (nome e username a piacere).
2. BotFather ti risponde con un **token** lungo, tipo `123456:ABC-DEF...`. Copialo e tienilo da parte: è una password, non condividerlo.
3. **Dove vuoi ricevere le notifiche?** Consiglio un **gruppo** con tutta la redazione: crea un gruppo Telegram, aggiungi il bot come membro, poi scrivi nel gruppo `/start`. In alternativa, per ricevere solo tu le notifiche, apri una chat col bot e premi **Start**.

### Passo 3 · Prendi le chiavi gratuite dei modelli

- **Gemini**: vai su **aistudio.google.com/apikey**, accedi con Google, clicca **Create API key** e copiala.
- **Groq** *(consigliato)*: vai su **console.groq.com/keys**, crea un account e genera una chiave.

### Passo 4 · Inserisci le chiavi su GitHub (in modo sicuro)

Nel repository: **Settings → Secrets and variables → Actions → New repository secret**. Crea questi segreti (nome esatto, tutto maiuscolo):

| Nome | Valore |
|---|---|
| `TELEGRAM_BOT_TOKEN` | il token di BotFather |
| `GEMINI_API_KEY` | la chiave di Google AI Studio |
| `GROQ_API_KEY` | la chiave Groq *(facoltativa ma consigliata)* |
| `TELEGRAM_CHAT_ID` | l'ID della chat: lo scopri al Passo 5, quindi per ora salta |

*(Usi Discord o Slack al posto di Telegram? Crea invece `DISCORD_WEBHOOK_URL` oppure `SLACK_WEBHOOK_URL` con l'indirizzo del webhook del tuo canale, e salta il chat ID.)*

### Passo 5 · Collaudo in 5 controlli

Vai nella scheda **Actions** del repository (se GitHub chiede di abilitare i workflow, accetta). Scegli **PopCulture Radar** nella colonna a sinistra, poi **Run workflow**, seleziona la modalità e avvia. Quando la riga diventa verde, aprila e guarda la pagina **Summary**: c'è il risultato.

| Ordine | Modalità | Cosa verifica | Esito atteso |
|---|---|---|---|
| 1 | `chat-id` | Trova l'ID della tua chat Telegram | Mostra `TELEGRAM_CHAT_ID = -100123…`. **Copialo e crea il segreto `TELEGRAM_CHAT_ID`** (Passo 4). Se non trova nulla, scrivi `/start` al bot (o nel gruppo) e riprova |
| 2 | `check-llm` | Le chiavi Gemini/Groq funzionano | ✅ per ciascun modello |
| 3 | `check-sources` | Quali feed rispondono davvero | Tabella con ✅ e ❌ per ogni fonte (provate anche quelle disattivate) |
| 4 | `test-notify` | Telegram riceve il messaggio | Arriva "Messaggio di prova: il Radar funziona" |
| 5 | `dry-run` | Prova vera con le notizie di adesso, **senza** inviare né salvare | Nel log vedi le notifiche che sarebbero partite |

Se una fonte è ❌ nel controllo 3, aprila nel browser: spesso basta correggere l'indirizzo del feed in `config.json`, oppure spegnerla con `"enabled": false`. Quelle già disattivate in `config.json` (Reddit, Everyeye, Multiplayer.it, Movieplayer, AnimeClick) sono **indirizzi da verificare**: se nel controllo risultano ✅, mettile a `true`.

### Passo 6 · Accendi

Lancia **Run workflow → `run`** una volta. Il Radar manda "✅ PopCulture Radar attivo" e da lì parte da solo ogni ~20 minuti (GitHub può ritardare di qualche minuto: è normale). Alle 20:00 arriva il riepilogo del giorno.

> **Importante:** nei repository pubblici GitHub **sospende le automazioni dopo 60 giorni senza attività**. Se un giorno le notifiche si fermano, apri **Actions** e clicca **Enable workflow**.

---

## Come ragiona il Radar

1. **Raccoglie** i feed delle fonti (inglesi e italiane) ogni ~20 minuti.
2. **Scarta il rumore**: offerte, recensioni, guide, oroscopi (lista modificabile in `config.json`), articoli più vecchi di 8 ore, cose già viste.
3. **Raggruppa** gli articoli che parlano dello stesso evento, anche tra lingue diverse, per non mandarti 10 notifiche per un trailer.
4. **Fa valutare** ogni notizia dall'LLM: impatto, interesse per il vostro pubblico, potenziale di traffico, affidabilità (ufficiale / trade / stampa / rumor / opinione) e propone titolo, motivo e taglio.
5. **Calcola il punteggio** con una formula trasparente, che tiene conto di quello che l'LLM non può sapere:

```
punteggio = (impatto×0.45 + pubblico×0.35 + traffico×0.20)
            × affidabilità × freschezza × saturazione × copertura italiana
```

| Fattore | Come funziona |
|---|---|
| Affidabilità | ufficiale ×1.0 · trade ×0.95 · stampa ×0.85 · rumor ×0.75 · opinione ×0.4 |
| Freschezza | entro 1 h ×1.0 → dopo 12 h ×0.5 |
| Saturazione | 1 fonte ×1.0 · 2 ×0.95 · 3-4 ×0.85 · 5-7 ×0.7 · 8+ ×0.55 |
| Copertura italiana | nessuna testata italiana ×1.0 · una ×0.85 · due o più ×0.65 |

   È il cuore del "cavalcare l'onda": una notizia che hanno già dato in dieci, anche in italiano, scende di punteggio da sola. Ogni notifica riporta in fondo i fattori applicati, così capisci sempre perché ha preso quel voto.

6. **Notifica**: punteggio ≥ 7 → messaggio subito (massimo 5 per esecuzione). Tra 5 e 7 → finisce nel **riepilogo serale**. Impatto ≥ 9 con fonte ufficiale o trade → notifica sempre (morti, cancellazioni, annunci enormi). Di notte (00:30-07:30) i messaggi arrivano **in silenzio**, tranne quelli da 9 in su.
7. **Non ti disturba due volte**: ricorda le notizie degli ultimi 3 giorni. Se aggiungi il feed del vostro sito (vedi sotto), non vi segnala ciò che avete già pubblicato.

---

## Personalizzarlo (le due cose da fare nella prima settimana)

### 1. Il profilo della redazione: `profilo_redazione.md`
È il file che rende il Radar "vostro". Dentro ci sono **esempi generici** di franchise prioritari, da ignorare, cosa vi piace cavalcare. Aprilo su GitHub (matita ✏️ in alto a destra), sostituisci con le vostre priorità, **Commit changes**. Vale dalla prossima esecuzione. Scrivi anche il nome della testata al posto di `[NOME DELLA TESTATA]`.

> Privacy: i modelli gratuiti possono usare i testi inviati per migliorare i loro prodotti. Nel profilo metti le linee editoriali, **non** informazioni riservate.

### 2. Le soglie e le fonti: `config.json`
- `thresholds.notify` (7.0): **alzalo (7.5-8)** se ricevi troppe notifiche, **abbassalo (6-6.5)** se ne ricevi poche.
- `digest.hour` (20): l'ora del riepilogo serale.
- `quiet_hours`: la fascia notturna silenziosa.
- `sources`: per **aggiungere una fonte** copia una riga esistente e cambia nome e indirizzo. Per quasi ogni sito WordPress il feed è `https://sito.it/feed/`. Per **spegnerne** una metti `"enabled": false`.
- **Il feed del vostro sito**: nella riga `LA NOSTRA TESTATA` metti l'indirizzo del vostro feed e `"enabled": true`.

Il file è un JSON: se sbagli una virgola il Radar si ferma con un messaggio che indica la riga. Puoi controllarlo incollandolo su **jsonlint.com**.

**Calibrazione consigliata:** per i primi 2-3 giorni tieni d'occhio il riepilogo serale. Se vedi lì notizie che avresti voluto subito, abbassa la soglia; se ricevi notifiche inutili, alzala o precisa meglio il profilo.

---

## Costi e limiti, onestamente

- **Costo: 0 €.** GitHub, Telegram e i piani gratuiti di Google AI Studio e Groq non richiedono carta di credito (controlla al momento dell'iscrizione: le condizioni possono cambiare).
- **Limiti dei modelli gratuiti**: Google e Groq cambiano spesso quote e nomi dei modelli. Il Radar fa poche richieste (di solito 1-2 per esecuzione, e solo quando ci sono novità), rileva da solo il nome del modello disponibile e, se Gemini finisce i limiti, passa a Groq. Per questo conviene configurarli entrambi.
- **Non è tempo reale**: tra una notizia e la notifica passano in media 10-30 minuti (cron di GitHub + frequenza dei feed). Per cavalcare l'onda basta; per i "primi in assoluto" no.
- **Solo fonti con feed**: niente X/Twitter (non è gratuito). Reddit è incluso ma disattivato, perché spesso blocca i server di GitHub.
- **Il raggruppamento è prudente**: preferisce un doppione a una notizia nascosta per errore. Capiterà ogni tanto di ricevere due notifiche sullo stesso evento.
- **Le valutazioni sono suggerimenti**: l'LLM può sbagliare. Verifica sempre la fonte prima di pubblicare, e usa le notizie come spunto: non copiare gli articoli altrui, scrivi i vostri.
- Se il servizio di notifica non è raggiungibile, i messaggi vengono ritentati per qualche ora.

---

## Se qualcosa non va

| Sintomo | Causa probabile e soluzione |
|---|---|
| Nessuna notifica | Lancia `test-notify`. Se non arriva: controlla `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`; il bot deve essere nel gruppo |
| `chat-id` non trova nulla | Scrivi `/start` al bot (o nel gruppo, dopo averlo aggiunto) e rilancia entro 24 ore |
| Il run diventa rosso con "nessuna chiave LLM" | Manca il segreto `GEMINI_API_KEY` (o `GROQ_API_KEY`), oppure ha un nome sbagliato |
| `check-llm` dà ❌ "chiave non valida" | Rigenera la chiave e aggiorna il segreto, senza spazi o virgolette |
| `check-llm` dà ❌ "limite raggiunto" | Quota giornaliera finita: si risolve da sola, meglio aggiungere la seconda chiave |
| Troppe notifiche | Alza `thresholds.notify`, o precisa il profilo: aggiungi cosa ignorare |
| Troppo poche | Abbassa `thresholds.notify`; controlla con `check-sources` che i feed funzionino |
| Una fonte non risponde | Il riepilogo serale te lo segnala dopo qualche ora. Apri il feed nel browser: se l'indirizzo è cambiato, aggiornalo in `config.json` |
| Si sono fermate le automazioni | Dopo 60 giorni di inattività (repo pubblico): Actions → Enable workflow |
| `config.json non è valido` | Manca o avanza una virgola: il messaggio indica la riga |

**Per fermarlo:** Actions → PopCulture Radar → menu `…` → **Disable workflow**.

---

## Provarlo sul tuo computer (facoltativo)

Serve Python 3.9 o successivo. Nessuna libreria da installare. Sui comandi qui sotto usa `python3` su Mac/Linux e `python` su Windows.

```bash
python radar.py --demo            # prova offline con notizie finte: vedi subito come ragiona
python radar.py --check-sources   # quali feed rispondono
python radar.py --dry-run         # prova vera, senza inviare nulla
python -m unittest discover -s tests   # i test automatici
```

Per le prove con chiavi vere copia `.env.example` in `.env` e compila i valori (il file `.env` non viene mai caricato su GitHub).

---

## I file

| File | A cosa serve | Lo modifichi? |
|---|---|---|
| `profilo_redazione.md` | Le priorità della vostra redazione | **Sì, spesso** |
| `config.json` | Fonti, soglie, orari, pesi del punteggio | Sì |
| `prompt_rating.md` | Le istruzioni di valutazione date all'LLM | Raramente |
| `radar.py` | Il programma | No |
| `demo.py` | Dati finti per la prova offline | No |
| `.github/workflows/radar.yml` | L'automazione ogni 20 minuti | Solo la frequenza |
| `tests/` | Test automatici | No |

La "memoria" del Radar (notizie già viste) vive sul branch `radar-state` del repository: non toccarlo. Se vuoi azzerarla, eliminalo da GitHub e al giro successivo ricomincia da capo.
