#!/usr/bin/env python3
"""Build the Seoul hotel-comparison itineraries (20 unique plans).

Reads the ingestion files under seoul-hotel-itineraries/ and the research
catalogs in data/collections/, then generates:

  seoul-hotel-itineraries/itineraries/<slug>.md  - 20 printable Markdown plans
  seoul-hotel-itineraries/index.md               - one-screen grid overview
  review/seoul-hotels/index.html                 - review index (cards by hotel)
  review/seoul-hotels/itineraries/<slug>.html    - one printable page per plan

Workflow
--------
1. Edit seoul-hotel-itineraries/hotel-options.json -> set "consider": true
   on exactly the hotels the travel partner is choosing between.
2. Optionally edit seoul-hotel-itineraries/trip.json (dates, nights, group).
3. Run:  python3 scripts/build_seoul_hotel_itineraries.py

The 20 themes (seoul-hotel-itineraries/themes.json) are spread evenly across
the considered hotels, so every generated plan is a unique hotel x theme pair
(e.g. 4 hotels x 5 themes, 5 x 4, 2 x 10, or 1 x 20).

No third-party dependencies (reuses the review renderer from
build_itinerary_review.py).
"""

from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_itinerary_review import STYLES, render_markdown  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "seoul-hotel-itineraries"
MD_OUT = SRC / "itineraries"
REVIEW_OUT = ROOT / "review" / "seoul-hotels"
REVIEW_ITIN = REVIEW_OUT / "itineraries"

TOTAL_ITINERARIES = 20

# Short display names for the catalog hotel ids.
HOTEL_SHORT = {
    "seoul-four-points-josun-station": "Four Points Seoul Station",
    "seoul-nine-tree": "Nine Tree Myeongdong 1",
    "seoul-l7-myeongdong": "L7 Myeongdong",
    "seoul-ibis-styles": "Ibis Styles Myeongdong",
    "seoul-skypark-myeongdong3": "Skypark Myeongdong 3",
    "seoul-lescape": "L'Escape Myeongdong",
    "seoul-ibis-insadong": "Ibis Insadong",
    "seoul-four-seasons": "Four Seasons Seoul",
    "seoul-fairmont": "Fairmont Seoul",
}

# Which food-catalog neighborhoods count as "around this hotel".
HOTEL_FOOD_AREAS = {
    "seoul-nine-tree": ["myeongdong", "chungmuro", "city hall"],
    "seoul-l7-myeongdong": ["myeongdong", "chungmuro", "city hall"],
    "seoul-ibis-styles": ["myeongdong", "chungmuro", "city hall"],
    "seoul-skypark-myeongdong3": ["myeongdong", "chungmuro", "city hall"],
    "seoul-lescape": ["myeongdong", "chungmuro", "city hall"],
    "seoul-ibis-insadong": ["insadong", "jongno", "anguk"],
    "seoul-four-seasons": ["jongno", "insadong", "anguk", "city hall"],
    "seoul-fairmont": ["yeouido", "mapo", "gongdeok", "yongsan"],
}

# Station / airport-transfer notes for hotels missing a catalog walk time.
HOTEL_NOTES = {
    "seoul-ibis-insadong": {
        "station": "Anguk Station (Line 3) ~6 min walk; Jongno 3-ga (Lines 1/3/5) ~10 min",
        "airport": "Airport limousine stop in Jongno/Insadong area (verify route 6002/6011 on the day); AREX to Seoul Station + Line 1/3 is the rail fallback.",
    },
    "seoul-four-seasons": {
        "station": "Gwanghwamun Station (Line 5) ~3 min walk; Gyeongbokgung Station (Line 3) ~8 min",
        "airport": "Airport limousine routes serve the Gwanghwamun/Seoul Station corridor (verify stop + times); AREX to Seoul Station then Line 5 is the rail fallback.",
    },
    "seoul-fairmont": {
        "station": "Yeouinaru Station (Line 5) ~8 min walk; Yeouido Station (Lines 5/9) ~12 min",
        "airport": "Airport limousine routes serve Yeouido (6001/6005 family — verify); AREX to Seoul Station + Line 5 via Gongdeok is the rail fallback.",
    },
    "seoul-skypark-myeongdong3": {
        "station": "Myeongdong Station (Line 4) ~5 min walk; Euljiro 1-ga (Line 2) ~8 min",
        "airport": "Airport limousine stops in the Myeongdong core (verify the exact stop near the hotel).",
    },
    "seoul-lescape": {
        "station": "Myeongdong Station (Line 4) ~5 min walk; Euljiro 1-ga (Line 2) ~7 min",
        "airport": "Airport limousine stops in the Myeongdong core (verify the exact stop near the hotel).",
    },
}

# Theme-neutral convenience bullets that reference hotel data.
ARRIVAL_NIGHT_RULE = (
    "If this is the arrival-night hotel, verify the **24-hour front desk** at "
    "booking — the reference trip lands ICN 21:00 and check-in can pass midnight. "
    "Standard check-in is 15:00 on all other days."
)


# ------------------------------------------------------------------- data ---


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def hotel_slug(hotel_id: str) -> str:
    return hotel_id.replace("seoul-", "")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def short_hotel(name: str, hotel_id: str) -> str:
    return HOTEL_SHORT.get(hotel_id, name)


def build_candidates() -> list[dict]:
    """Merge hotel-options.json with the full catalog (data/collections/hotels.json)."""
    ingest = load_json(SRC / "hotel-options.json")["hotels"]
    catalog = {h["id"]: h for h in load_json(ROOT / "data/collections/hotels.json")}
    considered = [h for h in ingest if h.get("consider")]
    if not considered:
        print(
            "No hotels marked consider:true in seoul-hotel-itineraries/hotel-options.json — "
            "nothing to build. Set the flags first."
        )
        sys.exit(1)
    out = []
    for entry in considered:
        h = dict(catalog.get(entry["id"], {}))
        h.update(entry)  # consider / why from ingestion wins
        h["short"] = short_hotel(h.get("name", entry["id"]), entry["id"])
        notes = HOTEL_NOTES.get(entry["id"], {})
        h["stationNote"] = notes.get("station", h.get("stationWalkTime", "Check the hotel map on booking"))
        h["airportNote"] = notes.get(
            "airport",
            "Airport limousine stops near the hotel (verify route + times); AREX is the rail fallback.",
        )
        h["foodAreas"] = HOTEL_FOOD_AREAS.get(entry["id"], ["myeongdong"])
        out.append(h)
    return out


def distribute_themes(candidates: list[dict], themes: list[dict]) -> list[tuple[dict, dict, int]]:
    """Spread the 20 themes round-robin across the candidates.

    Returns [(hotel, theme, number)] with numbers S01..S20 grouped by hotel.
    """
    n = len(candidates)
    per_hotel: dict[str, list[dict]] = {c["id"]: [] for c in candidates}
    for i, theme in enumerate(themes):
        hotel = candidates[i % n]
        per_hotel[hotel["id"]].append(theme)
    combos: list[tuple[dict, dict, int]] = []
    num = 1
    for hotel in candidates:
        for theme in per_hotel[hotel["id"]]:
            combos.append((hotel, theme, num))
            num += 1
    return combos


def nearby_food(hotel: dict, theme: dict, limit: int = 10) -> list[dict]:
    """Food-catalog picks around this hotel, theme-priority first."""
    foods = [f for f in load_json(ROOT / "data/collections/food.json") if f.get("city") == "Seoul"]
    areas = [a.lower() for a in hotel["foodAreas"]]
    nearby = [
        f
        for f in foods
        if any(a in str(f.get("neighborhood", "")).lower() for a in areas)
    ]
    priority = theme.get("foodPriority", [])
    def rank(f):
        cat = f.get("category", "")
        p = priority.index(cat) if cat in priority else len(priority)
        tier = {"Budget": 0, "Budget-to-Mid": 1, "Mid-to-Premium": 2}.get(f.get("priceTier"), 1)
        # "Seoul Local ..." rows are generic placeholders in the source catalog —
        # push them to the end so named, reviewable spots surface first.
        local = 1 if str(f.get("name", "")).startswith("Seoul Local") else 0
        return (local, p, tier, f.get("name", ""))
    nearby.sort(key=rank)
    # Keep category variety in the final table (max 3 per category).
    chosen: list[dict] = []
    counts: dict[str, int] = {}
    for f in nearby:
        cat = f.get("category", "Other")
        if counts.get(cat, 0) >= 3:
            continue
        chosen.append(f)
        counts[cat] = counts.get(cat, 0) + 1
        if len(chosen) >= limit:
            break
    return chosen


def nearby_activities(hotel: dict, theme: dict, limit: int = 8) -> list[dict]:
    """Activity-catalog picks matching this theme's keywords."""
    acts = [a for a in load_json(ROOT / "data/collections/activities.json") if a.get("city") == "Seoul"]
    keywords = [k.lower() for k in theme.get("activityKeywords", [])]
    scored = []
    for a in acts:
        hay = f"{a.get('title','')} {a.get('snippet','')}".lower()
        hits = sum(1 for k in keywords if k.lower() in hay)
        if hits:
            scored.append((hits, a))
    scored.sort(key=lambda t: (-t[0], t[1].get("title", "")))
    return [a for _, a in scored[:limit]]


def food_cell(f: dict) -> str:
    name = f.get("name", "?")
    korean = f.get("koreanName", "")
    url = f.get("mapUrl", "")
    label = name + (f" ({korean})" if korean else "")
    if url:
        label = f"[{label}]({url})"
    return label


def activity_cell(a: dict) -> str:
    title = a.get("title", "?")
    url = a.get("officialUrl", "")
    label = f"[{title}]({url})" if url else title
    return label


def md_escape_cell(text: str) -> str:
    """Keep markdown table cells intact when content contains pipes."""
    return text.replace("|", "\\|").replace("\n", " ")


def day_block(day: dict, hotel: dict, foods: list[dict], day_idx: int) -> str:
    ctx = {
        "hotel": hotel["short"],
        "area": hotel.get("area", "Seoul"),
        "station": hotel.get("stationNote", "a nearby subway station"),
        "walk": hotel.get("stationWalkTime", ""),
    }
    lines = [f"**{day['title']}**"]
    for slot in ("dawn", "morning", "afternoon", "evening", "night"):
        text = day.get(slot)
        if text:
            lines.append(f"- **{slot.title()}:** {text.format(**ctx)}")
    # Localized eat note from the actual nearby picks.
    if foods:
        a = foods[day_idx % len(foods)]
        b = foods[(day_idx + 2) % len(foods)]
        lines.append(f"- **Eat around here:** {food_cell(a)} — {a.get('category','')} · {a.get('priceTier','')}; {food_cell(b)} — {b.get('category','')} · {b.get('priceTier','')}.")
    return "\n".join(lines)


def build_markdown(num: int, hotel: dict, theme: dict) -> str:
    ctx = {
        "hotel": hotel["short"],
        "area": hotel.get("area", "Seoul"),
        "station": hotel.get("stationNote", "a nearby subway station"),
        "walk": hotel.get("stationWalkTime", ""),
    }
    foods = nearby_food(hotel, theme)
    acts = nearby_activities(hotel, theme)
    trip = load_json(SRC / "trip.json")
    frame = trip["frame"]
    focus = ", ".join(theme.get("focus", []))
    why = (hotel.get("why") or "Central, well-reviewed, and a strong base for Seoul.").strip()
    # Placeholder substitution (theme text references {hotel}, {area}, {station}, {walk}).
    theme_blurb = theme["blurb"].format(**ctx)
    day_blocks = [day_block(d, hotel, foods, i) for i, d in enumerate(theme["days"])]
    days_md = "\n\n".join(f"### Day {i + 1}\n\n{block}" for i, block in enumerate(day_blocks))
    plan_b = theme.get("planB")
    if plan_b:
        days_md += "\n\n**Plan B (rain / low energy):** " + plan_b
    extra = "\n".join(f"- {e}" for e in theme.get("extraNights", []))
    price = f"${hotel['priceFrom']}–${hotel['priceTo']}/night (research range)" if hotel.get("priceFrom") else "see booking sites"
    free_count = sum(
        1 for a in acts
        if "free" in str(a.get("snippet", "")).lower() or "free" in a.get("title", "").lower()
    )
    tier_word = {"Budget": "budget", "Mid": "mid-range", "Premium": "premium"}.get(hotel.get("tier"), "mid-range")
    verifier = (
        "Verify opening hours, ticket availability, event dates, and the hotel's "
        "24-hour desk policy with official providers before booking. Prices are "
        "indicative research ranges, not quotes."
    )
    food_rows = "\n".join(
        "| " + md_escape_cell(food_cell(f)) + " | " + md_escape_cell(str(f.get("category", ""))) + " | " + md_escape_cell(str(f.get("priceTier", ""))) + " |"
        for f in foods
    )
    act_rows = "\n".join(
        "| " + md_escape_cell(activity_cell(a)) + " | " + md_escape_cell(str(a.get("category", ""))) + " | " + md_escape_cell(str(a.get("snippet", ""))) + " |"
        for a in acts
    )
    food_tiers = ", ".join(sorted({str(f.get("priceTier", "")) for f in foods})) or "Budget-to-Mid"
    frame_line = f"{frame['arrive']}, {frame['arriveTime']} → {frame['depart']}, {frame['departTime']} · {frame['nights']} nights ({frame['airport']})"
    station_note = hotel.get("stationNote", "")
    airport_note = hotel.get("airportNote", "")
    neighborhood = hotel.get("neighborhood", "")
    area = hotel.get("area", "Seoul")
    hotel_name = hotel["name"]
    hotel_short = hotel["short"]
    best_for = theme["bestFor"].strip()
    best_for_sentence = best_for[0].lower() + best_for[1:] if best_for else best_for
    theme_title = theme["title"]
    return f"""# S{num:02d} · {theme_title} — base: {hotel_short}

> **Hotel base:** {hotel_name} · {area}
> **Neighborhood:** {neighborhood}
> **Trip frame:** {frame_line}
> **Pace:** {theme['pace']} · **Focus:** {focus}
> **Theme #:** {num}/20 · **Hotel tier:** {tier_word} · **~{price}**
> **Review notes:** *(leave decisions/comments here)*

## Who this suits

{best_for} {theme_blurb}

## Why {hotel_short} for this plan

{why} The plan is routed so the sightseeing loops return to {hotel_short} each evening — most days end a short stroll (or one subway stop) from the front door.

## Around {area} — what's close

- **Station:** {station_note}
- **Airport transfer:** {airport_note}
- **Arrival night:** {ARRIVAL_NIGHT_RULE}

### Eat around here ({len(foods)} picks from the research catalog)

| Spot | Category | Price tier |
| --- | --- | --- |
{food_rows}

*Full hours, signature dishes, and quality notes: `research/sources/food/cities/seoul.md`.*

### Do around here ({len(acts)} picks matched to this theme)

| Activity | Category | Why it's here |
| --- | --- | --- |
{act_rows}

*Status and booking notes: `research/sources/fun/seoul.md` and `data/collections/activities.json`.*

## Day-by-day (3-day sample window)

{days_md}

## If you have more nights

{extra or '- No extras defined for this theme.'}

## Transit & convenience

- **Last-train habit:** check the last train on your line home each night (Seoul Metro typically ~23:30–00:00; late buses and Kakao T are the fallback).
- **Payments:** T-money card for the metro + a little cash (₩50k–100k) for markets; cards work at most restaurants.
- **This base:** {station_note}.
- **Weather:** November is crisp and dry; pack layers and a light rain shell. The theme's Plan B covers a rainy day.

## Value notes

- **Hotel:** {price} — {tier_word} tier in {area}.
- **Food:** nearby picks span {food_tiers} tiers; street food and market meals are the value anchors of this plan.
- **Free wins:** {free_count} of the featured activities are free or free-with-reservation.
- **Splurge vs save:** this theme leans **{focus}** — where it says book ahead (cable car, Secret Garden, cruises, shows), booking early is the real money-saver.

## Verdict

**Pick S{num:02d} ({theme_title} at {hotel_short}) if** {best_for_sentence} The {area} base keeps the itinerary convenient, the theme keeps it fun, and the catalog picks keep it good value. If the partner's priorities shift, swap this plan for another theme at the same hotel — the base stays, the days change.

---
*{verifier} Generated {datetime.date.today().isoformat()} by `scripts/build_seoul_hotel_itineraries.py` from `seoul-hotel-itineraries/` ingestion files + `data/collections/` research catalogs.*
"""


def build_index_md(combos: list[tuple[dict, dict, int]]) -> str:
    trip = load_json(SRC / "trip.json")
    lines = [
        "# Seoul Hotel-Comparison — 20 Itineraries (index)",
        "",
        f"> Trip frame: **{trip['frame']['arrive']}, {trip['frame']['arriveTime']} → {trip['frame']['depart']}, {trip['frame']['departTime']}** · {trip['frame']['nights']} nights · {trip['group']}",
        "> Each plan assumes **one Seoul hotel as the base for the whole stay** — the point is to compare bases. The 20 themes are spread across the hotels marked `consider: true` in `hotel-options.json`.",
        "",
        "| # | Itinerary | Hotel base | Pace | Focus | Best for |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for hotel, theme, num in combos:
        slug = f"{slugify(theme['title'])}-at-{hotel_slug(hotel['id'])}"
        lines.append(
            f"| S{num:02d} | [{theme['title']}](itineraries/{slug}.md) | {hotel['short']} | {theme['pace']} | {', '.join(theme.get('focus', []))} | {theme['bestFor']} |"
        )
    n_hotels = len({h["id"] for h, _, _ in combos})
    per_hotel = sorted(
        (sum(1 for h, _, _ in combos if h["id"] == hid) for hid in {h["id"] for h, _, _ in combos}),
        reverse=True,
    )
    split_desc = " × ".join(str(p) for p in per_hotel)
    lines += [
        "",
        "## Regenerate",
        "",
        "```bash",
        "python3 scripts/build_seoul_hotel_itineraries.py",
        "```",
        "",
        "## How the split works",
        "",
        f"- {n_hotels} hotel(s) considered, themes per hotel: {split_desc} = {TOTAL_ITINERARIES} total.",
        "- Edit `hotel-options.json` (which hotels, why) and `themes.json` (the 20 themes) and re-run.",
    ]
    return "\n".join(lines)


# ------------------------------------------------------------------- html ---


ITIN_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title} · For Two in Seoul</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#fafaf7;color:#1a2b27;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;line-height:1.6;-webkit-font-smoothing:antialiased}
.toolbar{position:sticky;top:0;z-index:10;display:flex;gap:.5rem;align-items:center;background:#14332d;color:#fff;padding:.6rem 1rem;font-size:.88rem}
.toolbar a{color:#eaf3ef;text-decoration:none;padding:.3rem .6rem;border-radius:6px}
.toolbar a:hover{background:rgba(255,255,255,.14)}
.tool-btn{margin-left:auto;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.3);color:#fff;border-radius:999px;padding:.35rem .9rem;cursor:pointer}
.page{max-width:860px;margin:0 auto;padding:28px 22px 60px}
.hero{background:#fff;border:1px solid #e6e2d6;border-radius:20px;padding:22px 22px 18px;box-shadow:0 6px 24px rgba(22,35,29,.06)}
.hero-top{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:10px}
.badge-num{background:#14332d;color:#fff;font-weight:700;border-radius:999px;padding:4px 10px;font-size:.78rem}
.badge-couple{background:#fff0f0;color:#b23a3a;border:1px solid #f1c6c6;border-radius:999px;padding:4px 10px;font-size:.72rem;font-weight:700;letter-spacing:.02em}
.badge-pace{background:#edf7f1;color:#2e6958;border:1px solid #d5e8df;border-radius:999px;padding:4px 10px;font-size:.72rem;font-weight:600}
.hero h1{margin:6px 0 8px;font-size:1.55rem;letter-spacing:-.02em;line-height:1.25;color:#14332d}
.hero-sub{color:#5a6b66;font-size:.93rem;margin:0}
.meta-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}
.meta-card{background:#fafaf7;border:1px solid #ece8da;border-radius:12px;padding:10px 12px}
.meta-card b{display:block;font-size:.72rem;letter-spacing:.07em;text-transform:uppercase;color:#2e6958;margin-bottom:3px}
.meta-card span{font-size:.86rem;color:#1a2b27}
.couple-note{margin-top:12px;background:#fff8e6;border:1px solid #f2d99d;border-radius:12px;padding:10px 12px;display:flex;gap:10px;align-items:start}
.couple-note .icon{font-size:1.1rem}
.couple-note p{margin:0;font-size:.86rem;color:#6b5a2a;line-height:1.5}
.couple-note strong{color:#5a4310}
.section{margin-top:22px;background:#fff;border:1px solid #e8e2d6;border-radius:16px;padding:18px 18px 14px;box-shadow:0 2px 10px rgba(22,35,29,.04)}
.section h2{margin:0 0 10px;font-size:1.02rem;letter-spacing:-.02em;color:#14332d;display:flex;align-items:center;gap:8px}
.section h2 small{font-weight:500;color:#6b7a74;font-size:.78rem}
.pill-grid{display:flex;flex-wrap:wrap;gap:7px}
.pill{background:#f6f7f4;border:1px solid #e2e6de;border-radius:999px;padding:6px 11px;font-size:.8rem;color:#2b3a36;display:inline-flex;align-items:center;gap:6px}
.pill em{font-style:normal;background:#fff;border:1px solid #e2e6de;border-radius:999px;padding:1px 6px;font-size:.7rem;color:#6b7a74}
.food-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.food-item{background:#fafaf7;border:1px solid #ece8da;border-radius:12px;padding:9px 11px;display:grid;gap:2px}
.food-item a{color:#14332d;font-weight:600;text-decoration:none;font-size:.86rem}
.food-item a:hover{text-decoration:underline}
.food-item span{font-size:.75rem;color:#6b7a74}
.activity-grid{display:grid;grid-template-columns:1fr;gap:8px}
.act-item{display:grid;grid-template-columns:1fr auto;gap:8px;align-items:start;background:#fbfcf9;border:1px solid #dce7de;border-radius:12px;padding:10px 12px}
.act-item b{font-size:.86rem;color:#14332d}
.act-item p{margin:3px 0 0;font-size:.8rem;color:#5a6b66;line-height:1.45}
.act-item a{font-size:.78rem;color:#2e6958;text-decoration:none;white-space:nowrap}
.act-item a:hover{text-decoration:underline}
.timeline{display:grid;gap:14px}
.day-card{border:1px solid #e6e2d6;border-radius:16px;overflow:hidden;background:#fff}
.day-head{display:flex;align-items:center;gap:10px;padding:12px 14px;background:linear-gradient(135deg,#14332d,#2a5a4b);color:#fff}
.day-num{background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.25);border-radius:10px;padding:4px 8px;font-weight:700;font-size:.78rem}
.day-title{font-weight:700;font-size:.95rem}
.day-body{padding:12px 14px;display:grid;gap:8px}
.slot{display:grid;grid-template-columns:72px 1fr;gap:10px;align-items:start}
.slot-label{font-size:.7rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:#fff;background:#2e6958;border-radius:7px;padding:4px 7px;text-align:center;line-height:1.2}
.slot-label.evening{background:#b58a1f}
.slot-label.night{background:#4a5568}
.slot p{margin:0;font-size:.84rem;color:#2b3a36;line-height:1.55}
.eat-line{margin-top:2px;padding:7px 9px;background:#fff8e6;border:1px dashed #f2d99d;border-radius:8px;font-size:.78rem;color:#6b5a2a}
.extra-grid{display:flex;flex-wrap:wrap;gap:7px}
.extra-chip{background:#edf7f1;border:1px solid #d5e8df;border-radius:999px;padding:5px 10px;font-size:.78rem;color:#2e6958}
.verdict{background:linear-gradient(135deg,#fff8e6,#fff);border:1px solid #f2d99d;border-radius:12px;padding:12px 14px}
.verdict strong{color:#7a5a10}
.foot{margin-top:18px;padding-top:12px;border-top:1px solid #e6e2d6;font-size:.78rem;color:#8b8577;text-align:center}
@media(max-width:640px){.page{padding:16px 14px 40px}.meta-grid{grid-template-columns:1fr}.food-grid{grid-template-columns:1fr}}
@media print{body{background:#fff}.toolbar{display:none}.page{padding:0;max-width:none}.hero,.section{box-shadow:none;break-inside:avoid}}
</style>
</head>
<body>
<nav class="toolbar">
  <a href="../index.html">← All itineraries</a>
  <span style="flex:1"></span>
  {prev_link}{next_link}
  <button class="tool-btn" onclick="window.print()">Print / Save PDF</button>
</nav>
<div class="page">
{content}
<footer class="foot">Made for two · first time in Korea · late 30s · Print this page for offline use</footer>
</div>
</body>
</html>
"""

INDEX_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Seoul for Two · 20 itineraries · First time in Korea</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#fafaf7;color:#1a2b27;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1100px;margin:0 auto;padding:28px 20px 50px}
.hero{background:linear-gradient(135deg,#14332d 0%,#2a5a4b 70%,#3a7a65 100%);color:#fff;border-radius:22px;padding:26px 26px 22px;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;right:-40px;top:-40px;width:220px;height:220px;background:rgba(255,255,255,.08);border-radius:50%}
.hero h1{margin:8px 0 8px;font-size:1.7rem;letter-spacing:-.03em;line-height:1.2;position:relative}
.hero p{margin:0;color:rgba(255,255,255,.86);font-size:.93rem;max-width:640px;position:relative}
.badge{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:5px 11px;font-size:.72rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase}
.filters{margin:18px 0 16px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.filter-btn{border:1px solid #dddcd2;background:#fff;border-radius:999px;padding:7px 12px;font-size:.82rem;cursor:pointer;color:#4a5a56;font-weight:500}
.filter-btn.is-active{background:#14332d;color:#fff;border-color:#14332d}
.hotel-section{margin-top:22px}
.hotel-head{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:10px}
.hotel-head h2{margin:0;font-size:1.08rem;color:#14332d;letter-spacing:-.02em}
.hotel-head span{font-size:.8rem;color:#6b7a74}
.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.card{display:grid;gap:6px;background:#fff;border:1px solid #e8e2d6;border-radius:16px;padding:14px 14px;text-decoration:none;color:inherit;transition:transform .15s,box-shadow .15s;position:relative;overflow:hidden}
.card:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(22,35,29,.08);border-color:#d5cdb8}
.card-top{display:flex;align-items:center;gap:7px;flex-wrap:wrap}
.num{background:#14332d;color:#fff;font-weight:700;border-radius:8px;padding:3px 7px;font-size:.74rem}
.vibe{background:#edf7f1;color:#2e6958;border:1px solid #d5e8df;border-radius:999px;padding:3px 8px;font-size:.68rem;font-weight:600}
.pace{color:#6b7a74;font-size:.72rem}
.card h3{margin:0;font-size:.96rem;letter-spacing:-.015em;color:#14332d;line-height:1.3}
.card p{margin:0;font-size:.82rem;color:#5a6b66;line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.card-foot{display:flex;align-items:center;gap:6px;margin-top:4px;font-size:.74rem;color:#2e6958;font-weight:600}
.card-foot span{color:#a8b0ad;font-weight:400}
.foot{margin-top:28px;text-align:center;font-size:.76rem;color:#8b8577}
@media(max-width:740px){.cards{grid-template-columns:1fr}.hero{padding:22px 18px}}
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <span class="badge">♡ Made for two · late 30s · first time in Korea</span>
    <h1>Seoul — what to do & eat around each hotel</h1>
    <p>20 easy-to-scan itineraries, all built for a couple's first Seoul trip. Same Seoul base every night, one gentle idea before lunch + one after, cozy evenings together.</p>
    <p style="margin-top:10px;font-size:.82rem;color:rgba(255,255,255,.9)">{frame_line}</p>
  </header>
  <div class="filters" id="filters">
    <button class="filter-btn is-active" data-filter="all">All 20</button>
    <button class="filter-btn" data-filter="Classic & Easy">Classic & Easy</button>
    <button class="filter-btn" data-filter="Food Together">Food Together</button>
    <button class="filter-btn" data-filter="Romantic & Slow">Romantic & Slow</button>
    <button class="filter-btn" data-filter="Explore & Play">Explore & Play</button>
    <button class="filter-btn" data-filter="Balanced">Balanced</button>
  </div>
  {sections}
  <p class="foot">Tap any card → clean, printable page with morning / afternoon / evening timeline. Verify hours & prices before you book.</p>
</div>
<script>
document.querySelectorAll('.filter-btn').forEach(btn=>{
  btn.addEventListener('click',()=>{
    document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('is-active'));
    btn.classList.add('is-active');
    const f=btn.dataset.filter;
    document.querySelectorAll('.card').forEach(c=>{
      c.style.display=(f==='all'||c.dataset.vibe===f)?'':'none';
    });
    document.querySelectorAll('.hotel-section').forEach(s=>{
      const visible=[...s.querySelectorAll('.card')].some(c=>c.style.display!=='none');
      s.style.display=visible?'':'none';
    });
  });
});
</script>
</body>
</html>
"""

CARD = """      <a class="card" href="itineraries/{slug}.html" data-vibe="{vibe}">
        <div class="card-top"><span class="num">S{num:02d}</span><span class="vibe">{vibe}</span><span class="pace">{pace}</span></div>
        <h3>{title}</h3>
        <p>{summary}</p>
        <div class="card-foot">Open timeline → <span>· {focus}</span></div>
      </a>"""



def build_streamlined_html(num, hotel, theme, slug):
    ctx = {"hotel": hotel["short"], "area": hotel.get("area","Seoul"), "station": hotel.get("stationNote",""), "walk": hotel.get("stationWalkTime","")}
    foods = nearby_food(hotel, theme, limit=6)
    acts = nearby_activities(hotel, theme, limit=6)
    trip = load_json(SRC / "trip.json")
    frame = trip["frame"]
    focus_tags = " · ".join(theme.get("focus", []))
    price = f"${hotel['priceFrom']}–${hotel['priceTo']}/night" if hotel.get("priceFrom") else "see booking sites"
    # couple tag
    vibe = theme.get("coupleTag","Balanced")
    pace = theme.get("pace","Easy")
    # Build hero
    hero = f"""
    <section class="hero">
      <div class="hero-top"><span class="badge-num">S{num:02d}</span><span class="badge-couple">For two · late 30s · first time</span><span class="badge-pace">{pace}</span><span class="pill">{vibe}</span></div>
      <h1>{theme['title']} — at {hotel["short"]}</h1>
      <p class="hero-sub">{theme["bestFor"]}</p>
      <div class="meta-grid">
        <div class="meta-card"><b>Base</b><span>{hotel["name"]} · {hotel.get("area","Seoul")}</span></div>
        <div class="meta-card"><b>Price</b><span>{price}</span></div>
        <div class="meta-card"><b>Stay</b><span>{hotel.get("neighborhood","")}</span></div>
        <div class="meta-card"><b>Flow</b><span>{frame["arrive"]}, {frame["arriveTime"]} → {frame["depart"]}, {frame["departTime"]}</span></div>
      </div>
      <div class="couple-note"><span class="icon">♡</span><p><strong>Together pace:</strong> One main idea before lunch, one after — evenings are cozy and close to {hotel["short"]}. No rushing, lots of time for photos, coffee, and wandering.</p></div>
    </section>
    """
    # Eat pills
    food_html = "".join(f'<div class="food-item"><a href="{f.get("mapUrl","#")}" target="_blank" rel="noreferrer">{f.get("name","")}</a><span>{f.get("category","")} · {f.get("priceTier","")}</span></div>' for f in foods)
    act_html = "".join(f'<div class="act-item"><div><b>{a.get("title","")}</b><p>{a.get("snippet","")[:160]}</p></div><a href="{a.get("officialUrl","#")}" target="_blank" rel="noreferrer">Open ↗</a></div>' for a in acts)
    # Days timeline
    days_html = ""
    for i, d in enumerate(theme["days"]):
        slots=""
        for label in ["dawn","morning","afternoon","evening","night"]:
            if d.get(label):
                icon = {"dawn":"🌅","morning":"☀️","afternoon":"🏙️","evening":"🌇","night":"🌙"}.get(label,label)
                slots+=f'<div class="slot"><span class="slot-label {label}">{label}</span><p>{icon} {d[label].format(**ctx)}</p></div>'
        # eat line
        eat_line=""
        if foods:
            a=foods[i % len(foods)]; b=foods[(i+2)%len(foods)]
            eat_line=f'<div class="eat-line">🍜 Together bite: <b>{a.get("name","")}</b> and <b>{b.get("name","")}</b> — both a short walk from {hotel["short"]}.</div>'
        days_html+=f'<article class="day-card"><div class="day-head"><span class="day-num">Day {i+1}</span><span class="day-title">{d["title"]}</span></div><div class="day-body">{slots}{eat_line}</div></article>'
    extra = "".join(f'<span class="extra-chip">{e}</span>' for e in theme.get("extraNights",[])[:4])
    planb = theme.get("planB","")
    why = hotel.get("why","Central base with easy transit home together.")
    verdict = f"""<section class="section verdict"><h2>♡ Verdict for you two</h2><p><strong>Pick this if</strong> {theme["bestFor"].lower()} It keeps evenings simple near {hotel["short"]}, with one lovely thing to share each half-day.</p></section>"""
    html = hero
    html += f'<section class="section"><h2>☕ Eat together near {hotel["short"]} <small>tap to open map</small></h2><div class="food-grid">{food_html}</div></section>'
    html += f'<section class="section"><h2>✦ Do together <small>matched to this theme</small></h2><div class="activity-grid">{act_html}</div></section>'
    html += f'<section class="section"><h2>🗓 Your 3-day sample together</h2><div class="timeline">{days_html}</div><div style="margin-top:10px;padding:10px 12px;background:#f6f7f4;border-radius:10px;font-size:.82rem;color:#5a6b66">☔ <b>Together Plan B:</b> {planb}</div></section>'
    if extra:
        html += f'<section class="section"><h2>＋ If you have more nights</h2><div class="extra-grid">{extra}</div></section>'
    html += f'<section class="section"><h2>🚇 Getting around together</h2><p style="font-size:.86rem;color:#2b3a36;margin:0">Station: {hotel.get("stationNote","")}. Airport: {hotel.get("airportNote","")} Last trains ~23:30 — grab a taxi together if you stay out late.</p><p style="font-size:.82rem;color:#6b7a74;margin:8px 0 0">November is crisp — layers + light shell. T-money for two, small cash for markets.</p></section>'
    html += verdict
    return html


def build_html(combos: list[tuple[dict, dict, int]]) -> None:
    REVIEW_ITIN.mkdir(parents=True, exist_ok=True)
    generated = datetime.date.today().isoformat()
    trip = load_json(SRC / "trip.json")
    frame_line = (
        f"Trip frame: <strong>{trip['frame']['arrive']}, {trip['frame']['arriveTime']}</strong> → "
        f"<strong>{trip['frame']['depart']}, {trip['frame']['departTime']}</strong> · "
        f"{trip['frame']['nights']} nights · {trip['group']}. "
        f"{trip.get('singleHotelNote', '')} {trip.get('frame', {}).get('note', '')}"
    )
    pages: list[dict] = []
    for hotel, theme, num in combos:
        md = build_markdown(num, hotel, theme)
        slug = f"{slugify(theme['title'])}-at-{hotel_slug(hotel['id'])}"
        pages.append({
            "num": num, "slug": slug, "hotel": hotel, "theme": theme,
            "title": f"S{num:02d} · {theme['title']} — {hotel['short']}",
            "md": md, "body": render_markdown(md),
        })
    for i, p in enumerate(pages):
        prev = pages[i - 1] if i > 0 else None
        nxt = pages[i + 1] if i < len(pages) - 1 else None
        prev_link = f'<a class="tool" href="{prev["slug"]}.html">← {prev["title"].split("·")[0].strip()}</a>' if prev else ""
        nxt_link = f'<a class="tool" href="{nxt["slug"]}.html">{nxt["title"].split("·")[0].strip()} →</a>' if nxt else ""
        # Build streamlined body
        streamlined = build_streamlined_html(p["num"], p["hotel"], p["theme"], p["slug"])
        html_out = ITIN_PAGE.replace("{title}", p["title"]).replace("{content}", streamlined).replace("{generated}", generated).replace("{prev_link}", prev_link).replace("{next_link}", nxt_link)
        (REVIEW_ITIN / f"{p['slug']}.html").write_text(
            html_out,
            encoding="utf-8",
        )
    # Index grouped by hotel.
    by_hotel: dict[str, list] = {}
    for p in pages:
        by_hotel.setdefault(p["hotel"]["short"], []).append(p)
    sections = []
    for hotel_name, items in by_hotel.items():
        cards = "\n".join(
            CARD.format(slug=p["slug"], num=p["num"], title=p["theme"]["title"],
                        pace=p["theme"]["pace"], summary=p["theme"]["bestFor"],
                        focus=", ".join(p["theme"].get("focus", [])), vibe=p["theme"].get("coupleTag","Balanced"))
            for p in items
        )
        h = items[0]["hotel"]
        blurb = f"{h.get('area', 'Seoul')} · {h.get('neighborhood', '')} · ~${h.get('priceFrom')}–${h.get('priceTo')}/night"
        sections.append(
            f'<section class="route-section"><h2>{hotel_name}</h2><p class="route-blurb">{blurb}</p><div class="cards">\n{cards}\n  </div></section>'
        )
    html_idx = INDEX_PAGE.replace("{frame_line}", frame_line).replace("{sections}", "\n".join(sections))
    (REVIEW_OUT / "index.html").write_text(
        html_idx,
        encoding="utf-8",
    )


def main() -> None:
    candidates = build_candidates()
    themes = load_json(SRC / "themes.json")["themes"]
    if len(themes) < TOTAL_ITINERARIES:
        print(f"Need at least {TOTAL_ITINERARIES} themes, found {len(themes)}.")
        sys.exit(1)
    combos = distribute_themes(candidates, themes[:TOTAL_ITINERARIES])
    # Clean previous output so stale plans (from an older hotel shortlist) don't linger.
    MD_OUT.mkdir(parents=True, exist_ok=True)
    for stale in MD_OUT.glob("*.md"):
        stale.unlink()
    REVIEW_ITIN.mkdir(parents=True, exist_ok=True)
    for stale in REVIEW_ITIN.glob("*.html"):
        stale.unlink()
    for hotel, theme, num in combos:
        slug = f"{slugify(theme['title'])}-at-{hotel_slug(hotel['id'])}"
        (MD_OUT / f"{slug}.md").write_text(build_markdown(num, hotel, theme), encoding="utf-8")
    (SRC / "index.md").write_text(build_index_md(combos), encoding="utf-8")
    build_html(combos)
    per = {c["short"]: sum(1 for h, _, _ in combos if h["id"] == c["id"]) for c in candidates}
    print(f"Built {len(combos)} itineraries across {len(candidates)} hotels: "
          + ", ".join(f"{k} x{v}" for k, v in per.items()))
    print(f"  Markdown:  {MD_OUT}")
    print(f"  Index:     {SRC / 'index.md'}")
    print(f"  Review:    {REVIEW_OUT / 'index.html'}")


if __name__ == "__main__":
    main()
