# Βιβλιοθήκες κοπτικών για το FreeCAD CAM

Addon για το FreeCAD (1.1 και νεότερο, δοκιμασμένο στο 26.3) με έξι βιβλιοθήκες κοπτικών, κυρίως για **αλουμίνιο**:

| Βιβλιοθήκη | Κοπτικά |
|---|---|
| YG-1 Alu-Power (1 και 2 δόντια) | 26 |
| IZAR αλουμίνιο (1 και 2 δόντια) | 85 |
| IZAR αλουμίνιο 2026 — συμπλήρωμα (όσα δεν έχει η προηγούμενη) | 151 |
| IZAR HSSE (κατάλογος 235) — συμπλήρωμα: 4454/4464 Autolock, σφαιρικές 4422/4470 | 75 |
| IZAR σκληρομέταλλο 2018 — 2 δόντια γενικής χρήσης, σφαιρικές, μίνι (9421, 9424, 9425, 9426, 9470, 9475) | 109 |
| Amana για αλουμίνιο (από τη βιβλιοθήκη Fusion της Amana) | 34 |

## Εγκατάσταση
1. FreeCAD → **Tools → Addon Manager** → ⚙ → Custom repositories → πρόσθεσε
   `https://github.com/Marioskiv/freecad-cutter-libraries`, branch `main`.
2. Addon Manager → **CutterLibraries** → Install → επανεκκίνηση του FreeCAD.
3. Δεν πατάς τίποτα: με το άνοιγμα του FreeCAD τα κοπτικά μπαίνουν μόνα τους.
   Άνοιξε **CAM → Toolbit Library Manager** και διάλεξε βιβλιοθήκη.

Πώς δουλεύει:
- Σε κάθε άνοιγμα μπαίνει ό,τι λείπει.
- Στο πρώτο άνοιγμα μετά από εγκατάσταση ή ενημέρωση του addon **αντικαθίστανται όλα** τα αρχεία του addon.
  Ανάμεσα σε δύο ενημερώσεις, ένα κοπτικό που άλλαξες μένει όπως το άλλαξες.
- Τα δικά σου κοπτικά και η βιβλιοθήκη `Default` του FreeCAD δεν αγγίζονται ποτέ.

Χωρίς addon γίνεται και με το χέρι: αντέγραψε τα `libraries/Bit/*.fctb` στο `CamAssets/Tools/Bit` και τα
`libraries/Library/*.fctl` στο `CamAssets/Tools/Library` του φακέλου χρήστη του FreeCAD.

## Οδηγίες: στροφές και πρόωση
Από τους καταλόγους των κατασκευαστών, στα ελληνικά:

| Αρχείο | Για ποια βιβλιοθήκη |
|---|---|
| [`docs/odigies/YG1.html`](docs/odigies/YG1.html) | YG-1 Alu-Power |
| [`docs/odigies/IZAR.html`](docs/odigies/IZAR.html) | IZAR αλουμίνιο (η αρχική) |
| [`docs/odigies/IZAR_nees.html`](docs/odigies/IZAR_nees.html) | IZAR 2026 συμπλήρωμα, IZAR 235, IZAR σκληρομέταλλο 2018 |
| [`docs/odigies/Amana.html`](docs/odigies/Amana.html) | Amana για αλουμίνιο |

Μετά την εγκατάσταση τα βρίσκεις και στον υπολογιστή σου, στον φάκελο του addon:
`C:\Users\<όνομα>\AppData\Roaming\FreeCAD\v26-3\Mod\CutterLibraries\docs\odigies\`. Άνοιξέ τα με διπλό κλικ
(ανοίγουν στον browser). Στο GitHub φαίνονται ως κώδικας: εκεί πάτα «Download raw file» και άνοιξε το αρχείο που κατέβηκε.

## Στροφές και πρόωση
Η βιβλιοθήκη έχει μόνο τη **γεωμετρία** κάθε κοπτικού (διάμετρος, μήκη, δόντια). Στροφές και πρόωση μπαίνουν στο
**Tool Controller** κάθε Job, από τον κατάλογο του κατασκευαστή: πρόωση = στροφές × δόντια × φορτίο ανά δόντι (fz).

## Για προγραμματιστές
| Φάκελος | Περιεχόμενο |
|---|---|
| `libraries/` | τα αρχεία `.fctl` (βιβλιοθήκες) και `.fctb` (κοπτικά) |
| `addon/` | η αντιγραφή στο άνοιγμα του FreeCAD (`cutterlibs.py`, `InitGui.py`) |
| `tools/` | `izar_2026.py`, `izar_extra.py`: φτιάχνουν τα συμπληρώματα IZAR · `odigies_izar.py`: φτιάχνει το `IZAR_nees.html` |
| `tests/` | δοκιμή σε πραγματικό FreeCAD: `FREECAD=/path/to/freecad sh tests/run.sh` |
| `docs/odigies/` | οδηγίες με στροφές και πρόωση |
| `docs/notes/` | σημειώσεις (μνήμη, εκκρεμότητες) |

Copyright (c) 2026 Marioskiv — άδεια MIT (`LICENSE`). Οι διαστάσεις των κοπτικών είναι από τους καταλόγους των
κατασκευαστών (YG-1, IZAR «Aluminio 2026») και από τη δημόσια βιβλιοθήκη Fusion 360 της Amana Tool.
