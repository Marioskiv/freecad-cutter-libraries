# Cutter Libraries — test in a real FreeCAD (run by tests/run.sh, in a clean user folder).
#
# Nothing to press: at start-up the addon has already copied the libraries; FreeCAD's own CAM asset
# manager lists them and loads every cutter with its diameter. Another start of the same version copies
# only what is missing and keeps a cutter you changed; the first start of a new version replaces it. A file
# that is not the addon's is never touched. The button of 1.x (and its toolbar) is gone.
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

LIBRARIES = {"YG1_AluPower": 26, "IZAR_Aluminio": 85, "IZAR_Aluminio_2026": 151, "IZAR_235": 75,
             "IZAR_Carbide_2018": 109, "Amana_Aluminio": 34}
FILES = sum(LIBRARIES.values()) + len(LIBRARIES)


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
        for b in tb.findChildren(QtWidgets.QToolButton):
            a = b.defaultAction()
            if a is not None and a.objectName() == cmd:
                return b
    return None


def go():
    try:
        import cutterlibs
        Gui.activateWorkbench("CAMWorkbench")
        pump(1500)
        check(button("CutterLibraries_Install") is None, "no install button any more")
        check(not App.ParamGet(cutterlibs.OLD_TOOLBARS).HasGroup("CutterLibraries"), "no toolbar of 1.x left")

        target = cutterlibs.target_root()
        new, same, changed = cutterlibs.plan(target)
        check(not new and not changed and len(same) == FILES,
              "start-up copied all %d files by itself: %d missing, %d different, %d same"
              % (FILES, len(new), len(changed), len(same)))
        ver = cutterlibs.version()
        check(ver and App.ParamGet(cutterlibs.PARAMS).GetString("InstalledVersion", "") == ver,
              "installed version recorded (%s)" % ver)

        from Path.Tool import cam_assets
        from Path.Tool.library.models.library import Library
        from Path.Tool.assets import AssetUri
        libs = {lib.get_id(): lib for lib in cam_assets.fetch(asset_type="toolbitlibrary", depth=0)}
        check("Default" in libs, "FreeCAD's own Default library is still there (%s)" % sorted(libs))
        for lib_id, n in LIBRARIES.items():
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

        copied, new_version = cutterlibs.sync()
        check(copied == 0 and not new_version, "another start of the same version copies nothing (%d)" % copied)

        bit = os.path.join(target, "Bit", "YG1_E5522030.fctb")
        d = json.load(open(bit, encoding="utf-8"))
        d["parameter"]["Chipload"] = "0.030 mm"            # "my own change"
        json.dump(d, open(bit, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        gone = os.path.join(target, "Bit", "IZAR_4410_3.fctb")
        os.remove(gone)
        mine = os.path.join(target, "Bit", "my_own_cutter.fctb")
        open(mine, "w", encoding="utf-8").write("{}")
        copied, _ = cutterlibs.sync()
        check(copied == 1 and os.path.exists(gone), "same version: a missing file comes back (%d copied)" % copied)
        check("0.030" in open(bit, encoding="utf-8").read(), "same version: a changed cutter is kept")

        App.ParamGet(cutterlibs.PARAMS).SetString("InstalledVersion", "0.0.0")   # as after an update
        copied, new_version = cutterlibs.sync()
        check(new_version and "0.030" not in open(bit, encoding="utf-8").read(),
              "new version: the changed cutter is replaced (%d copied)" % copied)
        check(os.path.exists(mine) and open(mine).read() == "{}", "a file that is not the addon's is never touched")

        App.ParamGet(cutterlibs.OLD_TOOLBARS + "/CutterLibraries").SetString("Name", "x")
        cutterlibs.start()
        check(not App.ParamGet(cutterlibs.OLD_TOOLBARS).HasGroup("CutterLibraries"),
              "start() removes a toolbar left by 1.x")
    except Exception:
        fails.append("exception")
        log.write(traceback.format_exc())
    with open(os.path.join(OUT, "result.txt"), "w") as f:
        f.write("RESULT: %s\n" % ("PASS" if not fails else "FAIL " + "; ".join(fails)))
    log.close()
    os._exit(0)


QtCore.QTimer.singleShot(4000, go)
