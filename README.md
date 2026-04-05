# 📚 Library Manager

Modulo Odoo 17 personalizzato per la gestione di libri e prestiti.  
Progetto portfolio sviluppato per dimostrare competenze Odoo a livello junior.

---

## Tech Stack

- **Odoo 17 / Python 3.11**
- ORM Odoo (modelli, relazioni, compute fields)
- XML Views (form, list, search)
- `mail.thread` per chatter e tracking

---

## Struttura

```
library_manager/
├── __manifest__.py
├── __init__.py
├── models/
│   ├── book.py            # library.book
│   └── loan.py            # library.loan
├── views/
│   ├── book_views.xml
│   ├── loan_views.xml
│   └── menu.xml
├── security/
│   └── ir.model.access.csv
└── data/
    └── demo_data.xml
```

---

## Modelli

### `library.book`

| Campo | Tipo | Note |
|---|---|---|
| `name` | `Char` | Titolo, required |
| `author` | `Char` | Autore, required |
| `isbn` | `Char` | Codice ISBN |
| `year` | `Integer` | Anno pubblicazione |
| `state` | `Selection` | `available` / `on_loan` |
| `loan_ids` | `One2many` | Prestiti del libro |
| `loan_count` | `Integer` | Compute da `loan_ids` |

### `library.loan`

| Campo | Tipo | Note |
|---|---|---|
| `book_id` | `Many2one` | Libro prestato |
| `borrower_id` | `Many2one` | Lettore (`res.partner`) |
| `loan_date` | `Date` | Data inizio |
| `return_date` | `Date` | Data restituzione |
| `state` | `Selection` | `active` / `returned` |
| `is_overdue` | `Boolean` | Compute: scaduto e non restituito |

---

## Concetti Odoo dimostrati

| Concetto | Dove |
|---|---|
| `_inherit = ['mail.thread']` | chatter + field tracking |
| `One2many` / `Many2one` | relazione libro ↔ prestiti |
| `@api.depends` + `compute` | `loan_count`, `is_overdue` |
| `@api.constrains` | validazione anno |
| `@api.model_create_multi` | override `create` con logica business |
| `widget="badge"` + `decoration-*` | righe e stati colorati nelle viste |
| Smart button (`oe_stat_button`) | contatore prestiti con navigazione |
| `widget="statusbar"` | progressione stato visiva |
| `ir.model.access.csv` | permessi CRUD sui modelli |

---

## Installazione

```bash
# Copia il modulo nella cartella addons, poi:
./odoo-bin -u library_manager -d nome_database
```

Oppure da interfaccia: **Impostazioni → Aggiorna lista app → cerca "Library Manager" → Installa**

---

## Utilizzo

- **Biblioteca → Libri** — anagrafica libri con stato disponibilità
- **Biblioteca → Prestiti** — gestione prestiti, righe rosse = in ritardo
- Bottone **"Restituisci"** sul prestito → chiude il prestito e libera il libro
- **Smart button** sul libro → mostra storico prestiti

---

## Autore

Sviluppato da **Zigna** come progetto portfolio Odoo 17.  
`versione: 17.0.1.0.0` · `licenza: LGPL-3` · `dipendenze: base, mail`

## 📄 License  
This project is licensed under the MIT License.
