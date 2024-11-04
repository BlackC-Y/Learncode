# -*- coding: UTF-8 -*-
from maya import cmds
from maya.api import OpenMaya as om

import os
import time
import json
import traceback
from functools import wraps


def timeStatistics(func):
    @wraps(func)
    def statistics(*args, **kwargs):
        st = time.time()
        oneTuple = func(*args, **kwargs)
        print('%s: %s' %(func.__name__, time.time() - st))
        return oneTuple
    return statistics


def undoChunk(func):
    @wraps(func)
    def chunk(*args, **kwargs):
        cmds.undoInfo(ock=1)
        try:
            oneTuple = func(*args, **kwargs)
        except Exception:
            om.MGlobal.displayError(traceback.format_exc())
            #logging.error()
        else:
            return oneTuple
        finally:
            cmds.undoInfo(cck=1)
    return chunk


class RecordLog_Maya(object):
    
    def __call__(self, func):
        @wraps(func)
        def log(*args, **kwargs):
            AllLog = '%s\n' %time.strftime("%m-%d %H:%M:%S", time.localtime())
            AllLog = '%s%s func enter\n' %(AllLog, func.__name__)
            result = func(*args, **kwargs)
            AllLog = '%s%s func leave\n' %(AllLog, func.__name__)
            return result
        return log
    

class BoxQtStyle():

    @staticmethod
    def QButtonStyle(height=28, border_radius=4):
        theme=Functions.readSetting('Global', 'theme')
        if theme == 'black':
            TextColor = "#dbdbdb"
            ButtonBC = "#22252b"
            Button_hoverBC = "#333841"
            Button_pressedBC = "#292c34"
        elif theme == "pink":
            TextColor = "#2f2f2f"
            ButtonBC = "#f3abb6"
            Button_hoverBC = "#f3b7c0"
            Button_pressedBC = "#ffcad4"
        elif theme == 'eyegreen':
            TextColor = "#2f2f2f"
            ButtonBC = "#a6e1ad"
            Button_hoverBC = "#cdedd1"
            Button_pressedBC = "#c7edcc"

        return '''
        QPushButton {{
            height: {_height};
            border: none;
            padding-left: 10px;
            padding-right: 10px;
            font: "Sarasa Gothic SC";
            color: {_TextColor};
            border-radius: {_border_radius};
            background-color: {_ButtonBC};
        }}
        QPushButton:hover {{
            background-color: {_Button_hoverBC};
        }}
        QPushButton:pressed {{
            background-color: {_Button_pressedBC};
        }}
        '''.format(_height = height, _TextColor=TextColor, _border_radius = border_radius, 
                   _ButtonBC = ButtonBC, _Button_hoverBC = Button_hoverBC, _Button_pressedBC = Button_pressedBC
        )

    @staticmethod
    def backgroundMayaColor():
        theme=Functions.readSetting('Global', 'theme')
        if theme == 'black':
            return [.161, .172, .204]
        elif theme == "pink":
            return [1, .792, .831]
        elif theme == 'eyegreen':
            return [.776, .929, .808]
    
    @staticmethod
    def accentMayaColor():
        theme=Functions.readSetting('Global', 'theme')
        if theme == 'black':
            return [.133, .145, .169]
        elif theme == "pink":
            return [.953, .663, .718]
        elif theme == 'eyegreen':
            return [.653, .886, .684]


class Functions():

    @staticmethod
    def getmoudlePath():
        return cmds.moduleInfo(p=1, mn='BbBBToolBox')

    @staticmethod
    def installPyMel():
        ver = int(cmds.about(v=1))
        if ver < 2022 or ver > 2025:
            om.MGlobal.displayError('Maya 2022-2025 版本才能安装 PyMel')
            return
        pymelPath = "%s/data/pymel-1.5.0-py2.py3-none-any.whl" %Functions.getmoudlePath()
        import ctypes
        result = ctypes.windll.shell32.ShellExecuteW(None, u"runas", '%s/bin/mayapy.exe' %os.environ["MAYA_LOCATION"], ' -m pip install "%s"' %pymelPath, None, 1)
        if result <= 32:
            if cmds.framelessDialog(title='注意', message='你没有管理员权限，是否继续尝试安装', button=['安装', '取消'], primary=['取消']) == '安装':
                ctypes.windll.shell32.ShellExecuteW(None, u"open", '%s/bin/mayapy.exe' %os.environ["MAYA_LOCATION"], ' -m pip install --user "%s"' %pymelPath, None, 1)

    @staticmethod
    def check_font(font_name):
        systemfilepath = os.path.join('C:\Windows\Fonts', font_name)
        filepath = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft\Windows\Fonts', font_name)
        if os.path.isfile(filepath) or os.path.isfile(systemfilepath):
            return 0
        else:
            return 1
    
    @staticmethod
    def set_font(font_name):
        folder = '%s/data/' %cmds.moduleInfo(p=1, mn='BbBBToolBox')
        font = os.path.normpath(os.path.join(folder, font_name))
        return font

    @staticmethod
    def editSetting(ui, item, data):
        jsonFile = '%s/data/Settings.json' %cmds.moduleInfo(p=1, mn='BbBBToolBox')
        if os.path.isfile(jsonFile):
            with open(jsonFile, 'r') as jsFile:
                readData = json.load(jsFile)
            with open(jsonFile, 'w') as jsFile:
                readData[ui][item] = data
                json.dump(readData, jsFile, indent=2)

    @staticmethod
    def readSetting(ui, item):
        jsonFile = '%s/data/Settings.json' %cmds.moduleInfo(p=1, mn='BbBBToolBox')
        if not os.path.isfile(jsonFile):
            return None
        else:
            with open(jsonFile, 'r') as jsFile:
                readData = json.load(jsFile)
                jsSetting = readData[ui]
            return jsSetting[item]

