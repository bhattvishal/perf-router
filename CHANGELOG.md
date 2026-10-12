# Changelog

Perfboard Planner uses [CalVer](https://calver.org/) versions: `YYYY.MM.MICRO`, where MICRO counts releases within the month and restarts at 0. Every release gets a git tag and a GitHub release built from its section below.

To ship a change, run `python3 tools/bump_version.py "What changed" "Something else"`, commit and push. The Release workflow tags it and publishes the notes; it fails if `index.html` changed without a new version.

## [2026.10.0] - 2026-10-12

First versioned release.

### Added
- Board settings dialog for board size, per-side blank margins and the jumper limit (moved out of the top bar)
- Realistic part illustrations with shading for every component, also used as the parts-list icons
- LEDs in 3, 5, 8 and 10 mm, drawn at true size, with a red, green or blue colour option
- MAX98357A I2S amplifier module
- Mouse-wheel zoom centred on the pointer
- Drag handles to resize the parts and details panels (double-click resets)
- Redo (Ctrl+Y or Ctrl+Shift+Z) alongside Undo
- Confirmation dialogs for Organize parts, Re-route and Load sample
- About dialog with the version, and a step-by-step Get started guide that covers 3D printing the stencil

### Changed
- Load sample sits next to Import Wokwi; Start fresh is removed in favour of New
- Wokwi LEDs keep their colour on import

### Earlier work (before versioning)
- Placement, click-to-wire, ratsnest and short checks; jumper-minimising autorouter and component organizer
- Wokwi diagram.json import; project files; solder plan
- Castellated mounting, per-side board margins with dimensions
- Solder-side marking stencil export as STL and SVG
