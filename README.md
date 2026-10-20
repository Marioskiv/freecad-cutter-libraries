# Βιβλιοθήκες κοπτικών για το FreeCAD CAM

Addon για το FreeCAD (1.1 και νεότερο, δοκιμασμένο στο 26.3) με τρεις βιβλιοθήκες κοπτικών για **αλουμίνιο**:

| Βιβλιοθήκη | Κοπτικά |
|---|---|
| YG-1 Alu-Power (1 και 2 δόντια) | 26 |
| IZAR αλουμίνιο 2026 (1 και 2 δόντια) | 212 |
| Amana για αλουμίνιο (από τη βιβλιοθήκη Fusion της Amana) | 34 |

## Εγκατάσταση
1. FreeCAD → **Edit → Preferences → Addon Manager** → Custom repositories → πρόσθεσε
   `https://github.com/Marioskiv/freecad-cutter-libraries`, branch `main`.
2. Addon Manager → **CutterLibraries** → Install → επανεκκίνηση του FreeCAD.
3. Στο **CAM** εμφανίζεται η εργαλειοθήκη «Βιβλιοθήκες κοπτικών». Πάτα το κουμπί: τα κοπτικά μπαίνουν στο FreeCAD.
   Αν έχεις αλλάξει ήδη κάποιο κοπτικό, σε ρωτάει πριν το αντικαταστήσει.
4. **CAM → Toolbit Library Manager** → διάλεξε τη βιβλιοθήκη.

Χωρίς addon γίνεται και με το χέρι: αντέγραψε τα `libraries/Bit/*.fctb` στο `CamAssets/Tools/Bit` και τα
`libraries/Library/*.fctl` στο `CamAssets/Tools/Library` του φακέλου χρήστη του FreeCAD.

## Στροφές και πρόωση
Η βιβλιοθήκη έχει μόνο τη **γεωμετρία** κάθε κοπτικού (διάμετρος, μήκη, δόντια). Στροφές και πρόωση μπαίνουν στο
**Tool Controller** κάθε Job, από τον κατάλογο του κατασκευαστή: πρόωση = στροφές × δόντια × φορτίο ανά δόντι (fz).

## Για προγραμματιστές
| Φάκελος | Περιεχόμενο |
|---|---|
| `libraries/` | τα αρχεία `.fctl` (βιβλιοθήκες) και `.fctb` (κοπτικά) |
| `addon/` | το κουμπί εγκατάστασης (`cutterlibs.py`, `InitGui.py`) |
| `tools/` | `izar_2026.py`: φτιάχνει τη βιβλιοθήκη IZAR από τον πίνακα του καταλόγου 2026 |
| `tests/` | δοκιμή σε πραγματικό FreeCAD: `FREECAD=/path/to/freecad sh tests/run.sh` |
| `docs/notes/` | σημειώσεις (μνήμη, εκκρεμότητες) |

Copyright (c) 2026 Marioskiv — άδεια MIT (`LICENSE`). Οι διαστάσεις των κοπτικών είναι από τους καταλόγους των
κατασκευαστών (YG-1, IZAR «Aluminio 2026») και από τη δημόσια βιβλιοθήκη Fusion 360 της Amana Tool.
