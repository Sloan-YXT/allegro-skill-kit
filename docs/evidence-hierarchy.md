# Evidence hierarchy and the visual-misjudgment case library

Every case below actually happened. They cost real money and real time. Both directions occur — panic over things that were fine, and calm over things that were broken.

## The hierarchy

1. **Physical data**: Gerber/drill files, exported netlists, board CAM dumps, G-code bytes, measured mesh/STL dimensions, hash manifests
2. **Raw fields**: order/config file values read as text (not the rendered preview of them)
3. **Appearance**: viewer screenshots, "opens without error", file names, settings panels, somebody's summary

Layer 3 is never decisive. Claims must bottom out in layer 1.

## Looks wrong — is right

| Case | Appearance | Physical truth |
|---|---|---|
| Dangling stub + net label | Wire hanging in mid-air with a label, "obviously floating" | OrCAD joins same-named nets; the netlist shows the node on the net. Verify by diff, not eyes |
| Fab preview mirror | Bottom-side connectors "reversed" in the SMT confirm page | The preview mirrors bottom-side parts. Pad-to-pad coordinates are the only orientation criterion |
| Design-cache fragments | USB symbol renders as broken/duplicated pieces | Stale design cache (graphics), netlist may be fully intact — or not. Diff decides; Update Cache fixes the graphics |
| Offpage connector stubs | Port symbols with short wires to nowhere | The net on the other page carries the same name; connectivity is by name |

## Looks right — is wrong

| Case | Appearance | Physical truth |
|---|---|---|
| Superseded pinout | .dsn opens cleanly, renders normally, "already reviewed" twice | Content was the old planned pin assignment; the manufactured board used different pins. Only an exported netlist vs board CAM diff exposed it |
| "Opens without error" | File loads, DRC dialog quiet | Means the file parses. Says nothing about correctness |
| Previous "fixed" verdicts | Multiple agents reported success | None had exported a netlist. All were wrong until one did |

## Disposition discipline

After a diff, every residual line gets exactly one label:

- **FIXED** — with the new diff showing it gone
- **ARTIFACT** — with a one-line justification (unplaced part, NC grouping, mounting hole, mechanical pad, shield pin, unnamed copper)

No third option. "Probably fine" is not a disposition.
