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
- 2026-10-20 (1.1.0) Marios sent IZAR's 2026 aluminium catalogue (ALUMINIO_2026_ES_EN_FR_sin_precios.pdf,
  96 pages) and said: use only this one, forget the IZAR files before, take the 1- and 2-flute aluminium end
  mills. The old 85 IZAR bits were replaced by 212, every row checked against a picture of its page (the PDF
  text lost 2 rows: 6420 Ø3 and the third drain-hole row of 9417). Series (catalogue page): carbide 2Z 9427 (51),
  9429 (52); carbide 1Z 9441 (53), 9416 (54), 9417 (55), 9456 (56), 9466 (57), 9419 (58), 9413 (59), 9411 (60),
  9414 (61); PMX 2Z 6420 (69); HSSE 2Z 4420 (72), 4426 (73); HSSE 1Z 4410, 4411 (74); HSS 1Z 4412, 4413 (75),
  4414, 4415 (76), 4416, 4417 (77). Left out: 9417's drain-hole tools (90° point, not an end mill), 9674
  (Alucobond V-groove), 9330 (thread mill). 4454/4464 from the old catalogue are not in the 2026 one, so they
  are gone. One bit per row (coated and uncoated share the geometry; both article numbers are in the name).
  9456/9466 are right-hand cut with a left helix (pictures on p.56/57), so SpindleDirection stays Forward.
  The rows are in tools/izar_2026.py (python3 tools/izar_2026.py libraries rebuilds them).
- 2026-10-20 (1.2.0) Marios: "keep the old library I gave you at the start, and complete it with what I
  give you". So IZAR_Aluminio.fctl and its 85 bits are back byte for byte as in 1.0.0 (incl. 4454/4464), and
  the 2026 rows it lacks (151; same series + diameter + cutting length = already there) are a second library
  IZAR_Aluminio_2026.fctl, made by tools/izar_2026.py. Two old rows differ from the 2026 catalogue and were
  kept as he gave them: 9417 Ø5 l42 has L80 (2026: L75); 9417 Ø12 has l55 (2026: l52, added as
  IZAR_9417_12_l52). The 2018 Carbide Programme PDF he sent has no 4454/4464 (HSSE) and no aluminium 1Z/2Z
  series that the 2026 catalogue lacks.
- 2026-10-20 (1.3.0) Marios: "yes, keep them all" (Amana stays) and "add those too, and the IZAR 235 ones".
  tools/izar_extra.py makes two more libraries, every row checked against a picture of its page (the PDF text
  had lost rows again: 4422 Ø10-13, 4470 Ø10-12): IZAR_235 (75: the 4454/4464 rows his library lacked + ball
  4422/4470, IZAR_235.pdf p.241-243; its 4420/4426/4410/4411 are already covered) and IZAR_Carbide_2018 (109:
  9421, 9424, 9425, 9426 ball, 9470, 9475 micro ball; Carbide Programme p.27/29/37/38). Micro mills: the
  cutting length l is CuttingEdgeHeight; the neck reach (l1) is only in the name ("βάθος"). FreeCAD's bit shapes
  have no neck. 9452 (corner rounding) not added.
- His catalogues are kept in the session uploads (YG-1 YE-AP25 EUROPE.pdf, IZAR_235.pdf, Carbide_programme.pdf,
  ALUMINIO_2026.pdf, the Fusion .tools files); sent back to him 2026-10-20 after he lost his copies.
- 2026-10-21 (1.4.0) Marios: "yes, without a button" + "replace everything". No button any more: at every
  FreeCAD start (InitGui → QTimer → cutterlibs.start) the missing files are copied; the first start of a new
  addon version (param BaseApp/Preferences/Mod/CutterLibraries/InstalledVersion) replaces ALL the addon's
  files; between updates an edited cutter is kept. start() first calls cam_assets.setup(): CAM copies its
  own Default library + sample bits only while the folder is EMPTY, so copying ours first would have lost
  them (seen in the test, fixed). start() also removes the empty CAM toolbar left by 1.x.
- 2026-10-21 (1.4.1) Marios: "yes, do A B C D". docs/odigies/: his 3 guides of 2026-10-17 (YG1, IZAR, Amana
  .html; he re-uploaded them) with only "how to load" rewritten for the auto-copy, + IZAR_nees.html (made by
  tools/odigies_izar.py) for the 3 later IZAR libraries. Checked against the catalogues before publishing:
  YG-1 (EUROPE.pdf p.27/29/30-31: E5E47, E5E48/E5522 slot+side, long-tool ratios, E5910) all equal; IZAR
  (235 p.242/245; 2018 p.28/31/34) all equal; Amana: all 34 rows (Ø, flutes, lengths, shank, rpm, feed,
  plunge) equal to the Fusion file, and its 2 inconsistencies (51470, 51408) are real. T numbers in the guides
  equal the .fctl order. No aluminium data in the catalogue for 4422/4470 and 9470/9475 (said in the guide).
  9417 Ø5 L80 / Ø12 l55 are the 2018 catalogue's values (2026: L75 / l52); both kept.
- Repo PUBLIC (needed for the Addon Manager; his yes 2026-10-20). Claude's GitHub app cannot create repos
  (403): Marios created it by hand.

## FreeCAD 26.3 facts (checked in its source)
- Libraries: `Path.Preferences.getAssetPath()/Tools/Library/*.fctl`; bits: `.../Tools/Bit/*.fctb`
  (getAssetPath = user folder/CamAssets unless set). A library lists bits by file name; the bit holds the
  geometry. Feeds/speeds are in the Tool Controller, not in the bit.
- `cam_assets.fetch(asset_type="toolbitlibrary")` lists libraries; `cam_assets.get(uri, depth=1)` loads the bits.

## Verified
- 2026-10-21 1.4.0 real FreeCAD 26.3, clean user folder: no button; start-up copied all 486 files; CAM lists
  Default + the 6 libraries (26/85/151/75/109/34), every bit with a diameter; same version: missing file comes
  back, edited cutter kept; new version: edited cutter replaced; a file not ours untouched; 1.x toolbar removed.
- 2026-10-20 real FreeCAD 26.3, clean user folder (tests/run.sh): button on a CAM toolbar; first press copies
  148 files (1.0.0; 275 with the 2026 IZAR set); FreeCAD's CAM lists the 3 libraries and loads 26/85/34 bits
  (26/212/34 in 1.1.0; 26/85/151/34 and 300 files in 1.2.0; 26/85/151/75/109/34 and 486 files in 1.3.0), every one with a diameter; second press
  copies nothing; an edited bit is kept on "No" and replaced on "Yes".
