# Seoul Hotel-Comparison — 20 Itineraries

A companion module to the master planner: **20 unique itineraries that compare the
travel partner's top Seoul hotel options**. Each itinerary is built around one
hotel base and answers the question *"what do we do and eat around here?"* —
balanced across **convenience, activities, fun, and value**.

## The one-line workflow

1. **Ingest her hotel choices** → edit `hotel-options.json`
2. **Optional:** adjust trip dates / nights in `trip.json`
3. **Build** → `python3 scripts/build_seoul_hotel_itineraries.py`

The build spreads the **20 themes** (`themes.json`) evenly across the hotels
marked `consider: true`, so every plan is a unique **hotel × theme** pair:

| Hotels considered | Themes per hotel | Total |
| --- | --- | --- |
| 1 | 20 | 20 |
| 2 | 10 + 10 | 20 |
| 4 | 5 + 5 + 5 + 5 | 20 |
| 5 | 4 + 4 + 4 + 4 + 4 | 20 |
| 8 | 3 + 3 + 3 + 3 + 2 + 2 + 2 + 2 | 20 |

## Ingesting the hotel choices (`hotel-options.json`)

The file is pre-filled with the **9 Seoul hotels already researched** in
`data/collections/hotels.json` (Myeongdong cluster, Seoul Station, Insadong,
Gwanghwamun, Yeouido). For each hotel her partner is actually deciding between:

- set `"consider": true`
- optionally add a `"why"` note — it becomes the opening of that hotel's plans

```json
{ "id": "seoul-nine-tree", "consider": true,
  "why": "Her top value pick — 1-min walk to Myeongdong Station." }
```

Everything else about the hotel (price range, neighborhood, station, amenities)
is pulled automatically from the catalog.

## What each itinerary contains

- **Header card** — hotel base, neighborhood, trip frame, pace, focus tags, tier & price range
- **Who this suits / why this hotel for this plan**
- **Around the hotel** — station + airport-transfer notes (incl. the arrival-night
  24-hour front-desk rule), a **nearby eats table** and a **nearby activities table**
  filtered from the research catalogs, matched to the theme
- **Day-by-day (3-day sample window)** — localized with real nearby food picks and
  a Plan B for rain / low energy
- **If you have more nights** — stretch ideas
- **Transit & convenience** and **Value notes**
- **Verdict** — who should pick this combo

## Output

| Path | What it is |
| --- | --- |
| `itineraries/*.md` | The 20 printable plans (S01–S20) |
| `index.md` | One-screen grid of all 20 |
| `../review/seoul-hotels/index.html` | Review index — cards grouped by hotel |
| `../review/seoul-hotels/itineraries/*.html` | Printable document-style pages (Print / Save PDF) |

## Notes

- The committed `hotel-options.json` currently reflects the latest shortlist
  the user provided: **Four Points by Sheraton Josun, Seoul Station + ibis
  Styles Ambassador Seoul Myeongdong**. Swap the flags to any new shortlist and
  re-run — the generator replaces the whole `itineraries/` output each time.
- Trip frame defaults to the master planner's Nov 1–22, 2026 window; edit
  `trip.json` for her real dates.
- Prices, hours, event dates, and hotel policies in the generated plans are
  research estimates — always verify with official providers before booking.
