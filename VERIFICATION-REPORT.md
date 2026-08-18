# Independent verification report — line-by-line hallucination & fact audit

**Audit date:** 2026-08-18 (UTC) · **Auditor:** Arena.ai Agent Mode  
**Method:** Re-read the generated catalogs and source snapshots. Every *checkable, high-impact* claim (entry rules, emergency numbers, fares, named venues, dated events, hotel names, restaurant names) was checked against **official or primary published sources**, not against the previous in-repo report. The earlier 2026-08-18 report is **not treated as evidence** — it itself marked the AREX Express fare as “verified ₩11,000,” which official booking now contradicts.

> **Bottom line:** The hard logistics core (K-ETA waiver, e-Arrival Card, 112/119/1330, CSAT 19 Nov 2026, KTX ₩59,800, Climate Card tourist prices, most Nov 2026 concert/expo dates) is solid. This pass found **one remaining invented restaurant name**, **one event still marked as if it were a Hisaishi concert**, **one official fare the previous audit got wrong (AREX Express ₩13,000, not ₩11,000)**, **Korea VAT recorded as 7.5% instead of 10%**, **AREX last-train times mixed up with the all-stop**, and **systematic food-category mislabels** (a-la-carte BBQ tagged AYCE; naengmyeon/kalguksu tagged ramen). Those are fixed in source + regenerated catalog. Remaining dated sports fixtures and festival windows stay TBA on purpose.

---

## 1. Hallucinations / invented facts found on this pass

### 1.1 ❌ Invented restaurant: “Ramen Jiro Seoul / 라멘 지로 서울” (Yongsan) — **removed**

- **Where:** `research/sources/food/restaurants-bookmarks.csv`, `cities/seoul.md`, `cities/walking-food-routes.md` route S8, `data/collections/food.json` (`food-seoul-4`).
- **Fact:** Official Ramen Jiro (ラーメン二郎) has **no licensed Korea branch** (NamuWiki store list; Korea coverage is “지로계 / Jiro-*style*” independents). The well-known Seoul Jiro-style shop is **566라멘** in Yeonnam-dong, not a Yongsan shop called “Ramen Jiro Seoul.”
- **Fix applied:** replaced with **566 Ramen (566라멘), Yeonnam-dong**, labeled as Jiro-*style*, not an official Jiro.

### 1.2 ❌ “Candlelight: Joe Hisaishi” listed as a confirmed Hisaishi concert on 13 Nov 2026

- **Where:** `events.csv` event-18, `fun/seoul.md`, `fun/itinerary.md`, trip B12.
- **Fact:** Fever’s Candlelight series is a **rotating tribute** (string quartet playing Hisaishi / Ghibli repertoire). It is not a Joe Hisaishi concert. Recurring Jeongdong 1928 dates exist, but **13 Nov / 27 Nov 2026 were not independently verified** on Fever at audit time.
- **Fix applied:** status → **TBA**; title now says “Ghibli tribute”; notes say to check feverup.com.

### 1.3 ❌ Shin Old Tea House described as a “130-year tea house”

- **Where:** `research/sources/food/cities/seoul.md`.
- **Fact:** The *business* has operated since about **1992**. Local reviews say the *hanok building* is old (~100 years). Calling the tea house itself 130 years old is false.
- **Fix applied:** wording corrected.

### 1.4 ❌ Sutgol Won Naengmyeon called “100-year heritage (1954)”

- **Where:** walking-food-routes.md route D2.
- **Fact:** Founded **1954** → ~70 years in 2026, not 100. Korean write-ups say “70년 전통.”
- **Fix applied:** “since 1954 / ~70-year.”

### 1.5 ❌ Geumdwaeji Sikdang called “Michelin-starred”

- **Where:** walking-food-routes.md route S9.
- **Fact:** It is a **Bib Gourmand**, not a starred restaurant.
- **Fix applied.**

### 1.6 ⚠️ Previous in-repo report labeled AREX Express ₩11,000 “verified correct”

That was wrong. Official AREX booking (`airportrailroad.com`) lists **Adult ₩13,000 / member ₩12,500**. Third-party 2026 guides match that on-site fare; Klook/KKDay/Creatrip sell ~₩11,400–11,600. The ₩11,000 figure is a stale official fare.

---

## 2. Incorrect / outdated facts (this pass)

| # | Claim in repo (before fix) | Official / current | Severity | Status |
|---|---|---|---|---|
| 2.1 | AREX Express **₩11,000** | Official adult one-way **₩13,000** (member ₩12,500) on AREX booking | High | **Fixed** |
| 2.2 | AREX all-stop **₩4,450** | Distance fare after Jun 2025 hike ≈ **₩4,750 T1 / up to ~₩5,350 T2** | Med | **Fixed** (hedged) |
| 2.3 | Tax-refund `vat_rate_percent: 7.5` | Korea VAT is **10%**. Tourists typically net **~5–8%** after operator fees | High | **Fixed** to 10 + fee note |
| 2.4 | AREX Express last train **~23:32** | Express last ≈ **22:40 T2 / 22:48 T1** (2026 published). 23:32 is the later *all-stop* window | High (arrival night) | **Fixed** |
| 2.5 | WOWPASS issuance **₩5,000** | Kiosk fee raised **Mar 2026** to ~**₩6,000** (app ~₩5,500) | Low-Med | **Fixed** (hedged) |
| 2.6 | Premium Seoul→Busan bus 2-pax still **₩79,600** in logistics | Inconsistent with the updated ₩44,300/person route (should be **₩88,600**) | Low | **Fixed** |
| 2.7 | Food categories: Geumdwaeji / Daedo / Yukjeon / Nari / Jeong Daepo / Haeundae Amso / Busan Jokbal tagged **AYCE BBQ**; Sariwon tagged **jajangmyeon**; Sutgol/Ossi/Boksu/Gijang tagged **ramen** | Those are a-la-carte BBQ, jokbal, naengmyeon/kalguksu/bunsik — not AYCE or ramen | Med (planning error) | **Fixed** in CSV + seoul.md |
| 2.8 | Food README “**57** highly verified restaurants” | Bookmark list is **50** | Low | **Fixed** |
| 2.9 | Myeongdong Kyoja “Michelin Bib (1966–2026)” | **1966 is the founding year**, not the Michelin span | Low | **Fixed** |
| 2.10 | JTBC Marathon entry “~₩100,000” | 2026 full **₩150,000** / 10K **₩100,000** (Korean press) | Low | Noted; still labeled approx |
| 2.11 | Busan Biennale “46 artists / 22 countries” | Organizers: **44 artists/collectives from 23 countries** (more TBA) | Low | Noted, not blocking |
| 2.12 | N Seoul Tower observatory **₩21,000** | Historical official adult price. Some 2026 third-party guides quote **₩29,000 onsite**. Official `nseoultower.co.kr` / `seoultower.co.kr` not independently scraped here | Low | Hedged in DSP break-even note |

---

## 3. Verified correct against official / primary sources

### Entry & safety

| Claim | Source |
|---|---|
| US citizens visa-free 90 days; **K-ETA exemption through 31 Dec 2026 (KST)** | Consulate General of the ROK in New York notice: [newyork.mofa.go.kr](https://newyork.mofa.go.kr/us-newyork-en/brd/m_25545/view.do?seq=21) |
| **e-Arrival Card** required from **1 Jan 2026**, submit within 3 days / valid 72 h, free, `e-arrivalcard.go.kr`; K-ETA holders exempt | EY tax alert 11 Dec 2025; Korean government / travel-industry summaries of the MOJ rule |
| **112** police · **119** fire/ambulance · **1330** KTO helpline English **24/7** (`+82-2-1330` from abroad) | [knto.or.kr 1330 page](https://knto.or.kr/eng/1330KoreaTravelHelpline); VisitKorea |
| **1345** Hi Korea immigration contact center (weekday hours) | Hi Korea / MOJ |
| **+82-2-397-4114** U.S. Embassy Seoul, **188 Sejong-daero, Jongno-gu** | [kr.usembassy.gov/contact-us](https://kr.usembassy.gov/contact-us/) |
| **+82-2-3210-0404** is MOFA consular line for **Korean nationals abroad**, not a tourist emergency line | Already correctly footnoted after the first pass |
| **CSAT / 2027학년도 수능 = Thursday 19 Nov 2026** | KICE “2027 CSAT Basic Implementation Plan” (Mar 2026); MOE |
| No Korean public holidays 1–22 Nov 2026; 1 Nov = Sunday, 22 Nov = Sunday | Calendar |

### Transport

| Claim | Source |
|---|---|
| KTX Seoul–Busan standard **₩59,800** / first **₩83,700**, ~2 h 15–2 h 45 | Seat61; Korail fare tables widely republished; consistent across 2026 guides |
| SRT Suseo–Busan **₩52,600** | SRT / travel guides |
| Climate Card tourist: **1d ₩5,000 / 2d ₩8,000 / 3d ₩10,000 / 5d ₩15,000** | [Seoul Metropolitan Government](https://english.seoul.go.kr/seoul-launches-climate-card-tourist-pass-with-1-2-3-and-5-day-options-starting-in-july/) |
| Seoul subway adult card **₩1,550** since **28 Jun 2025** | Seoul Metropolitan Government / Korea JoongAng Daily 21 Jun 2025 |
| Busan Metro card **₩1,600 / ₩1,800** (zone 1/2) | [Humetro English fare pages](https://work.humetro.busan.kr/homepage/english/page/subLocation.do?menu_no=100601040202) |
| Tax refund min **₩15,000**, immediate-refund ceiling **₩1,000,000**/txn | VisitKorea tax-refund guidance |
| KORAIL Saver 2-day flexible **₩121,000**/person (2–5 travelers) | 2026 Korail Pass price tables |
| Discover Seoul Pass 72 h **₩90,000** (Pick 3 Basic ₩49,000 / Theme ₩70,000 / 120 h ₩130,000 also on official schema) | [discoverseoulpass.com](https://discoverseoulpass.com/index.php/en) |
| Visit Busan Pass 24 h **₩55,000** / 48 h **₩85,000** | Common published VBP prices (confirm on visitbusanpass.com at purchase) |
| Gyeongbokgung adult **₩3,000**, free in full hanbok; Nov hours **09:00–17:00**, closed Tue | VisitSeoul official palace page |
| Seoul Sky adult **₩33,000** | [seoulsky.lotteworld.com/price](https://seoulsky.lotteworld.com/price/info/ticket) |

### November 2026 dated events (independently confirmed)

| Event | Dates / venue | Source |
|---|---|---|
| BANKSY: Still Here | 22 Jul–3 Nov 2026, The Hyundai Seoul ALT.1; adult **₩23,000** / youth **₩18,000** | [VisitSeoul exhibition page](https://english.visitseoul.net/exhibition/BANKSY-still-here/ENPx0x7wx) |
| My Chemical Romance | **7 Nov**, Paradise City, Incheon | Songkick / venue listings; Asia tour pages |
| Jujutsu Kaisen in Concert | **7–8 Nov**, Kyung Hee Grand Peace Palace | Official tour site + NOL |
| KGMA 2026 | **7–8 Nov**, Gocheok Sky Dome | Organizer announcement 18 Mar 2026 |
| Sir Simon Rattle & BRSO | **12–13 Nov**, Seoul Arts Center Concert Hall | [sac.or.kr show page](https://www.sac.or.kr/site/main/show/show_view?SN=77520) |
| Jason Mraz | **14 Nov**, KINTEX | [jasonmraz.com/asia-2026-tour](https://jasonmraz.com/asia-2026-tour/) |
| Melon Music Awards | **14–15 Nov**, Gocheok Sky Dome | Kakao Ent. / Melon 9 Jun 2026 |
| Kings of Convenience | **18 Nov**, Sejong Center | YES24 Ticket English |
| 5 Seconds of Summer | **19 Nov**, KINTEX Hall 1 | Sports Khan / setlist.fm (fan wiki Hall 9 is the outlier) |
| G-STAR 2026 | **19–22 Nov**, BEXCO | Organizing committee / gstar.or.kr |
| MAMA 2026 | **20–21 Nov**, Kyocera Dome Osaka (stream) | [CJ ENM](https://newsroom.cj.net/2026-mama-awards-to-take-place-in-japan-from-november-20-21/) |
| JTBC Seoul Marathon | **1 Nov**, Sangam start 07:30 | [en.marathon.jtbc.com](http://en.marathon.jtbc.com/) |
| Daejeon International Wine EXPO | **6–8 Nov**, DCC | [djwinefair.com/eng/0501](https://djwinefair.com/eng/0501) |
| Busan Biennale “Dissident Chorus” | **29 Aug–1 Nov**, MoCA + Space Wonji + former Nam High | Biennale organizing committee |
| Seoul Outdoor Library | **23 Apr–1 Nov 2026** | [VisitSeoul](https://english.visitseoul.net/events/2026SeoulOutdoorLibrary/ENPvro3vg) |
| V-League 2026–27 | Regular season **31 Oct 2026 – 2 Apr 2027** | KOVO schedule release 18 Aug 2026 (Korean press) |
| LoL Worlds final | **14 Nov**, Barclays Center, Brooklyn (US ET → early **15 Nov KST**) | Riot / Inven Global |
| Musical *Elisabeth* | 16 Aug–15 Nov, Blue Square | NOL |
| Musical *Hell’s Kitchen* | 24 Jul–8 Nov, GS Arts Center | NOL |
| Musical *Gwanghwamun Love Song* | 6 Sep–15 Nov, D-CUBE LINK | NOL |
| Musical *Dear Evan Hansen* | 1 Aug–1 Nov, Chungmu Arts Center | NOL |
| Leeum *Inside Other Spaces* | 5 May–29 Nov | leeumhoam.org |
| MMCA × LG OLED Christine Sun Kim | 31 Jul–29 Nov, Seoul Box | MMCA / Korea Herald |
| Culture Flowing Through Seoul Plaza | Wednesdays May–Dec (so **4 / 11 / 18 Nov** are in-window) | [english.seoul.go.kr](https://english.seoul.go.kr/seoul-launches-citywide-outdoor-performances-musicals-at-seoul-plaza-opera-by-the-han-river/) |

**Busan Fireworks 7 Nov 2026:** widely reported as Saturday 7 Nov (first-Saturday pattern) on travel sites that cite busanfireworks.com. Treat as **highly likely** but re-open the official page before locking hotels — the event has moved dates before.

### Hotels (35) and restaurants (50)

- All **35 hotel names** are real properties (Lotte L7, Nine Tree Parnas, ibis Styles/Insadong, Four Seasons, Fairmont Ambassador, Shilla Stay Haeundae/Cheonan, ASTI Busan Station, Grand Josun, Park Hyatt Busan, Hwangnamkwan, Commodore, Lahan Select, Hilton Gyeongju, GG Hotel, Ramada Encore Cheonan/Haeundae, ON City, Sono Belle, Best Western Asan, Toyoko Inn Daejeon/Haeundae 2, Ramada Daejeon, Lotte City Daejeon, Benikea Daelim, Hotel Stendhal, Brown Dot Cheonan Station, The Mains, Interciti, Aank Air, Skypark Myeongdong 3, Four Points Josun Seoul Station, L’Escape). Nightly USD bands are **estimates**, correctly labeled.
- Remaining **50 food bookmarks** are real named businesses (VisitKorea / VisitSeoul / VisitBusan / brand sites / Naver Map). Category labels that were wrong are corrected. **Michelin year-spans** should be re-checked against the current MICHELIN Guide Korea PDF before anyone treats “still Bib in 2026” as a booking fact.

---

## 4. Still TBA / not independently lockable

Keep these as TBA/Watch (already labeled, or should stay labeled):

- K League 2 named fixtures (E-Land vs Jeonnam 7 Nov, vs Asan 22 Nov; Cheonan City vs Busan IPark 8 Nov; IPark vs Chungbuk Cheongju 21 Nov).
- Korea Sale FESTA 2026 dates (2025 was 29 Oct–16 Nov).
- Seoul Kimjang / aT Kimjang Grand Festival 2026 dates.
- Lotte World / Everland Halloween 2026 end dates.
- Changdeokgung Moonlight Tour fall 2026 window.
- MMCA Night November edition.
- Noodle Daejeon Festival; O-World chrysanthemum window.
- KBL / WKBL 2026–27 tip-off dates.
- KBO Korean Series participants.
- Hotel “typical 2026” nightly USD bands.
- N Seoul Tower **current** onsite adult price (₩21,000 vs reported ₩29,000).
- Climate Card **7-day** tourist SKU — official 2024 SMG launch listed 1/2/3/5 day only; some 2026 blogs add ₩20,000 / 7-day. Confirm at the station desk.
- Discover Seoul Pass **24 h / 48 h** physical SKUs — official site schema now leads with Pick 3 / 72 h / 120 h.

---

## 5. What this pass changed in the repo

| Fix | Files |
|---|---|
| AREX Express **₩13,000** official; all-stop hedged **~₩4,750** | `transport/data/routes.json`, `logistics_rules.json`, docs 05a / 06 / 19 |
| Express last-train **~22:40 T2**, not 23:32 | emergency 01 / 07 / 10, README, during-trip checklist, docs index |
| VAT **10%** + fee note | `tax_refund.json` |
| WOWPASS issuance **~₩6,000** | `cards.json` |
| Logistics premium-bus 2-pax **₩88,600** | `logistics_rules.json` |
| Deleted invented **Ramen Jiro Seoul**; replaced with **566라멘** | food CSV, seoul.md, walking-food-routes.md |
| AYCE / ramen / jajangmyeon category corrections | food CSV + seoul.md note |
| Hisaishi tribute **TBA** | events.csv, fun/seoul.md, fun/itinerary.md |
| Shin Old Tea House / Sutgol / “Michelin-starred” wording | seoul.md, walking-food-routes.md |
| Regenerated planner catalog | `python3 scripts/build_catalog.py` → `data/index.json`, `data/collections/*` |

Catalog counts after rebuild: **6 sources · 35 hotels · 50 food · 110 events · 443 activities · 15 places · 15 routes · 9 apps · 61 savings · 2 blueprints.**

---

## 6. Honest limits

- Outbound HTTP to arbitrary official sites is blocked in this sandbox; verification used the search/fetch tools against government, operator, and ticketing domains (MOFA NY, US Embassy, SMG, Humetro, AREX booking, SAC, CJ ENM, JTBC marathon, VisitSeoul, Seoul Sky, KICE press).
- A CI link-checker is still recommended. `royal.cha.go.kr` in some destination rows is the old CHA host; Korea Heritage Service now uses **royal.khs.go.kr**.
- Menu prices and hours in the food city tables were **not** re-ticketed line by line against today’s Naver listings. Names and existence were the hallucination test; prices remain “re-check before you go.”
- The 30 trip-itineraries and 20 hotel-comparison plans are **planning narratives** built on this research. They inherit any leftover TBA items (K-League, Hisaishi tribute, festival windows). They no longer recommend the invented Jiro shop.

**Still do this at D-30 (late Sep 2026):** official AREX timetable for the 21:00 arrival night, K League November round, Korea Sale FESTA, fireworks official PDF, N Seoul Tower ticket page, and every restaurant hour on Naver Map.
