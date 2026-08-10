# Seoul Hotel-Comparison — 20 Itineraries (index)

> Trip frame: **Sun, Nov 1, 2026, 21:00 → Sun, Nov 22, 2026, 13:00** · 21 nights · 2 adults (couple — just the two of you)
> Each plan assumes **one Seoul hotel as the base for the whole stay** — the point is to compare bases. The 20 themes are spread across the hotels marked `consider: true` in `hotel-options.json`.

| # | Itinerary | Hotel base | Pace | Focus | Best for |
| --- | --- | --- | --- | --- | --- |
| S01 | [Classic First-Timer Highlights](itineraries/classic-first-timer-highlights-at-nine-tree.md) | Nine Tree Myeongdong 1 | Moderate–full days | activities, fun, convenience | Her first Seoul trip (or yours together) and she wants the famous sights plus a real feel for the city. |
| S02 | [Shopping & Beauty Haul](itineraries/shopping-beauty-haul-at-nine-tree.md) | Nine Tree Myeongdong 1 | Market-paced — shop, compare, pack | value, fun, convenience | She wants the beauty/souvenir/fashion haul without decision fatigue or overpaying. |
| S03 | [Day-Trip Base Camp](itineraries/day-trip-base-camp-at-nine-tree.md) | Nine Tree Myeongdong 1 | Base-camp — big day out, calm day in | convenience, activities | She wants Seoul PLUS the famous outside-Seoul day trips without moving hotels or packing bags. |
| S04 | [Photo & Golden-Hour Loop](itineraries/photo-golden-hour-loop-at-nine-tree.md) | Nine Tree Myeongdong 1 | Early starts — golden & blue hour anchors | fun, activities | She shoots (phone or camera) and plans days around light. |
| S05 | [Romance & Date Night](itineraries/romance-date-night-at-nine-tree.md) | Nine Tree Myeongdong 1 | Polished — golden hours and good tables | fun, activities | The trip is partly a getaway — she wants a few properly romantic days. |
| S06 | [Market & Street-Food Crawl](itineraries/market-street-food-crawl-at-l7-myeongdong.md) | L7 Myeongdong | Grazing pace — meals are the anchors | value, fun | Food-first travelers — she wants to taste Seoul rather than tick sights. |
| S07 | [Nightlife & Late-Night Eats](itineraries/nightlife-late-night-eats-at-l7-myeongdong.md) | L7 Myeongdong | Late shift — slow mornings, late nights | fun, activities | Night owls — she wants Seoul's after-dark energy, not early palace gates. |
| S08 | [K-Culture & Pop-Up Circuit](itineraries/k-culture-pop-up-circuit-at-l7-myeongdong.md) | L7 Myeongdong | Late-ish — pop-ups, stages, and screen culture | fun, activities | K-culture fans — she wants the 'now' of Seoul: trends, idols, gaming, and stage culture. |
| S09 | [Slow Mornings & Spa Recharge](itineraries/slow-mornings-spa-recharge-at-l7-myeongdong.md) | L7 Myeongdong | Very gentle — one anchor per day, late starts | value, convenience | She wants to come home rested, not exhausted; recovery days between active ones. |
| S10 | [Fitness & Morning Runs](itineraries/fitness-morning-runs-at-l7-myeongdong.md) | L7 Myeongdong | Active — run/hike/walk first, sightsee after | activities, fun | She wants to keep the training habit on vacation (and earn the BBQ). |
| S11 | [Cafe & Dessert Hop](itineraries/cafe-dessert-hop-at-ibis-styles.md) | Ibis Styles Myeongdong | Cafe-paced — sit, sip, stroll | fun, value | She collects cafes and dessert shots; wants an Insta-worthy but unhurried Seoul. |
| S12 | [Museums & Galleries](itineraries/museums-galleries-at-ibis-styles.md) | Ibis Styles Myeongdong | Museum-paced — one ticketed anchor per day | activities, convenience | She reads every wall text and wants exhibitions over street crowds. |
| S13 | [Rainy-Day Indoor Plan](itineraries/rainy-day-indoor-plan-at-ibis-styles.md) | Ibis Styles Myeongdong | Weather-proof — indoors, connected by subway | convenience, activities | November drizzle/forecast says rain and she still wants a great day. |
| S14 | [Neighborhood Immersion](itineraries/neighborhood-immersion-at-ibis-styles.md) | Ibis Styles Myeongdong | Moderate — one neighborhood per half-day, no backtracking | activities, fun | Returners or curious travelers who prefer texture over tick-list sights. |
| S15 | [Night Market & Food Marathon](itineraries/night-market-food-marathon-at-ibis-styles.md) | Ibis Styles Myeongdong | Marathon — but it's eating, so it's fine | fun, value | Food maximalists — she plans days around where she'll eat at night. |
| S16 | [Palaces & Heritage Walk](itineraries/palaces-heritage-walk-at-skypark-myeongdong3.md) | Skypark Myeongdong 3 | Steady — one palace per morning, tea in the afternoons | activities, convenience | History and architecture lovers; nearly weather-proof because half the day is indoors. |
| S17 | [Han River & Parks](itineraries/han-river-parks-at-skypark-myeongdong3.md) | Skypark Myeongdong 3 | Outdoorsy but gentle — one park anchor per day | activities, fun, value | She wants fresh air and river views between the city days; loves a sunset picnic. |
| S18 | [Budget-Smart Seoul](itineraries/budget-smart-seoul-at-skypark-myeongdong3.md) | Skypark Myeongdong 3 | Moderate — wallet-first, free first | value, convenience | She wants the trip to feel rich without spending like it; great for the 'value' line of the comparison. |
| S19 | [Family & Kid-Friendly](itineraries/family-kid-friendly-at-skypark-myeongdong3.md) | Skypark Myeongdong 3 | Kid-paced — short walks, early dinners | fun, convenience, value | Traveling with children (or a partner who wants zero stress and maximum fun). |
| S20 | [Last-Day Convenience & Airport Flow](itineraries/last-day-convenience-airport-flow-at-skypark-myeongdong3.md) | Skypark Myeongdong 3 | Easy — zero panic, zero missed flights | convenience, value | The final 1–2 nights of the trip — this is the 'come home smooth' plan. |

## Regenerate

```bash
python3 scripts/build_seoul_hotel_itineraries.py
```

## How the split works

- 4 hotel(s) considered, themes per hotel: 5 × 5 × 5 × 5 = 20 total.
- Edit `hotel-options.json` (which hotels, why) and `themes.json` (the 20 themes) and re-run.