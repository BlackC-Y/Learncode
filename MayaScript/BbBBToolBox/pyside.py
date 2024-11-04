try:
    from PySide6 import QtCore, QtGui, QtWidgets
    import shiboken6 as shiboken
except ImportError:
    from PySide2 import QtCore, QtGui, QtWidgets   #2016 - 2024
    import shiboken2 as shiboken
    #except ImportError:   #2015
    #    from PySide import QtCore, QtGui, QtGui as QtWidgets
    #    import shiboken


def get_main_window():
    from maya import OpenMayaUI as OmUI
    return shiboken.wrapInstance(int(OmUI.MQtUtil.mainWindow()), QtWidgets.QWidget)
