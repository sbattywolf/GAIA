# Runbook di modellazione Home Assistant

## Obiettivo

Preparare Home Assistant affinché Assist e Zeus possano trovare solo target utili usando aree, nomi, alias, label ed esposizione controllata.

## Regola 1: area fisica

Ogni device controllabile deve avere un'area coerente. Se un'entità ha un'area esplicita differente dal device, documentare perché. Non assegnare automaticamente dispositivi tecnici a un'area solo per farli comparire.

## Regola 2: nomi canonici

Schema consigliato per nomi visibili:

`<Area> <funzione o oggetto> [qualificatore]`

Esempi:

- `Ufficio luce soffitto`
- `Ufficio luce scrivania`
- `Camera da letto luce soffitto`
- `Corridoio luce soffitto`
- `Ingresso luce soffitto`
- `Soggiorno finestra destra`

Non rinominare in massa gli `entity_id` oggi. Prima correggere friendly name e alias; gli entity ID possono avere dipendenze in automazioni.

## Regola 3: alias naturali

Aggiungere solo espressioni realmente usate:

### Camera da letto

- luce camera
- luce camera da letto
- luce soffitto camera
- luce tetto camera

### Ufficio

- luce ufficio
- luce tetto ufficio
- luce soffitto ufficio
- luce scrivania

### Corridoio

- luce corridoio
- luce tetto corridoio
- luce soffitto corridoio

### Ingresso

- luce ingresso
- luce tetto ingresso
- luce soffitto ingresso

Per le aree, aggiungere alias solo se non crea collisioni. Valutare `camera` come alias di `Camera da letto`. Verificare con attenzione la coesistenza di `Office` e `Ufficio`.

## Regola 4: label con namespace

Creare una tassonomia piccola:

### Capability

- `zeus_cap_lighting`
- `zeus_cap_opening`
- `zeus_cap_presence`
- `zeus_cap_climate`
- `zeus_cap_media`

### Policy

- `zeus_control_allowed`
- `zeus_read_only`
- `zeus_exclude`
- `zeus_confirm_required`

### Technology, solo se utile

- `zeus_wall_switch`
- `zeus_smart_bulb`

Evitare una label generica `zeus_exception`: non spiega la policy. Preferire label positive e comprensibili.

## Applicazione iniziale consigliata

### Wall switch che rappresentano illuminazione

Applicare `zeus_cap_lighting` e, dopo verifica, `zeus_control_allowed` a:

- wall switch ufficio
- wall switch camera da letto
- wall switch cucina

Per corridoio, ingresso, spot 1 e spot 2, applicare `zeus_cap_lighting`, ma prima decidere se il target logico deve essere uno script/gruppo che preserva il comportamento del bulbo smart. Non comandare simultaneamente relay e bulbo senza policy.

### Luci utente

Applicare `zeus_cap_lighting` solo alle entità che l'utente considera una luce controllabile. Per i gruppi, scegliere se il gruppo è il target canonico. Se sì, marcare le entità figlie come non target generico per evitare duplicati.

### Esclusioni

Applicare `zeus_exclude` a:

- LED indicator/status
- RGB GPU/motherboard
- segmenti tecnici TV backlight, se non devono essere controllati con "luci"
- entità di configurazione Adaptive Lighting
- power outage memory, flip indicator, child lock

Non assumere che una label sul device o area si propaghi alle entità. Verificare e leggere i tre livelli nell'inventory provider.

## Regola 5: esposizione Assist

Esporre solo target canonici e utili. Non esporre ogni entità diagnostica. Preferire gruppi, script o entità logiche quando rappresentano l'intenzione meglio delle entità fisiche.

## Procedura area per area

Per ogni area:

1. Elencare device ed entità.
2. Identificare la capability umana: illuminazione, apertura, presenza, climate.
3. Scegliere un target canonico per ogni comando generico.
4. Aggiungere friendly name e alias.
5. Applicare label capability e policy.
6. Decidere esposizione Assist.
7. Testare in Developer Tools > Assist.
8. Testare con Zeus in read-only.
9. Testare un'azione reversibile.
10. Registrare risultato in `config/entity_capability_catalog.example.yaml` copiato in un file locale non segreto.

## Ordine raccomandato

1. Ufficio
2. Camera da letto
3. Cucina
4. Corridoio
5. Ingresso
6. Spot
7. Soggiorno
8. Altre aree

Corridoio, ingresso e spot vengono dopo i casi semplici perché coinvolgono smart bulb e automazioni.
