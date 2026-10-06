# allegro-skill-kit

Battle-tested method + tools for verifying and repairing **Cadence Allegro / OrCAD Capture** designs against the board that was actually manufactured — born from a real incident where a schematic "looked fine", opened without errors, and turned out to carry an old planned pinout instead of the as-built one. The fix was only provable by exporting the netlist and diffing it against the board CAM data, pin by pin.

**The one rule: trust physical data, never rendering.**

Evidence hierarchy (highest first):

1. Gerber / drill files, exported netlists (`pstxnet.dat`), board CAM dumps (`allpins.txt`), G-code bytes, measured mesh/STL dimensions
2. Raw fields in order/config files (not the rendered preview)
3. Viewer screenshots, "opens without error", file names, settings panels — **never decisive**

## What's inside

- `SKILL.md` — agent skill: the full verification workflow, evidence hierarchy, and visual-misjudgment case library
- `tools/netlist_diff.py` — diff an OrCAD `pstxnet.dat` export against a board `allpins.txt` dump as **node sets** (net-name agnostic): exact matches, near-miss pairs sorted by overlap, board nets never overlapped
- `docs/orcad-gui-automation.md` — pywinauto recipe for driving OrCAD Capture reliably (it is fragile; this recipe cost a lot of pain to learn)
- `docs/evidence-hierarchy.md` — the misjudgment case library: things that look wrong but are right, and things that look right but are wrong
- `docs/per-agent-notes.md` — failure modes observed in AI agents doing this work, and the countermeasures

## Quick start

```bash
# 1. In OrCAD Capture: select dsn root → Tools > Create Netlist > PCB tab → export pstxnet.dat
# 2. In Allegro PCB Editor: dump pins (e.g. via a dump_allpins Skill script) → allpins.txt
# 3. Diff:
python tools/netlist_diff.py pstxnet.dat allpins.txt
```

Reading the output:

- **exact node-set matches** — these nets are provably identical between schematic and board
- **near-miss pairs** — same-named nets with node differences; every line must be either FIXED or justified as an artifact (unplaced parts, NC groupings)
- **board nets never overlapped** — coordinate-named artifacts are usually unnamed copper groupings, mounting holes, mechanical pads; real named nets here are red flags

Claiming "fixed" without a final clean (or fully justified) diff is claiming without evidence.

## License

MIT — see LICENSE.
