---
name: allegro-skill-kit
description: Verify and repair Allegro/OrCAD designs against the as-manufactured board — netlist-vs-CAM diffing, evidence hierarchy, OrCAD GUI automation recipe, and the visual-misjudgment case library. Use whenever asked to confirm a schematic/PCB is "correct", to converge a schematic to as-built, or to review another agent's fix claim.
---

# Allegro/OrCAD as-built verification kit

## The one rule

Trust physical data, never rendering. Hierarchy: exported netlists / Gerber / CAM dumps / measured meshes > raw config fields > viewer screenshots, "opens without error", file names.

Both directions of visual misjudgment are real (see `docs/evidence-hierarchy.md`):

- **Looks wrong, is right**: dangling wire stubs joined by net labels (electrically connected); mirrored bottom-side parts in fab-house preview pages (judge orientation by pad coordinates only); symbol fragments from a stale design cache
- **Looks right, is wrong**: a .dsn that opens cleanly and renders normally while carrying a superseded planned pinout instead of the as-built one

## Verification workflow

1. **Establish the authority**: the manufactured board. Dump pins from the production `.brd` (Allegro Skill `dump_allpins` script or equivalent) → `allpins.txt` with lines `PIN REFDES.PADNUM NETNAME ...`.
2. **Export the schematic**: OrCAD Capture → select dsn root → Tools > Create Netlist > PCB tab → `pstxnet.dat`.
3. **Diff as node sets**: `python tools/netlist_diff.py pstxnet.dat allpins.txt` (net-name agnostic pairing by overlap).
4. **Disposition every residual line**: FIX real mismatches; log ARTIFACT with a one-line justification (unplaced/NC parts, unnamed copper groupings, mounting holes, mechanical pads, shield pins). Nothing silently skipped.
5. **Re-export after each edit class** and re-diff. A fix claim without a final diff is unverified.

## Repair discipline (OrCAD Capture)

- `.dsn` is a binary OLE compound file — GUI automation (pywinauto UIA) is the only practical edit path. Full recipe: `docs/orcad-gui-automation.md`.
- **Save after every edit class** and keep milestone backups. GUI automation sessions die (focus theft, dialogs, token/quota limits) and unsaved work is simply gone.
- Backup before starting; never touch the authority board files.
- OrCAD joins nets by shared label name — renaming a stub's net label is the reliable way to connect it.
- Cosmetic issues (dangling stubs, label overlaps, stale design-cache symbol fragments) are worth fixing for reviewability, but only the netlist diff decides electrical correctness.

## Reviewing another agent's "fixed it" claim

Ask: which evidence layer? If the answer is screenshots or "it opens fine", reject and demand the exported diff. Ten rejections beat one pass of "should be fine".
