# Seoul Hotel-Comparison — 20 Itineraries (index)

> Trip frame: **Sun, Nov 1, 2026, 21:00 → Sun, Nov 22, 2026, 13:00** · 21 nights · 2 adults (couple — just the two of you)
> Each plan assumes **one Seoul hotel as the base for the whole stay** — the point is to compare bases. The 20 themes are spread across the hotels marked `consider: true` in `hotel-options.json`.

| # | Itinerary | Hotel base | Pace | Focus | Best for |
| --- | --- | --- | --- | --- | --- |
| S01 | [Classic First-Timer Highlights](itineraries/classic-first-timer-highlights-at-four-points-josun-station.md) | Four Points Seoul Station | Moderate–full days | activities, fun, convenience | You two, first time in Seoul — want the greatest hits without rushing, with time to linger together. |
| S02 | [Cafe & Dessert Hop](itineraries/cafe-dessert-hop-at-four-points-josun-station.md) | Four Points Seoul Station | Cafe-paced — sit, sip, stroll | fun, value | For two cafe lovers — slow mornings, beautiful spaces, dessert second-dates in every neighborhood. |
| S03 | [Shopping & Beauty Haul](itineraries/shopping-beauty-haul-at-four-points-josun-station.md) | Four Points Seoul Station | Market-paced — shop, compare, pack | value, fun, convenience | You two want to shop smart together — beauty, souvenirs, and gift hunting with easy hotel drop-offs. |
| S04 | [Museums & Galleries](itineraries/museums-galleries-at-four-points-josun-station.md) | Four Points Seoul Station | Museum-paced — one ticketed anchor per day | activities, convenience | You two enjoy museums at your own pace — one thoughtful exhibition a day, no crowds to battle. |
| S05 | [Day-Trip Base Camp](itineraries/day-trip-base-camp-at-four-points-josun-station.md) | Four Points Seoul Station | Base-camp — big day out, calm day in | convenience, activities | You two want one easy day trip from Seoul and still sleep in the same bed that night. |
| S06 | [Rainy-Day Indoor Plan](itineraries/rainy-day-indoor-plan-at-four-points-josun-station.md) | Four Points Seoul Station | Weather-proof — indoors, connected by subway | convenience, activities | You two want a weather-proof plan — malls, museums, and a warm jjimjilbang evening. |
| S07 | [Photo & Golden-Hour Loop](itineraries/photo-golden-hour-loop-at-four-points-josun-station.md) | Four Points Seoul Station | Early starts — golden & blue hour anchors | fun, activities | You two love golden-hour photos together — palaces, river, and neon at blue hour. |
| S08 | [Neighborhood Immersion](itineraries/neighborhood-immersion-at-four-points-josun-station.md) | Four Points Seoul Station | Moderate — one neighborhood per half-day, no backtracking | activities, fun | You two want neighborhood texture — alleys, cafes, and local streets without backtracking. |
| S09 | [Romance & Date Night](itineraries/romance-date-night-at-four-points-josun-station.md) | Four Points Seoul Station | Polished — golden hours and good tables | fun, activities | You two want a proper date — sunset tower, nice dinner, night walk, river cruise. |
| S10 | [Night Market & Food Marathon](itineraries/night-market-food-marathon-at-four-points-josun-station.md) | Four Points Seoul Station | Marathon — but it's eating, so it's fine | fun, value | You two want to eat your way through Seoul at night — market stalls to late BBQ, together. |
| S11 | [Market & Street-Food Crawl](itineraries/market-street-food-crawl-at-ibis-styles.md) | Ibis Styles Myeongdong | Grazing pace — meals are the anchors | value, fun | You two love to eat together — markets and street-food alleys at a grazing, hand-in-hand pace. |
| S12 | [Palaces & Heritage Walk](itineraries/palaces-heritage-walk-at-ibis-styles.md) | Ibis Styles Myeongdong | Steady — one palace per morning, tea in the afternoons | activities, convenience | You two want classic Seoul history together — palaces by morning, tea houses by afternoon. |
| S13 | [Nightlife & Late-Night Eats](itineraries/nightlife-late-night-eats-at-ibis-styles.md) | Ibis Styles Myeongdong | Late shift — slow mornings, late nights | fun, activities | You two want Seoul after dark — neon alleys, a show, late-night eats, cozy walk home together. |
| S14 | [Han River & Parks](itineraries/han-river-parks-at-ibis-styles.md) | Ibis Styles Myeongdong | Outdoorsy but gentle — one park anchor per day | activities, fun, value | You two want fresh air together — Han River picnics, sunset views, gentle bike rides. |
| S15 | [K-Culture & Pop-Up Circuit](itineraries/k-culture-pop-up-circuit-at-ibis-styles.md) | Ibis Styles Myeongdong | Late-ish — pop-ups, stages, and screen culture | fun, activities | You two are K-culture curious — pop-ups, music, and playful photo spots together. |
| S16 | [Budget-Smart Seoul](itineraries/budget-smart-seoul-at-ibis-styles.md) | Ibis Styles Myeongdong | Moderate — wallet-first, free first | value, convenience | You two want it to feel rich without overspending — free gems, market meals, smart value. |
| S17 | [Slow Mornings & Spa Recharge](itineraries/slow-mornings-spa-recharge-at-ibis-styles.md) | Ibis Styles Myeongdong | Very gentle — one anchor per day, late starts | value, convenience | You two need to actually recharge — late starts, spas, tea houses, unhurried wandering. |
| S18 | [Family & Kid-Friendly](itineraries/family-kid-friendly-at-ibis-styles.md) | Ibis Styles Myeongdong | Kid-paced — short walks, early dinners | fun, convenience, value | You two want an easy, low-stress rhythm — gentle walks, early dinners, relaxed evenings together. |
| S19 | [Fitness & Morning Runs](itineraries/fitness-morning-runs-at-ibis-styles.md) | Ibis Styles Myeongdong | Active — run/hike/walk first, sightsee after | activities, fun | You two want to move together — sunrise riverside stroll, easy hike, then big lunch. |
| S20 | [Last-Day Convenience & Airport Flow](itineraries/last-day-convenience-airport-flow-at-ibis-styles.md) | Ibis Styles Myeongdong | Easy — zero panic, zero missed flights | convenience, value | You two on your last nights — easy shopping, farewell dinner, smooth airport send-off. |

## Regenerate

```bash
python3 scripts/build_seoul_hotel_itineraries.py
```

## How the split works

- 2 hotel(s) considered, themes per hotel: 10 × 10 = 20 total.
- Edit `hotel-options.json` (which hotels, why) and `themes.json` (the 20 themes) and re-run.