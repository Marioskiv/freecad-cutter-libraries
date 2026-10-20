# CLAUDE.md — read this first

Owner: Marios (GitHub: Marioskiv). He writes in Greeklish; **always answer in proper Greek script**, simple,
honest and direct. **No change without his clear "ναι"**; never claim something you have not checked.

Read `docs/notes/memory.md`, then `docs/notes/pending.md`.

## What lives where (decided by Marios, 2026-10-20)
| Repository | What it holds |
|---|---|
| **this repo** (`freecad-cutter-libraries`) | ONLY the cutter libraries (.fctl/.fctb) and the one-button installer addon |
| `freecad-wikitips` | WikiTips: hover help + Greek error explanations |
| `polar-cnc-converter` (to be renamed) | web converter, Polar CNC addon, Knurling & Wrap |
| `linuxcnc-calibrations`, `cnc-manuals` (private) | machine calibration; machine .ini/.hal and manuals |

## Rules
- Branch → PR → merge into `main` only after `tests/run.sh` passes in a real FreeCAD. Never push to `main`.
- Never hand-edit a `.fctb` without checking it against the maker's catalogue; bump `package.xml` <version> on
  every change so the Addon Manager offers the update.
- No pip dependencies; the addon must never break FreeCAD (start-up wrapped in try/except).
