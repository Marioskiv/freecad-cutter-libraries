# Cutter Libraries — test in a real FreeCAD (run by tests/run.sh, in a clean user folder).
#
# The button is on a CAM toolbar; pressed, it copies the libraries; FreeCAD's own CAM asset manager then
# lists the three libraries and loads every cutter with its diameter; pressing again copies nothing; a
# cutter you changed is kept when you answer "No" and replaced when you answer "Yes".
#
# Copyright (c) 2026 Marioskiv
# https://github.com/Marioskiv/freecad-cutter-libraries
# SPDX-License-Identifier: MIT

import json
import os
import traceback

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets

OUT = os.environ["CL_OUT"]
os.makedirs(OUT, exist_ok=True)
log = open(os.path.join(OUT, "log.txt"), "w", encoding="utf-8")
fails = []


def check(ok, what):
    log.write("%s %s\n" % ("ok  " if ok else "FAIL", what))
    log.flush()
    if not ok:
        fails.append(what)


def pump(ms):
    t = QtCore.QElapsedTimer()
    t.start()
    while t.elapsed() < ms:
        QtWidgets.QApplication.processEvents()


def button(cmd):
    for tb in Gui.getMainWindow().findChildren(QtWidgets.QToolBar):
        if tb.isVisible():
            for b in tb.findChildren(QtWidgets.QToolButton):
                a = b.defaultAction()
                if a is not None and a.objectName() == cmd and b.isVisible():
                    return b
    return None


def go():
    try:
        import cutterlibs
        told, answers = [], []
        cutterlibs._tell = lambda parent, title, text: told.append(text)
        cutterlibs._ask = lambda parent, title, text: answers.pop(0)
        Gui.activateWorkbench("CAMWorkbench")
        pump(1500)
        check(button("CutterLibraries_Install") is not None, "install button on a CAM toolbar")

        target = cutterlibs.target_root()
        new, same, changed = cutterlibs.plan(target)
        check(len(new) == 275 and not changed, "clean FreeCAD: 275 files to copy (272 cutters + 3 libraries), "
              "got %d new, %d changed" % (len(new), len(changed)))
        Gui.runCommand("CutterLibraries_Install")
        pump(300)
        check(told and "275 αρχεία αντιγράφηκαν" in told[-1], "first press: 275 copied (%r)" % (told[-1:] or ""))

        from Path.Tool import cam_assets
        from Path.Tool.library.models.library import Library
        from Path.Tool.assets import AssetUri
        libs = {lib.get_id(): lib for lib in cam_assets.fetch(asset_type="toolbitlibrary", depth=0)}
        want = {"YG1_AluPower": 26, "IZAR_Aluminio": 212, "Amana_Aluminio": 34}
        for lib_id, n in want.items():
            check(lib_id in libs, "FreeCAD's CAM lists the library %s (%s)" % (lib_id, sorted(libs)))
            if lib_id not in libs:
                continue
            lib = cam_assets.get(AssetUri.build(asset_type=Library.asset_type, asset_id=lib_id), depth=1)
            tools = list(lib)
            dias = []
            for tb in tools:
                try:
                    dias.append(float(tb.get_property("Diameter").Value))
                except Exception:
                    dias.append(None)
            check(len(tools) == n and all(d and d > 0 for d in dias),
                  "%s: %d cutters loaded with a diameter (%d, %s…)" % (lib_id, n, len(tools), dias[:3]))
            log.write("     %s = %r\n" % (lib_id, lib.label))

        told.clear()
        Gui.runCommand("CutterLibraries_Install")
        pump(300)
        check(told and "0 αρχεία αντιγράφηκαν, 275 ήταν ήδη ίδια" in told[-1], "second press copies nothing")

        bit = os.path.join(target, "Bit", "YG1_E5522030.fctb")
        d = json.load(open(bit, encoding="utf-8"))
        d["parameter"]["Chipload"] = "0.030 mm"            # "my own change"
        json.dump(d, open(bit, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        answers.append(False)
        Gui.runCommand("CutterLibraries_Install")
        pump(300)
        check("0.030" in open(bit, encoding="utf-8").read(), "a changed cutter is kept when the answer is No")
        answers.append(True)
        Gui.runCommand("CutterLibraries_Install")
        pump(300)
        check("0.030" not in open(bit, encoding="utf-8").read(), "and replaced when the answer is Yes")
    except Exception:
        fails.append("exception")
        log.write(traceback.format_exc())
    with open(os.path.join(OUT, "result.txt"), "w") as f:
        f.write("RESULT: %s\n" % ("PASS" if not fails else "FAIL " + "; ".join(fails)))
    log.close()
    os._exit(0)


QtCore.QTimer.singleShot(4000, go)
