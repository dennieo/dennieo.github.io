Source: https://imdennie.com/case/veylo.html

Updated: 2026-10-12

Navigation · iOS · Founder product

# A navigator that never guesses where you are.

Veylo is an iPhone navigator for Kyiv and Kyiv oblast, where satellite positioning is jammed and spoofed. It asks the driver before it trusts the dot, keeps the directions going as manual steps when it can’t, and runs the map, routing and address search on the phone itself.

- **Role** · Founder, Product Designer & Engineer
- **Timeline** · October 2026 → App Store
- **Platform** · iOS 26 · SwiftUI · CarPlay
- **Scope** · Map, routing, search, guidance
- **Team** · Solo, with AI tooling
- **Status** · In development, pre-release

[ How it was built ](https://imdennie.com/case/veylo.html#build) [App support](https://imdennie.com/veylo/support/)

![Veylo route options across Kyiv beside a manual-steps turn card, on two phones against pale blue](https://imdennie.com/dist/img/covers/open-studio/veylo.webp)

**01** — What I built and how I used AI

## A map, a router and a search engine that live on the phone.

Veylo is a native iPhone app with its own offline map, its own router and its own address search. There is no AI inside the product — routes and position checks are deterministic code — but it was built with AI-assisted development. This section keeps the two apart.

My responsibility: Product definition, UX and UI, the position-trust model, guidance and manual steps, the on-device router, the offline map pipeline, address search, CarPlay and the App Store kit.

Implementation: SwiftUI for iOS 26 with Liquid Glass. MapLibre Native draws OpenStreetMap vector tiles shipped inside the app. A road graph of Kyiv oblast is built from OpenStreetMap in CI and routed on the phone. The address index is built on the device from the same data. StoreKit 2 handles purchases on the device, with no server of my own.

AI-assisted development: Claude Code wrote first implementations from my specs and written decision records. A Python reference router is the specification: CI fails unless the Swift router returns the same routes on a test grid and on real routes across the oblast. Independent AI review passes read every change; one caught the typed address leaking into the system log and online answers cached on disk, both fixed before merge.

My review and decisions: Never act on a position the driver has not confirmed; what replaces live guidance when trust drops; which numbers may be shown without a position; what goes to the internet and what never leaves the phone; which thresholds stay proposals until they are measured in a car.

Release status: In development. Checked in the iOS simulator and installed on an iPhone; not yet tested on the road or in a CarPlay car. Trust thresholds are proposals until measured. [App support](https://imdennie.com/veylo/support/)

One build loop, start to finish

1. **Rough flow.** Confirm where you are → choose where to → compare routes → follow the turns.
2. **AI-generated first implementation.** A native app with an Apple-Maps-style sheet, on-device routes and turn-by-turn voice in Ukrainian, generated from that flow and the decision records.
3. **What I decided.** In Kyiv a spoofed fix can be kilometres off and still report ±5 m, so a navigator that silently follows the dot will confidently lead you wrong. Trust became one state the whole interface reads — the chip, the location button, the dot and the guidance card. When it drops, live guidance becomes “Кроки вручну”: the route’s turns as printed directions that only the driver advances.
4. **Working result.** Search an address or long-press the map, compare up to three routes, start. With a spoofed position, the app shows the turns one by one with “Назад” and “Далі” and frames each turn on the map.

**A limitation I designed around:** without a trusted position, a missed turn is invisible. Manual steps never pretend otherwise — no arrival time, distances labelled “from the shown turn”, nothing advancing on a timer, and a note that a passenger should step through the turns.

**02** — The problem

## In Kyiv the blue dot can lie — and most navigators believe it.

Electronic warfare jams and spoofs satellite positioning across the city. A phone can report a position across the river with confident accuracy, or freeze in the middle of a turn. Navigation apps follow it, reroute into nonsense, and drivers learn to ignore them exactly when they need help.

- The dot jumps kilometres or freezes mid-turn
- Rerouting follows the fake position, not the car
- A spoofed fix still shows “accuracy ±5 m”
- Mobile internet drops, and online maps go blank
- In my experience, new roads reach some maps late

**03** — Product thinking

## Three bets that shaped the app.

01

### Never guess a position

The driver confirms where they are. Jumps, impossible speeds, simulated or stale fixes and positions outside the oblast withdraw that trust, and the app says why.

02

### Everything on the phone

Map, routing and address search work with no server and no internet. A connection only adds online search results on top.

03

### Keep the directions

When the position can’t be trusted, the route becomes manual steps the driver advances — like printed directions, never on a timer.

**04** — Key UX & UI decisions

## Where it became a real product.

Position · trust

### “Is this your location?” before anything else

On launch Veylo shows where the phone thinks it is and asks. A simulated position can’t be confirmed at all; a jump or a coarse fix explains what is wrong and offers to pick the start on the map instead. The same state drives the chip at the top, the location button and the style of the dot.

**Why it works:** the driver, who can see the street, is a better judge of the position than satellites that can’t be trusted.

![Veylo position check reporting a spoofed position near Khreshchatyk, offering to pick the start on the map](https://imdennie.com/dist/img/veylo/device-position-check.webp)

Guidance · no trusted position

### Printed directions, one turn at a time

Without a trusted position the guidance card becomes “Кроки вручну”: the turn, the street, how far it is from the previous one, what comes next, and a wide “Далі”. The map frames the turn with an arrow. The bottom row shows distance and time from the shown turn — never an arrival time the app can’t know.

**Why it works:** the driver stays oriented, and nothing on screen pretends to know where the car is.

![Veylo manual-steps card: turn left onto Obolonskyi Avenue, with Back and Next buttons and the turn arrow on the map](https://imdennie.com/dist/img/veylo/device-manual-step.webp)

Planning

### Long-press anywhere, then Go — or Steps

A long press drops a pin with “Маршрут сюди” and “Звідси”, the fastest way to a place with no address, and it works offline. Up to three routes appear with their time differences on the map. The green “Поїхали” shows only with a confirmed position; otherwise the same button reads “Кроки”, as Apple Maps offers Steps for a route that doesn’t start where you are.

**Why it works:** the button tells the truth about what will happen before the drive starts.

![Veylo route options across Kyiv with 18, 19 and 22 minute callouts and a Steps button](https://imdennie.com/dist/img/veylo/device-routes.webp)

Search · offline first

### Search that works without signal

The index is built on the phone from the map inside the app: streets, house numbers, towns, districts, shops and stations. It tolerates Ukrainian and Russian spellings, Latin transliteration, the wrong keyboard layout and typos. With internet, online results merge in without duplicates; only the typed text and a point rounded to about a kilometre are sent.

**Why it works:** the moment you need an address is often the moment the signal is gone.

![Veylo search for Khreshchatyk 22 with house, street, station and district results](https://imdennie.com/dist/img/veylo/device-search.webp)

Map · day and night

### A map made for glances

Guidance switches to a driving style: grey ground, white streets, amber main roads and larger street names, built for contrast in sunlight. At night the same map turns dark, and the cards follow the system appearance.

**Why it works:** at 50 km/h the map gets a glance, not a read; contrast does the work.

![Veylo manual-steps card on the dark night map](https://imdennie.com/dist/img/veylo/device-manual-step-dark.webp)

**05** — Under the hood

## Fresh OpenStreetMap, rebuilt with one button.

One CI workflow turns a fresh OpenStreetMap extract into everything the app ships: the road graph, the vector tiles, map styles with the high-contrast driving look, fonts and icons. Search is extracted from the same tiles on the phone, so the map, the router and the results always show the same roads.

- Road graph: 316,330 intersections, 754,040 road segments, 9,554 turn restrictions — 40 MB
- Map: vector tiles of Kyiv and the oblast, zoom 0–14 — about 126 MB, no internet needed
- Search: 72,273 entries and 225,609 house numbers, indexed on the device
- Router parity: the Swift router must match the Python reference in CI

**06** — Design system

## Native first: it should feel like Apple made it.

One persistent Liquid Glass sheet over a full-screen map, system controls, SF Symbols and Dynamic Type. Colour is reserved for meaning: blue for a confirmed position and the route, orange for anything the app doubts, green only for a drive that can follow you.

Component language

- GPS chip
- Position check
- Maneuver card
- Manual steps
- Route callouts
- Place card
- Search rows
- Driving map

Every state of trust has one look across the app and CarPlay, so a doubtful position reads the same in the chip, on the dot and in the guidance card.

**07** — Where it stands

## What works today.

A working iPhone app in development. The search figure was measured on a Mac with the real Kyiv data; nothing on this page was measured on the road yet.

316k

Intersections routed on the phone

1–35 ms

Offline search per query · Mac, real data

0

Accounts, ads or analytics

101

Automated core tests

**08** — More

## App support, privacy, or another study.

[ Veylo support ](https://imdennie.com/veylo/support/) [Privacy policy](https://imdennie.com/veylo/privacy/) [All work](https://imdennie.com/#work)

[ Next case study Numi — AI nutrition ](https://imdennie.com/case/numi.html) [ Case study Karta — restaurant platform ](https://imdennie.com/case/karta.html)
