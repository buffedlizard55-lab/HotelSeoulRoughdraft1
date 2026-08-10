# Seoul Hotel-Comparison — 20 Itineraries (index)

> Trip frame: **Sun, Nov 1, 2026, 21:00 → Sun, Nov 22, 2026, 13:00** · 21 nights · 2 adults (couple — just the two of you)
> Each plan assumes **one Seoul hotel as the base for the whole stay** — the point is to compare bases. The 20 themes are spread across the hotels marked `consider: true` in `hotel-options.json`.

| # | Itinerary | Hotel base | Pace | Focus | Best for |
| --- | --- | --- | --- | --- | --- |
| S01 | [Classic First-Timer Highlights](itineraries/classic-first-timer-highlights-at-four-points-josun-station.md) | Four Points Seoul Station | Moderate–full days | activities, fun, convenience | Her first Seoul trip (or yours together) and she wants the famous sights plus a real feel for the city. |
| S02 | [Cafe & Dessert Hop](itineraries/cafe-dessert-hop-at-four-points-josun-station.md) | Four Points Seoul Station | Cafe-paced — sit, sip, stroll | fun, value | She collects cafes and dessert shots; wants an Insta-worthy but unhurried Seoul. |
| S03 | [Shopping & Beauty Haul](itineraries/shopping-beauty-haul-at-four-points-josun-station.md) | Four Points Seoul Station | Market-paced — shop, compare, pack | value, fun, convenience | She wants the beauty/souvenir/fashion haul without decision fatigue or overpaying. |
| S04 | [Museums & Galleries](itineraries/museums-galleries-at-four-points-josun-station.md) | Four Points Seoul Station | Museum-paced — one ticketed anchor per day | activities, convenience | She reads every wall text and wants exhibitions over street crowds. |
| S05 | [Day-Trip Base Camp](itineraries/day-trip-base-camp-at-four-points-josun-station.md) | Four Points Seoul Station | Base-camp — big day out, calm day in | convenience, activities | She wants Seoul PLUS the famous outside-Seoul day trips without moving hotels or packing bags. |
| S06 | [Rainy-Day Indoor Plan](itineraries/rainy-day-indoor-plan-at-four-points-josun-station.md) | Four Points Seoul Station | Weather-proof — indoors, connected by subway | convenience, activities | November drizzle/forecast says rain and she still wants a great day. |
| S07 | [Photo & Golden-Hour Loop](itineraries/photo-golden-hour-loop-at-four-points-josun-station.md) | Four Points Seoul Station | Early starts — golden & blue hour anchors | fun, activities | She shoots (phone or camera) and plans days around light. |
| S08 | [Neighborhood Immersion](itineraries/neighborhood-immersion-at-four-points-josun-station.md) | Four Points Seoul Station | Moderate — one neighborhood per half-day, no backtracking | activities, fun | Returners or curious travelers who prefer texture over tick-list sights. |
| S09 | [Romance & Date Night](itineraries/romance-date-night-at-four-points-josun-station.md) | Four Points Seoul Station | Polished — golden hours and good tables | fun, activities | The trip is partly a getaway — she wants a few properly romantic days. |
| S10 | [Night Market & Food Marathon](itineraries/night-market-food-marathon-at-four-points-josun-station.md) | Four Points Seoul Station | Marathon — but it's eating, so it's fine | fun, value | Food maximalists — she plans days around where she'll eat at night. |
| S11 | [Market & Street-Food Crawl](itineraries/market-street-food-crawl-at-ibis-styles.md) | Ibis Styles Myeongdong | Grazing pace — meals are the anchors | value, fun | Food-first travelers — she wants to taste Seoul rather than tick sights. |
| S12 | [Palaces & Heritage Walk](itineraries/palaces-heritage-walk-at-ibis-styles.md) | Ibis Styles Myeongdong | Steady — one palace per morning, tea in the afternoons | activities, convenience | History and architecture lovers; nearly weather-proof because half the day is indoors. |
| S13 | [Nightlife & Late-Night Eats](itineraries/nightlife-late-night-eats-at-ibis-styles.md) | Ibis Styles Myeongdong | Late shift — slow mornings, late nights | fun, activities | Night owls — she wants Seoul's after-dark energy, not early palace gates. |
| S14 | [Han River & Parks](itineraries/han-river-parks-at-ibis-styles.md) | Ibis Styles Myeongdong | Outdoorsy but gentle — one park anchor per day | activities, fun, value | She wants fresh air and river views between the city days; loves a sunset picnic. |
| S15 | [K-Culture & Pop-Up Circuit](itineraries/k-culture-pop-up-circuit-at-ibis-styles.md) | Ibis Styles Myeongdong | Late-ish — pop-ups, stages, and screen culture | fun, activities | K-culture fans — she wants the 'now' of Seoul: trends, idols, gaming, and stage culture. |
| S16 | [Budget-Smart Seoul](itineraries/budget-smart-seoul-at-ibis-styles.md) | Ibis Styles Myeongdong | Moderate — wallet-first, free first | value, convenience | She wants the trip to feel rich without spending like it; great for the 'value' line of the comparison. |
| S17 | [Slow Mornings & Spa Recharge](itineraries/slow-mornings-spa-recharge-at-ibis-styles.md) | Ibis Styles Myeongdong | Very gentle — one anchor per day, late starts | value, convenience | She wants to come home rested, not exhausted; recovery days between active ones. |
| S18 | [Family & Kid-Friendly](itineraries/family-kid-friendly-at-ibis-styles.md) | Ibis Styles Myeongdong | Kid-paced — short walks, early dinners | fun, convenience, value | Traveling with children (or a partner who wants zero stress and maximum fun). |
| S19 | [Fitness & Morning Runs](itineraries/fitness-morning-runs-at-ibis-styles.md) | Ibis Styles Myeongdong | Active — run/hike/walk first, sightsee after | activities, fun | She wants to keep the training habit on vacation (and earn the BBQ). |
| S20 | [Last-Day Convenience & Airport Flow](itineraries/last-day-convenience-airport-flow-at-ibis-styles.md) | Ibis Styles Myeongdong | Easy — zero panic, zero missed flights | convenience, value | The final 1–2 nights of the trip — this is the 'come home smooth' plan. |

## Regenerate

```bash
python3 scripts/build_seoul_hotel_itineraries.py
```

## How the split works

- 2 hotel(s) considered, themes per hotel: 10 × 10 = 20 total.
- Edit `hotel-options.json` (which hotels, why) and `themes.json` (the 20 themes) and re-run.