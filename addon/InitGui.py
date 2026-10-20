# Cutter Libraries — FreeCAD start-up: the install button on a CAM toolbar.
#
# Copyright (c) 2026 Marioskiv
# https://github.com/Marioskiv/freecad-cutter-libraries
# SPDX-License-Identifier: MIT

try:
    import cutterlibs
    cutterlibs.install_gui()
except Exception as e:  # never break FreeCAD start-up
    import FreeCAD
    FreeCAD.Console.PrintError("Cutter Libraries could not start: %s\n" % e)
