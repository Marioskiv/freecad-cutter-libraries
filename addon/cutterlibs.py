# Cutter Libraries — puts the cutter libraries of this addon into FreeCAD's CAM (one button).
#
# FreeCAD 26.3 keeps tool libraries in <CAM asset folder>/Tools/Library/*.fctl and the cutters they list
# in <CAM asset folder>/Tools/Bit/*.fctb (Path.Preferences.getAssetPath(); by default the user folder's
# CamAssets). The button copies this addon's files there. A file that is already there and different
# (for example a cutter you edited) is overwritten only if you say so.
#
# Copyright (c) 2026 Marioskiv
# https://github.com/Marioskiv/freecad-cutter-libraries
# SPDX-License-Identifier: MIT

import filecmp
import os
import shutil

import FreeCAD as App

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(os.path.dirname(HERE), "libraries")
ICON = os.path.join(HERE, "Resources", "CutterLibraries.svg")
TOOLBAR = "User parameter:BaseApp/Workbench/CAMWorkbench/Toolbar/CutterLibraries"


def target_root():
    """The CAM asset folder's Tools directory, as FreeCAD's CAM uses it."""
    import Path.Preferences
    return os.path.join(str(Path.Preferences.getAssetPath()), "Tools")


def plan(target=None):
    """(new, same, changed): lists of (source, destination) for every file of the addon."""
    target = target or target_root()
    new, same, changed = [], [], []
    for sub in ("Bit", "Library"):
        src_dir = os.path.join(SOURCE, sub)
        for name in sorted(os.listdir(src_dir)):
            src = os.path.join(src_dir, name)
            dst = os.path.join(target, sub, name)
            if not os.path.exists(dst):
                new.append((src, dst))
            elif filecmp.cmp(src, dst, shallow=False):
                same.append((src, dst))
            else:
                changed.append((src, dst))
    return new, same, changed


def install(overwrite=False, target=None):
    """Copies the files; `changed` ones only with overwrite. Returns (copied, kept)."""
    new, _same, changed = plan(target)
    todo = new + (changed if overwrite else [])
    for src, dst in todo:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    return len(todo), (0 if overwrite else len(changed))


def libraries():
    """The libraries of this addon: [(file name, label, number of cutters)]."""
    import json
    out = []
    lib_dir = os.path.join(SOURCE, "Library")
    for name in sorted(os.listdir(lib_dir)):
        with open(os.path.join(lib_dir, name), encoding="utf-8") as f:
            d = json.load(f)
        out.append((name, d.get("label", name), len(d.get("tools", []))))
    return out


if App.GuiUp:
    import FreeCADGui as Gui
    from PySide import QtGui

    try:
        from PySide import QtWidgets
    except ImportError:  # pragma: no cover
        QtWidgets = QtGui

    def _ask(parent, title, text):
        """Yes/No; the tests replace it."""
        B = QtWidgets.QMessageBox
        return B.question(parent, title, text, B.Yes | B.No, B.No) == B.Yes

    def _tell(parent, title, text):
        QtWidgets.QMessageBox.information(parent, title, text)

    class InstallCommand:
        def GetResources(self):
            return {"Pixmap": ICON,
                    "MenuText": "Εγκατάσταση βιβλιοθηκών κοπτικών",
                    "ToolTip": "Βάζει στο CAM τις βιβλιοθήκες κοπτικών YG-1, IZAR και Amana. "
                               "Ρωτάει πριν αλλάξει κοπτικό που έχεις ήδη και είναι διαφορετικό."}

        def IsActive(self):
            return True

        def Activated(self):
            mw = Gui.getMainWindow()
            try:
                target = target_root()
                new, same, changed = plan(target)
                overwrite = False
                if changed:
                    names = ", ".join(os.path.basename(d) for _s, d in changed[:8])
                    more = " κ.ά." if len(changed) > 8 else ""
                    overwrite = _ask(mw, "Βιβλιοθήκες κοπτικών",
                                     "%d αρχεία υπάρχουν ήδη στο FreeCAD σου και είναι διαφορετικά "
                                     "(ίσως τα άλλαξες): %s%s.\n\nΝα αντικατασταθούν με αυτά του addon;\n"
                                     "«Όχι»: μένουν τα δικά σου και μπαίνουν μόνο τα καινούργια."
                                     % (len(changed), names, more))
                copied, kept = install(overwrite, target)
                libs = "\n".join("• %s (%d κοπτικά)" % (label, n) for _f, label, n in libraries())
                _tell(mw, "Βιβλιοθήκες κοπτικών",
                      "Έτοιμο: %d αρχεία αντιγράφηκαν, %d ήταν ήδη ίδια%s.\n\n%s\n\n"
                      "Άνοιξε CAM → Toolbit Library Manager και διάλεξε τη βιβλιοθήκη "
                      "(αν ήταν ήδη ανοιχτό, κλείσ' το και άνοιξέ το ξανά).\n"
                      "Φάκελος: %s"
                      % (copied, len(same), (", %d κράτησες τα δικά σου" % kept) if kept else "",
                         libs, target))
            except Exception as e:
                _tell(mw, "Βιβλιοθήκες κοπτικών", "Δεν έγινε η εγκατάσταση: %s" % e)

    def ensure_toolbar():
        grp = App.ParamGet(TOOLBAR)
        grp.SetString("Name", "Βιβλιοθήκες κοπτικών")
        if not grp.GetBool("Created", False):
            grp.SetBool("Active", True)
            grp.SetBool("Created", True)
        if not grp.GetString("CutterLibraries_Install", ""):
            grp.SetString("CutterLibraries_Install", "cutterlibs")

    def install_gui():
        Gui.addCommand("CutterLibraries_Install", InstallCommand())
        ensure_toolbar()
