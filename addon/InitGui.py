# Cutter Libraries — FreeCAD start-up: copies the libraries into CAM once the window is up.
#
# Copyright (c) 2026 Marioskiv
# https://github.com/Marioskiv/freecad-cutter-libraries
# SPDX-License-Identifier: MIT

try:
    import cutterlibs
    from PySide import QtCore
    QtCore.QTimer.singleShot(0, cutterlibs.start)
except Exception as e:  # never break FreeCAD start-up
    import FreeCAD
    FreeCAD.Console.PrintError("Cutter Libraries could not start: %s\n" % e)
