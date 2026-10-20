# Memory — durable facts

## Origin (2026-10-17 → 2026-10-20)
- Libraries built 2026-10-17 (first sent as zips; facts in freecad-wikitips docs/notes/memory.md "CAM tool
  library"): YG-1 Alu-Power from his catalogue PDF "YE-AP25 EUROPE" (26 bits: E5E47 1F Ø2-12, E5E48 2F short
  Ø3-12, E5522 2F long Ø3-12, E5910 2F ball Ø6-12); IZAR (85 bits: HSSE 4454 Autolock Ø2-20, 4464, 4420, 4410,
  4411 from IZAR_235.pdf p.241/242/245, carbide 9427/9429/9416/9417/9413/9414 from the Carbide Programme 2018);
  Amana (the 34 "Aluminum Cutting" bits of Amana's Fusion library, inch → mm; Amana's own file has 2
  inconsistencies: 51470 flutes, 51408 cutting length). RobbJack: he said NOT to make it. Stepcraft (3 bits)
  was sent too but its library file was not among the files he uploaded on 2026-10-20.
- 2026-10-20 Marios: "new repo, as an addon". He uploaded the 3 .fctl + FreeCAD's Default.fctl and his whole
  Bit folder (160 .fctb). In the repo: only YG1_*, IZAR_*, Amana_* (145) + the 3 libraries. Left out: FreeCAD's
  own sample bits/Default library (FreeCAD ships them) and one bit he made himself ("5mm 2 fluit izar", id
  34e100ea-…).
- Repo PUBLIC (needed for the Addon Manager; his yes 2026-10-20). Claude's GitHub app cannot create repos
  (403): Marios created it by hand.

## FreeCAD 26.3 facts (checked in its source)
- Libraries: `Path.Preferences.getAssetPath()/Tools/Library/*.fctl`; bits: `.../Tools/Bit/*.fctb`
  (getAssetPath = user folder/CamAssets unless set). A library lists bits by file name; the bit holds the
  geometry. Feeds/speeds are in the Tool Controller, not in the bit.
- `cam_assets.fetch(asset_type="toolbitlibrary")` lists libraries; `cam_assets.get(uri, depth=1)` loads the bits.

## Verified
- 2026-10-20 real FreeCAD 26.3, clean user folder (tests/run.sh): button on a CAM toolbar; first press copies
  148 files; FreeCAD's CAM lists the 3 libraries and loads 26/85/34 bits, every one with a diameter; second press
  copies nothing; an edited bit is kept on "No" and replaced on "Yes".
