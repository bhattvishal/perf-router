# Perf Router

A browser-based planner for laying out, wiring and auto-routing components on **double-sided perfboard** — and turning the result into a step-by-step solder plan.

It is a single static `index.html`: no build step, no server, no dependencies. Open it in a browser or host it on GitHub Pages.

## Features

- **Any board size** — default 24 × 18 holes at 2.54 mm pitch.
- **Parts library** — ESP32-C3 Super Mini (default), Seeed XIAO ESP32-C6, ESP32 DevKitC (38-pin), JST-XH 2/3/4-pin, resistor (adjustable lead spacing), 5 mm LED, WS2812 pixel LED (5 mm and 3-pin module).
- **Placement** — drag and drop on the hole grid, rotate, lock, overlap and off-board checks, and auto-suggested spots near the microcontroller. The microcontroller lands on the board edge with USB facing out.
- **Click-to-wire** — in Wire mode, tap a pin and then the pin it connects to. Nets merge automatically, power nets (GND, 5V, 3V3) are named and coloured, and each pin shows its GPIO label.
- **Ratsnest** — live Manhattan minimum-spanning tree per net, with a total length you can use to compare placements.
- **Connectivity checks** — flags power shorts (e.g. 5V on GND), both leads of a resistor or LED on one net, and GPIOs tied together.
- **Autorouter** — routes every net and reroutes on every change (see below).
- **Solder plan** — numbered build order: jumpers, then parts lowest-first, then solder-side wire runs (power first) with waypoints like `Wire C6 → C9 → P9`. Steps can be ticked off, copied as text or saved as `.txt`.
- **Component side / solder side views** — the solder-side view is mirrored to match the board in your hand.
- **Project files** — save and open `.json` projects, plus an automatic browser save between visits.
- **Wokwi import** — open a Wokwi `diagram.json` and it places the parts and routes the board (see below).

## How routing works

Double-sided perfboard has plated-through holes, so a hole belongs to one net on both sides. The router uses:

- **Solder side:** bare tinned wire or solder bridges between adjacent holes, with bends allowed. Every hole on a run joins the net.
- **Component side:** straight insulated jumpers that hop over other wires. Jumper ends land in free holes, and jumpers never cross a component body.

Routing uses A* on the hole grid, with a bend penalty and a jumper cost of about 8 holes of wire. Multi-pin nets grow as a tree from the nearest pin. The router tries several net orders, rips up nets that fail, and keeps the result with the fewest unrouted pins, then the fewest jumpers, then the least wire. You can limit jumper length or turn jumpers off.

## Wokwi import

Use **Import Wokwi** (or **Open…**) with a `diagram.json`. A review step lets you choose the target microcontroller and board size, and change how each part maps.

- Microcontroller pins are matched by **GPIO number**, and GND / 3V3 / 5V by name. This works across board variants: a Wokwi ESP32-C3 DevKitM or XIAO C3 lands on the C3 Super Mini, and an ESP32 DevKit V1 or DevKitC V4 lands on the DevKitC.
- Resistors, LEDs and NeoPixels map to their footprints.
- Off-board modules (sensors, displays, buttons, pots) become JST connectors labelled with the module's pin names, power first.
- Simulator-only wires (serial monitor) are ignored. Pins the target board doesn't break out are reported and left out.

An example is in [`examples/wokwi-esp32-devkitc-diagram.json`](examples/wokwi-esp32-devkitc-diagram.json), and the dialog also has **Try an example**.

## Usage

- **Online:** enable GitHub Pages for this repo (Settings → Pages → deploy from the `main` branch, root folder) and open the site.
- **Locally:** open `index.html` in a browser.

Keyboard shortcuts: `W` toggles Wire mode, `R` rotates, arrow keys nudge, `Delete` removes, `Ctrl+Z` undoes, `Esc` cancels.

## Check before soldering

- **Pin labels:** the ESP32-C3 Super Mini labels follow the common layout. Clones vary, so check against your board's silkscreen.
- **DevKitC header spacing:** headers are modelled 10 holes (1.0 in) apart, per Espressif's DevKitC V4. Many 38-pin clones are narrower, so measure yours.
- **Pixel LED leads:** the lead order of through-hole addressable LEDs varies by maker. Check your datasheet.

## Project file format

```json
{
  "app": "perfboard-planner",
  "version": 3,
  "name": "My board",
  "board": { "cols": 24, "rows": 18 },
  "maxJump": 8,
  "parts": [{ "id": "p1", "type": "c3mini", "ref": "U1", "x": 0, "y": 5, "rot": 3, "locked": true }],
  "nets":  [{ "name": "", "pins": ["p1:9", "p2:1"] }]
}
```

`x`/`y` are the top-left hole of the part's footprint. `rot` is in 90° steps clockwise. Net pins are `partId:pinIndex`.
