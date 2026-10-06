# OrCAD Capture GUI automation recipe (pywinauto)

OrCAD Capture `.dsn` files are binary OLE compound documents — there is no safe headless edit path. Driving the GUI with pywinauto (UIA backend) works, but the application is fragile. This recipe is what survived contact with reality.

## Setup

- Python with `pywinauto` (UIA backend). Attach to the running instance by window class `OrCaptureFrame`; do not launch a second instance over the same design (lock file `<DSN>.DSNlck`).
- If a relaunch is unavoidable: `taskkill /F /IM capture.exe`, delete the `.DSNlck`, relaunch with the dsn path, answer **No** to any recovery/"files in project" dialog, wizard = Schematic + OK.

## The #1 killer: focus theft

Other terminal windows steal keystrokes mid-`send_keys`. **Call `main.set_focus()` on the OrCaptureFrame immediately before EVERY `send_keys`.** When in doubt, screenshot first and confirm the focused window.

## Navigation

- The project tree's UIA rectangles **lie once the tree is scrolled**. Click tree rows by coordinates read from a fresh screenshot, never from UIA rects. Keyboard Down/Up + Enter opens pages reliably once the tree panel has focus (click a tree row first).
- Zoom: ctypes mouse wheel with Ctrl held at the target point:
  `user32.SetCursorPos(x,y); user32.keybd_event(0x11,0,0,0); user32.mouse_event(0x0800,0,0,120,0); user32.keybd_event(0x11,0,2,0)` — repeat per notch (~1.5× each).
- Find: Ctrl+F focuses the search box but it searches **net** names by default. For parts use Edit > Find with object type = part, or navigate visually.

## Editing

- **Net label rename (the workhorse)**: double-click the label text → in-place edit → type → Enter. OrCAD joins same-named nets — this is how you connect things.
- Alternative: select wire → right-click → Edit Properties → change net name.
- Screenshot BEFORE and AFTER every edit; name them sequentially. They are your undo log and your evidence.

## Saving (do it constantly)

- File > Save after **every edit class**. Automation sessions die without warning (focus loss, dialogs, external interruptions) and unsaved edits are gone permanently.
- If "Save Files In Project" appears, answer Yes All — autocorrection drops only unreadable records; the netlist export afterward is the real integrity check.
- Keep milestone backups of the .dsn (copy the file; the lock does not prevent copying).

## Verification

- Click the dsn root in the project tree → Tools > Create Netlist > PCB tab → export to a fresh `verify_N/` directory → diff `pstxnet.dat` against the board pin dump (see `tools/netlist_diff.py`).
- Verify after each edit class, not just at the end. A final export + full-page screenshots are the minimum evidence for any "done" claim.

## Hard rules

- Never edit the authority board files, backups, or reference designs.
- Kill-and-relaunch on hang; never force-save.
- The instance can self-destruct on unexpected dialogs — keep the automation loop polling for dialogs and screenshot on any exception.
