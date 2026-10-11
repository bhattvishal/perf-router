# Perf Router

A browser-based planner for laying out, wiring and auto-routing components on **double-sided perfboard** — and turning the result into a step-by-step solder plan.

It is a single static `index.html`: no build step, no server, no dependencies. Open it in a browser or host it on GitHub Pages.

## Features

- **Any board size** — default 24 × 18 holes at 2.54 mm pitch.
- **Parts library**
  - Microcontrollers: ESP32-C3 Super Mini (default), Seeed XIAO ESP32-C6, ESP32 DevKitC (38-pin)
  - Connectors and headers: JST-XH 2/3/4-pin, female berg strips 1×3, 4, 5, 6, 8, 10 and 12
  - Passives and LEDs: resistor and diode (adjustable lead spacing), 5 mm LED, WS2812 pixel LED (5 mm and 3-pin module), WS2812B 5050 SMD LED drawn at true size with its off-grid pads bridged to the nearest holes
  - Sound and switches: active and passive 12 mm buzzers, 6 × 6 mm push button, 3-pin slide switch (SPDT)
  - Modules: DHT22 (bare 4-pin and 3-pin module), DRV8833 motor driver, VEML6030 light sensor, VL53L0X / VL53L1X ToF sensor, INMP441 I2S microphone
- **Castellated (SMD) mounting** — the C3 Super Mini and XIAO C6 can lie flat and solder from their edge pads. The module is drawn at its real size and stays put; only the solder points move one hole outward on each side. This works on locked parts too.
- **Placement** — drag and drop on the hole grid, rotate, lock, overlap checks (a part may overhang the board edge as long as every solder point lands on a hole), and auto-suggested spots near the microcontroller. The microcontroller lands on the board edge with USB facing out.
- **Component organizer** — places every unlocked part for short wires and as few jumpers as possible. Locked parts stay put, and the microcontroller keeps its USB at an edge.
- **Click-to-wire** — in Wire mode, tap a pin and then the pin it connects to. Nets merge automatically, power nets are named (GND is always black, 5V and 3V3 always red), and each pin shows its GPIO label.
- **Ratsnest** — live Manhattan minimum-spanning tree per net, with a total length you can use to compare placements.
- **Connectivity checks** — flags power shorts (e.g. 5V on GND), both leads of a resistor or LED on one net, and GPIOs tied together.
- **Autorouter** — routes every net and reroutes when parts or connections change. Resizing the board keeps existing wires; **Re-route** uses the new space.
- **Solder plan** — numbered build order: jumpers, then parts lowest-first, then solder-side wire runs (power first) with waypoints like `Wire C6 → C9 → P9`. It lives in the right panel next to the board details: switch with the floating **Details** / **Solder plan** tabs on the board edge, or hide the panel. Steps can be ticked off, copied as text or saved as `.txt`.
- **Component side / solder side views** — the solder-side view is mirrored to match the board in your hand.
- **Project files** — **New** (offers to save first), **Open…** and **Save file** for `.json` projects, plus an automatic browser save between visits.
- **Wokwi import** — open a Wokwi `diagram.json` and it places the parts and routes the board (see below).

## How routing works

Double-sided perfboard has plated-through holes, so a hole belongs to one net on both sides. The router uses:

- **Solder side:** bare tinned wire or solder bridges between adjacent holes, with bends allowed. Every hole on a run joins the net.
- **Component side:** straight insulated jumpers that hop over other wires. Jumper ends land in free holes, and jumpers never cross a component body.

Each net is routed with A* on the hole grid, growing as a tree from its nearest pin. The search uses a bend penalty, and a jumper costs about 20 holes of wire, so detours win over jumpers.

The router first uses **negotiated congestion**: nets may share holes at first, and the price of contested holes rises each pass until every net finds its own path. If that doesn't settle, a sequential router takes over. It tries several net orders and rips up nets that fail or need jumpers.

A final pass re-routes each net against the others to shorten it. The router keeps the result with the fewest unrouted pins, then the fewest jumpers, then the least wire. The **Jumpers** setting in the top bar limits jumper length or turns jumpers off.

## Wokwi import

Use **Import Wokwi** (or **Open…**) with a `diagram.json`. A review step lets you choose the target microcontroller and board size, and change how each part maps.

- Microcontroller pins are matched by **GPIO number**, and GND / 3V3 / 5V by name. This works across board variants: a Wokwi ESP32-C3 DevKitM or XIAO C3 lands on the C3 Super Mini, and an ESP32 DevKit V1 or DevKitC V4 lands on the DevKitC.
- Resistors, LEDs and NeoPixels map to their footprints.
- Push buttons, buzzers and slide switches map to their footprints. A VL53L0X or VL53L1X maps to the ToF module.
- Other off-board modules (sensors, displays, pots) become JST connectors labelled with the module's pin names, power first.
- Simulator-only wires (serial monitor) are ignored. Pins the target board doesn't break out are reported and left out.

An example is in [`examples/wokwi-esp32-devkitc-diagram.json`](examples/wokwi-esp32-devkitc-diagram.json), and the dialog also has **Try an example**.

## Usage

- **Online:** enable GitHub Pages for this repo (Settings → Pages → deploy from the `master` branch, root folder) and open the site.
- **Locally:** open `index.html` in a browser.

The app fills one screen with no page scroll: the parts list and the right panel scroll on their own, and both can be collapsed (the **Parts** tab on the board's left edge, the **Details** / **Solder plan** tabs on the right). Part categories collapse too. At 100% the whole board fits the window; zoom in with `+` or Ctrl + mouse wheel and pan by dragging with the right mouse button.

Keyboard shortcuts: `W` switches Place / Wire (the board turns dark in Wire mode), `S` switches component / solder side, `F` fits the board, `R` rotates, arrow keys nudge, `Delete` removes, `Ctrl+Z` undoes, `Esc` cancels.

## Check before soldering

- **Pin labels:** the ESP32-C3 Super Mini labels follow the common layout. Clones vary, so check against your board's silkscreen.
- **DevKitC header spacing:** headers are modelled 10 holes (1.0 in) apart, per Espressif's DevKitC V4. Many 38-pin clones are narrower, so measure yours.
- **Pixel LED leads:** the lead order of through-hole addressable LEDs varies by maker. Check your datasheet.
- **Module pinouts:** DRV8833, VEML6030, VL53L0X/L1X and INMP441 breakouts come in several variants. The footprints follow the most common ones, so check pin order and row spacing against your module.
- **Push button:** pins A1/A2 and B1/B2 are joined inside the switch. Wire one A pin and one B pin.

## Project file format

```json
{
  "app": "perfboard-planner",
  "version": 3,
  "name": "My board",
  "board": { "cols": 24, "rows": 18 },
  "maxJump": 8,
  "parts": [{ "id": "p1", "type": "c3mini", "ref": "U1", "x": 0, "y": 5, "rot": 3, "locked": true, "mount": "smd" }],
  "nets":  [{ "name": "", "pins": ["p1:9", "p2:1"] }]
}
```

`x`/`y` are the top-left hole of the part's footprint. `rot` is in 90° steps clockwise. `mount: "smd"` marks a castellated board laid flat. Net pins are `partId:pinIndex`.

## License

[MIT](LICENSE)
