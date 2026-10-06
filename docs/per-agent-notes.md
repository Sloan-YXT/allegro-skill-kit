# Per-agent failure modes and countermeasures

Observed across multiple AI agents doing PCB/schematic forensics in one long project. Written down so each agent can recognize its own patterns.

## Token/quota-heavy GUI agent

**Failure modes**
- Burned ~600k tokens for ~27 GUI edits — multiple full-screen screenshots per step.
- No incremental saves: killed by a capacity limit mid-task, everything after the last save lost.
- Earlier rounds declared "fixed" without physical evidence attached.

**Countermeasures**
- Batch inventory via scripting (Tcl injection / netlist export) instead of clicking through the GUI for read-only inspection.
- Screenshots only before/after an actual edit; crop, don't full-screen; never screenshot a read-only check.
- Save + milestone backup after every edit class; when capacity warnings appear, save and write a STATUS file (done/remaining) before continuing.
- Every "done" claim must carry the final exported diff.

## Orchestrator/communicator agent

**Failure modes**
- Relayed other agents' "fixed it" claims to the user as fact — they were wrong.
- Judged connector orientation from a fab-house preview rendering (mirrored bottom view) and raised a false alarm.
- Ran too many parallel threads; verification closure lagged behind promises.

**Countermeasures**
- Re-run the physical check yourself before relaying any conclusion — a diff or measurement takes minutes.
- Orientation questions: pad coordinates only.
- Close every thread with an explicit "verified / not verified" split.

## Reviewer agent

**Failure modes**
- Reviewed by appearance ("looks right") instead of data ("numbers match"); passed states that physical data later proved wrong.

**Countermeasures**
- Reviewer checklist: physical evidence present? pad-coordinate alignment for orientation? netlist diff for connectivity? measured mesh for structure? Any "should be fine" → reject.

## Shared rule

The verdict hierarchy is identical for every agent: exported netlists / Gerber / CAM dumps / measured meshes > raw config fields > screenshots, "opens fine", file names, and summaries.
