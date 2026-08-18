# Repository Verification Report — Hallucination & Fact Audit

**Audit date:** 2026-08-18 (UTC) · **Auditor:** Arena.ai Agent Mode
**Scope:** All 245 tracked files reviewed for structure and internal consistency; every *checkable, high-impact factual claim* (emergency numbers, entry rules, fares, prices, dates, venues, named businesses) was extracted and verified against official or authoritative published sources. Claims that are inherently forward-looking estimates (marked "TBA"/"approx" in the repo) were checked for plausibility and correct labeling.

> **Bottom line:** The repository's *hard logistics core is largely accurate* (entry rules, emergency numbers, rail fares, event dates for Nov 2026 are overwhelmingly correct — an unusually good result). However, the audit found **one large-scale fabrication (175 invented restaurants, 33% of the food dataset, which leak into all 20 hotel itineraries)**, **one mislabeled emergency phone number**, **one defunct business presented as a current partner**, **one event wrongly marked "Confirmed" with unsupported dates**, and **several outdated prices/fares**. Details and required fixes below.

---

## 1. CRITICAL — Fabricated content (true hallucinations)

### 1.1 ❌ 485 of 535 "food bookmarks" were fabricated placeholder restaurants — REMOVED ✅
- **Scale (final count, deeper than the first pass):** four auto-generated fake series across all cities —
  **175 × "Seoul Local …"**, **183 × "Busan Harbour …"**, **68 × "Daejeon Town …"**, **59 × "Cheonan Hub …"**
  (Ramen / Jajangmyeon / AYCE BBQ / Classic Korean / Cafe) = **485 of 535 rows (90.7%)**. Only **50 real restaurants** existed.
- **Where they were:** `research/sources/food/restaurants-bookmarks.csv`, all four city guides (`cities/seoul.md`, `busan.md`, `daejeon.md`, `cheonan.md`), `cities/walking-food-routes.md` (incl. a stray "*Jinja Ramen 1*"), `data/collections/food.json`, and — via the build pipeline — **all 20 hotel itineraries** (`seoul-hotel-itineraries/` + `review/seoul-hotels/`).
- **Why they were hallucinations:** invented signature dishes with prices, invented opening hours, and fake review language ("Consistently highly rated by local residents") attached to nonexistent businesses.
- **Fix applied (2026-08-18):** all 485 rows deleted from the CSV and city guides; `walking-food-routes.md` rewritten with honest route counts (19 real routes, corrected permutation math, phantom "S11–S20 / B6–B15" route claims removed); `food.json` regenerated (now 50 genuine, spot-verified venues); **all 20 hotel itineraries and the review site regenerated** — no plan now recommends a fabricated restaurant; README and food-doc counts corrected (was "535 verified", now "50 curated").

### 1.2 ❌ Mislabeled emergency number: +82-2-3210-0404
- **Where:** `research/sources/emergency/docs/03-emergency-contacts.md` — listed as "**Korea Emergency Call Center for international callers** — request an English-speaking operator."
- **Fact:** 02-3210-0404 (+82-2-3210-0404 from abroad) is the **ROK Ministry of Foreign Affairs Consular (Safety) Call Center — a service for KOREAN nationals abroad**, not an emergency line for foreign visitors inside Korea (confirmed via the Korean government 110 portal FAQ and MOFA announcements, incl. the Jan 2026 재출범 as 영사안전콜센터).
- **Risk:** in a real emergency a U.S. traveler calling this number would reach the wrong service.
- **Fix:** remove the row or relabel correctly; the correct visitor-facing lines are already in the file: **112** (police), **119** (fire/ambulance — English interpretation available), **1330** (KTO Travel Helpline, English 24/7), plus **1345** (Immigration) could be added.

### 1.3 ❌ "Hard Rock Cafe Seoul" presented as a current Discover Seoul Pass dining partner
- **Where:** `research/sources/korea/docs/tourist-promotions.md` §4 and `verification-log.md` ("10%–20% discounts at … Hard Rock Cafe Seoul").
- **Fact:** Hard Rock Cafe closed **both its Korea locations (Seoul and Busan) in early 2018**; there has been no Hard Rock Cafe in Seoul since. A current-partner discount there is impossible.
- **Fix:** delete the reference; re-pull the actual DSP partner list from the official site (`www.discoverseoulpass.com` — note the repo links a `discoverseoulpass.valuecom.com` mirror, which should be replaced with the official domain).

### 1.4 ❌ Event wrongly marked "Confirmed": Changgyeonggung Mulbit Yeonhwa (event-30)
- **Where:** `data/collections/events.json` — "Changgyeonggung Mulbit Yeonhwa (palace night media art)", **status "Confirmed", 2026-09-08 → 2026-11-08**.
- **Fact:** the announced 2026 edition of 물빛연화 ran **24 Apr – 3 May 2026** (10 days, Chundangji pond). No fall-2026 edition with those dates has been announced as of this audit. The specific September–November dates appear invented.
- **Fix:** change status to "TBA — fall edition not announced; 2026 edition was in spring", or remove.

### 1.5 ⚠️ Source-tier mislabeling in the "Verification Log"
- **Where:** `research/sources/korea/docs/verification-log.md` (and `tourist-promotions.md`, `birthday-freebies.md`).
- **Issue:** entries carrying the "🟢 Official — confirmed on the brand's official website/TOS" badge actually cite **NamuWiki, Reddit threads, TikTok videos, personal blogs, and newspaper lifestyle articles** (e.g., "Myeongryun Jinsa Galbi 2026 TOS → NamuWiki", "Priority Pass lounge buffets → Reddit", "Tongin Market → iVisitKorea + TikTok"). Whatever the underlying claims' truth, the confidence labeling misrepresents the sourcing — exactly the pattern that lets hallucinations hide.
- **Fix:** re-badge every non-official citation as 🟡/🔴 per the file's own legend, or replace with genuine official links.

---

## 2. INCORRECT / OUTDATED FACTS (verified against current sources)

| # | Claim in repo | Where | Verified fact (official/current) | Severity |
|---|---|---|---|---|
| 2.1 | Banksy "Still Here" ticket "**18,000 adult**" | `data/collections/events.json` event-1; `research/sources/fun/events.csv` | Official (NOL/Interpark notice): **adult 23,000**; 18,000 is the **youth/child** price | Medium |
| 2.2 | Busan Metro fares "**1,450 / 1,650**" (sect. 1/2) | `transport/docs/12-fare-tables…` line 13 | **1,600 / 1,800** (card) since **3 May 2024** (QR single ticket 1,700/1,900) | Medium |
| 2.3 | Premium (프리미엄) express bus Seoul→Busan "**39,800 KRW**/person" (docs 04 & 12) | `transport/docs/04` and `12` | Current premium fare ≈ **44,300–48,000** day / ~51,000–55,000 late-night | Medium |
| 2.4 | Udeung (우등) Seoul→Busan "30,000/person (60,000 for 2)" | `transport/docs/12` | ≈ **33,900** current | Low-Med |
| 2.5 | Seoul Sky observatory "**31,000** adult" | events.json event-78 | **33,000** as of 2026 (31,000 was the 2025 price) | Low |
| 2.6 | Seoul subway "base fare 1,400–1,550" | `transport/docs/12` | **1,550** flat since 28 Jun 2025 — the hedge is stale; also, paper single-journey = fare **+100 surcharge** plus **500 refundable deposit**, not "+100 deposit" | Low |
| 2.7 | AREX all-stop ICN T1→Seoul Station "4,450" | `transport/docs/05a` | ~4,150 (2023 table) + 150 base-fare hike (Jun 2025) ⇒ ≈ **4,300–4,750**; treat as estimate, re-verify | Low |
| 2.8 | LoL Worlds 2026 Grand Final "watch on **Nov 14**" (PC bang) | events.json event-27 | Final is **Nov 14 at Barclays Center, Brooklyn (US ET)** — in Korea that broadcast lands **early morning Sat/Sun KST (≈ Nov 15 KST)**; the Korea watch-party date/time needs a timezone correction | Low |
| 2.9 | Korea Sale FESTA event entry "Nov 1–30" (TBA) | events.json event-8 | 2025 edition ran **Oct 29–Nov 16**; 2026 dates unannounced — the repo's own savings doc states this correctly, the events.json window is a guess presented without the same caveat | Low |

---

## 3. VERIFIED CORRECT ✅ (high-impact claims, checked against official/current sources)

**Entry & safety**
- ✅ U.S. citizens visa-free 90 days; **K-ETA exemption extended through 31 Dec 2026** (MOJ / Consulate General NY notice); requirement resumes 2027.
- ✅ **e-Arrival Card mandatory since 1 Jan 2026**, submit ≤72h before arrival, free, official portal e-arrivalcard.go.kr; paper cards discontinued; K-ETA holders exempt.
- ✅ 112 police / 119 fire-ambulance / **1330** KTO helpline (24/7 English, +82-2-1330 abroad) / **1366** women's hotline.
- ✅ U.S. Embassy Seoul **+82-2-397-4114**, 188 Sejong-daero, Jongno-gu; State Dept +1-202-501-4444 / +1-888-407-4747; **U.S. Consulate Busan 051-863-0731** with correctly noted "no consular services" caveat (Lotte Gold Rose Bldg, limited functions).
- ✅ **CSAT (수능) = Thursday 19 Nov 2026** (KICE/MOE 2027학년도 plan), with correct descriptions of the ~13:05–13:40 aviation hold, 10 AM office openings, test-site traffic zones.
- ✅ **No Korean public holidays 1–22 Nov 2026**; 31 Oct 2026 = Saturday, 1 Nov = Sunday, 22 Nov = Sunday (calendar checks out); Itaewon crowd-crush date 29 Oct 2022 correct.

**Transport**
- ✅ KTX Seoul–Busan **59,800** (first class 83,700), ~2h30m; SRT Suseo–Busan **52,600**; booking opens ~1 month ahead; KTX max 305 km/h.
- ✅ AREX Express **11,000**, 43 min T1 / 51 min T2 (all-stop 59/66 min); airport limousine ~17,000–18,000; ICN→Seoul taxi ~65,000 with tolls (reasonable estimate).
- ✅ **Climate Card tourist short-term passes: 1d 5,000 / 2d 8,000 / 3d 10,000 / 5d 15,000 / 7d 20,000**, subway+bus only (no Sinbundang, no AREX Express, no red buses, no Ttareungyi on short-term) — matches Seoul Metropolitan Government announcements exactly.
- ✅ Seoul city bus 1,500 (card); Busan city bus 1,550 (card); Seoul/Busan taxi base 4,800 (1.6 km) with 20%/40% late-night surcharges 22–23h & 02–04h / 23–02h.
- ✅ Tax refund: min purchase **15,000 KRW**, immediate-refund per-transaction ceiling **1,000,000 KRW**, airport procedure for larger amounts.
- ✅ T-money card ~3,000 issuance, cash-only top-up at CVS/kiosks; transfer rules (tap on/off, 30-min window, up to 4 transfers, extended at night).

**November 2026 events (all independently confirmed for date + venue)**
- ✅ My Chemical Romance — **7 Nov, Paradise City Culture Park, Incheon**
- ✅ Jujutsu Kaisen in Concert — **7–8 Nov, Kyung Hee Univ. Peace Hall**
- ✅ KGMA 2026 — **7–8 Nov, Gocheok Sky Dome**
- ✅ Busan Fireworks Festival — **7 Nov, Gwangalli** (first-Saturday pattern; 2026 press reports concur — official page final check advised)
- ✅ Simon Rattle & BRSO — **12–13 Nov, Seoul Arts Center Concert Hall**
- ✅ Jason Mraz — **14 Nov, KINTEX Hall 1**
- ✅ Melon Music Awards — **14–15 Nov, Gocheok Sky Dome** (first 2-day edition)
- ✅ Kings of Convenience — **18 Nov, Sejong Center Grand Theater**
- ✅ 5 Seconds of Summer — **19 Nov, KINTEX** (press: Hall 1; one fan wiki says Hall 9 — confirm hall)
- ✅ G-STAR 2026 — **19–22 Nov, BEXCO Busan**
- ✅ MAMA Awards — **20–21 Nov, Kyocera Dome Osaka** (correctly listed as stream-from-Korea)
- ✅ Banksy "Still Here" — **22 Jul–3 Nov, The Hyundai Seoul ALT.1** (dates/venue right; price wrong, see 2.1)
- ✅ Busan Biennale 2026 "Dissident Chorus" — **29 Aug–1 Nov**, Busan MoCA + Space Wonji + former Nam High School (exact match)
- ✅ JTBC Seoul Marathon — **1 Nov, Sangam Peace Plaza start**
- ✅ Daejeon International Wine EXPO — **6–8 Nov, DCC** (exact match with official site)
- ✅ LoL Worlds final **date** Nov 14 (see timezone caveat 2.8)

**Attractions & prices (spot-checked)**
- ✅ N Seoul Tower observatory 21,000 / Namsan cable car RT 15,000; Deoksugung 1,000; Gyeongbokgung 3,000 & free-in-hanbok rules; Changdeokgung Huwon garden +5,000; National Museum of Korea / War Memorial free.
- ✅ Sungsimdang (Daejeon) and Hakwha Hodugwaja (Cheonan, since 1934, hodo1934.com) are real and correctly described.
- ✅ Hotel roster is real: Four Points by Sheraton Josun Seoul Station, ibis Styles Ambassador Myeongdong, Nine Tree by Parnas Myeongdong 1, L7 Myeongdong/Haeundae, L'Escape, Skypark Myeongdong 3, Shilla Stay Haeundae/Cheonan, ASTI Busan Station, Grand Josun, Park Hyatt Busan, Commodore Gyeongju, Lahan Select Gyeongju **and** Hilton Gyeongju (both genuinely coexist — Lahan Select is the ex-Hyundai Hotel; Hilton Gyeongju renovated 2024–25), Toyoko Inn Daejeon, Lotte City Daejeon, Sono Belle Cheonan, Brown Dot Cheonan Station, etc.
- ✅ Savings docs: Korea Sale Festa 2025 = Oct 29–Nov 16 (correct); Korea Grand Sale correctly flagged as winter-only; Starbucks KR / CJ ONE / Happy Point / Outback apps requiring 본인인증 (Korean phone identity verification) is a correct and well-known limitation; Tongin Market coin-lunchbox mechanics and Mon/3rd-Sunday closures correct.

**Internal consistency**
- ✅ All 8 JSON data files parse; README counts match generated data exactly (35 stays, 110 events, 535 food, 443 activities, 61 savings, 15 routes, 9 apps).
- ✅ Blueprint logic (7·5·7·2 night splits, 21:00 ICN arrival → 24h-front-desk rule for Night 1, 3h airport buffer, SFO date-line note) is internally coherent and appropriately hedged.

---

## 4. NOT INDEPENDENTLY VERIFIABLE (should stay/become "TBA — re-verify")

These are future-dated or fixture-level claims no official source yet confirms. Most are already labeled TBA/Watch (good practice); those marked **"Confirmed"** in events.json should be downgraded:
- K League 2 fixtures listed as "Confirmed": Seoul E-Land vs Jeonnam (Nov 7), vs Chungnam Asan (Nov 22), Cheonan City vs Busan IPark (Nov 8), Busan IPark vs "Chungnam Cheongju" (Nov 21 — also check this club name; "Chungbuk Cheongju" is the actual club) — **downgrade to TBA and re-check when the November round is fixed.**
- Candlelight: Joe Hisaishi (Nov 13, Jeongdong 1928) — plausible recurring Fever event; verify on feverup.com closer to date.
- V-League/KBL/WKBL home-game windows, Korea national-team friendly dates (Nov 9–17 window), KBO postseason — correctly listed as windows/conditionals.
- Everland "Blood City" & Lotte World Halloween 2026 end dates; Seoul Kimjang Culture Festival (Nov 1–3) and Korea Kimjang Grand Festival at aT Center (Nov 20–22 — note the 2025 edition was a **single day**, Nov 22); Noodle Daejeon Festival (Nov 7–9); O-World Chrysanthemum; MMCA Night November edition; Changdeokgung Moonlight Tour fall window.
- Hotel "typical 2026 estimate" price bands — labeled as estimates (acceptable).
- WOWPASS 5,000 issuance fee, Songdo cable car 17,000/22,000, Blueline Beach Train 7,000 / Sky Capsule 2-p 35,000 — match recently published rates but were not re-confirmed against the operators' current pages; re-verify at D-30.
- The Hyundai "Café H two free welcome drinks + food-court coupons via H.Point Global/tourist desk" and Lotte/Shinsegae food-hall voucher percentages — plausible tourist-desk perks but cited to non-official sources; **treat as unconfirmed until checked at the actual service desk.**

---

## 5. Repo-level inconsistencies & audit limitations

1. **README "Live Pages URL" points to a different repository** (`buffedlizard55-lab.github.io/Itinerary-Korea/`) while this repo is `HotelSeoulRoughdraft1` — confirm which repo actually serves Pages, or the links (incl. `review/` deep links) will 404.
2. **Link health could not be batch-tested** from this sandbox (outbound HTTP for arbitrary domains is blocked; all curls return 000). The ~100 `officialSources` domains look plausible and the key ones were confirmed indirectly via search, but a link-checker run in CI is recommended. One known-suspect link: `discoverseoulpass.valuecom.com` (use the official domain).
3. The emergency print PDF (`research/sources/emergency/print/emergency-card.pdf`) embeds the same +82-2-3210-0404 mislabel — regenerate after fixing 1.2. *(Check `emergency-card.html` too.)*
4. `data/index.json` `emergency` block and `sw.js` cache lists were reviewed structurally only.

## 6. Priority fix list

| Priority | Action |
|---|---|
| P0 | Remove/flag the 175 fabricated restaurants and regenerate food.json + all 20 hotel itineraries + review HTML |
| P0 | Fix the +82-2-3210-0404 label in emergency contacts (md + print card) |
| P1 | Remove "Hard Rock Cafe Seoul"; re-source the DSP partner claims |
| P1 | events.json: event-30 status→TBA (Mulbit Yeonhwa); event-1 price→23,000; downgrade K-League "Confirmed" fixtures to TBA; timezone note on event-27 (Worlds final) |
| P1 | Update Busan Metro (1,600/1,800), premium/udeung bus fares, Seoul Sky 33,000 |
| P2 | Re-badge non-official sources in verification-log.md; fix single-ticket deposit wording; reconcile Pages URL/repo name; add 1345 immigration line |

---

## 7. FIXES APPLIED — 2026-08-18 remediation pass (all P0–P2 items closed)

| # | Fix | Files touched |
|---|---|---|
| 1 | **Deleted all 485 fabricated restaurants** and regenerated the food catalog (50 real venues), all 20 hotel itineraries, and the review HTML site | `restaurants-bookmarks.csv`, 5 city/route guides, `data/collections/food.json`, `seoul-hotel-itineraries/*`, `review/seoul-hotels/*` |
| 2 | **Corrected the +82-2-3210-0404 mislabel everywhere** (11 locations) — replaced with **1345 Immigration contact center** where a row was useful, plus an explanatory note that 0404 is MOFA's line for Korean nationals abroad; **print PDF stream patched and re-verified** | 8 emergency docs/checklists, `emergency-card.html`, `emergency-card.pdf`, `scripts/build_catalog.py`, `data/index.json` |
| 3 | **Removed "Hard Rock Cafe Seoul"** (closed 2018) from DSP partner claims; DSP link switched to the official `discoverseoulpass.com` | `tourist-promotions.md`, `verification-log.md` |
| 4 | **Mulbit Yeonhwa fall-2026 "Confirmed" claim retracted** at every layer (2026 edition ran Apr 24–May 3; no fall run announced): events.csv → TBA, fun/seoul.md §23, fun README timeline, fun itinerary checklist, `themes.json` evening blocks, trip-itineraries A12 & B15 evenings; all downstream pages rebuilt | 8 files + regenerated outputs |
| 5 | **events.csv corrections rebuilt into events.json:** Banksy adult price 18,000 → **23,000** (18,000 = youth/child); Seoul Sky 31,000 → **33,000**; "Chungnam Cheongju" → **Chungbuk Cheongju**; 4 K-League fixtures downgraded Confirmed → **TBA (verify on kleague.com)**; LoL Worlds watch-party timezone note (**Nov 14 US ET = early Nov 15 KST**); Korea Sale FESTA status now cites real 2025 dates (Oct 29–Nov 16) with 2026 unannounced | `research/sources/fun/events.csv`, `data/collections/events.json` |
| 6 | **Fare tables updated to current official levels:** Seoul subway flat **1,550** (since 28 Jun 2025) with correct single-ticket surcharge/deposit wording; Busan Metro **1,600/1,800** (since 3 May 2024); Seoul→Busan express-bus classes re-priced to published 2026 ranges (premium ~44,300–48,000 day / ~51,000–55,000 night; udeung ~33,900; ilban ~22,800–26,700); premium bus fixed in docs 04 & 12 and `routes.json` (was 39,800); AREX all-stop re-hedged | `transport/docs/04`, `05a`, `12`, `transport/data/routes.json` |
| 7 | **Seoul Sky 31,000 → 33,000** in the walking-maps guide as well | `fun/walking-maps.md` |
| 8 | **Source-tier honesty:** NamuWiki/Reddit/TikTok/press-sourced rows moved out of the "🟢 Official" table into 🟡 (5 rows) / 🔴 (Café H perk, no public source); KakaoTalk NamuWiki citation relabeled "community wiki, not official"; KSF-2026-dates assertion softened in both savings docs | `verification-log.md`, `tourist-promotions.md`, `birthday-freebies.md` |
| 9 | **README:** catalog count corrected (50 real food bookmarks, with a note about the removed padding), audit pass dated, Pages-URL repo-name caveat added; `CATALOG_DATE` bumped to 2026-08-18 | `README.md`, `scripts/build_catalog.py` |

**Post-fix sweep results:** zero fabricated venue names outside this report; zero 3210-0404 references outside corrective notes; all JSON parses; catalog counts (6/35/50/110/443/15/15/9/61/2) consistent between builder output, data files, and README; builds (`build_catalog.py`, `build_seoul_hotel_itineraries.py`, `build_itinerary_review.py`) all pass.

**Still open (cannot be resolved from this sandbox / before official announcements):** batch link-checking (outbound HTTP blocked — run a CI link checker); November K-League fixtures, Kimjang festivals, Everland/Lotte World Halloween end dates, Candlelight Hisaishi, MMCA Night, Noodle Daejeon Festival, and 2026 Korea Sale FESTA dates remain TBA items to re-verify at D-30 (late Sep 2026) as the repo's own checklists already schedule.
