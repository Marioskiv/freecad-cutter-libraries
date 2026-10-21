# Cutter Libraries — puts the cutter libraries of this addon into FreeCAD's CAM, by itself, at start-up.
#
# FreeCAD 26.3 keeps tool libraries in <CAM asset folder>/Tools/Library/*.fctl and the cutters they list
# in <CAM asset folder>/Tools/Bit/*.fctb (Path.Preferences.getAssetPath(); by default the user folder's
# CamAssets), and CAM → Toolbit Library Manager shows what is there. At every start this addon copies the
# files that are missing. The first start of a new version of the addon (installed or updated) replaces
# ALL of its files, so an update always wins (Marios, 2026-10-21); between updates a cutter you edited is
# kept. Files that are not this addon's (your own cutters, FreeCAD's Default library) are never touched.
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
PARAMS = "User parameter:BaseApp/Preferences/Mod/CutterLibraries"
OLD_TOOLBARS = "User parameter:BaseApp/Workbench/CAMWorkbench/Toolbar"  # 1.x had a button there


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


def version():
    """This addon's version, from its package.xml."""
    import xml.etree.ElementTree as ET
    root = ET.parse(os.path.join(os.path.dirname(HERE), "package.xml")).getroot()
    for el in root:
        if el.tag.split("}")[-1] == "version":
            return el.text.strip()
    return ""


def sync(target=None):
    """Copies the missing files; on the first start of a new version, replaces all of this addon's files.
    Returns (copied, new_version)."""
    grp = App.ParamGet(PARAMS)
    ver = version()
    new_version = grp.GetString("InstalledVersion", "") != ver
    copied, _kept = install(overwrite=new_version, target=target)
    grp.SetString("InstalledVersion", ver)
    return copied, new_version


def remove_old_button():
    """1.x put an install button on a CAM toolbar; its toolbar would stay behind, empty."""
    grp = App.ParamGet(OLD_TOOLBARS)
    if grp.HasGroup("CutterLibraries"):
        grp.RemGroup("CutterLibraries")


def start():
    """Run once the GUI is up (InitGui). Never raises: a problem is only reported."""
    try:
        remove_old_button()
        # CAM puts its own Default library and sample cutters into the folder only while it is empty, so
        # let it do that first; otherwise our files would make it skip them.
        try:
            from Path.Tool import cam_assets
            cam_assets.setup()
        except Exception as e:
            App.Console.PrintWarning("Cutter Libraries: CAM's own assets were not set up first: %s\n" % e)
        copied, new_version = sync()
        if copied:
            App.Console.PrintMessage("Cutter Libraries %s: %d αρχεία κοπτικών μπήκαν στο CAM (%s)%s.\n"
                                     % (version(), copied, target_root(),
                                        ", νέα έκδοση: αντικαταστάθηκαν όλα" if new_version else ""))
    except Exception as e:
        App.Console.PrintError("Cutter Libraries: τα κοπτικά δεν μπήκαν στο CAM: %s\n" % e)


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
