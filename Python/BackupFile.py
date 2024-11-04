# -*- coding: utf-8 -*-
# Python 3.8
from PySide2.QtCore import Qt, QSize, QMetaObject, QFileInfo, QRect, QPropertyAnimation, QParallelAnimationGroup, QPoint
from PySide2.QtGui import QIcon, QPainter, QPalette, QColor, QPixmap, QIntValidator, QCursor
from PySide2.QtWidgets import *
from datetime import datetime
import threading
import tempfile
import shutil
import time
import sys
import os


UIData = {}

class BackupFile_Ui(QMainWindow):

    def __init__(self):
        super(BackupFile_Ui, self).__init__()
        with tempfile.NamedTemporaryFile('w', suffix='.log', delete=False) as tempfileA:
            tempfileA.write(f'{_GetTime()}:程序开始\n')
        UIData['LogFile'] = self.LogFile = tempfileA.name

        self.proPath = ''
        self.UiName = 'BackupFile'
        if not self.objectName():
            self.setFocus()
            self.setupUi()

    def setupUi(self):
        self.setObjectName(self.UiName)
        self.resize(500, 500)
        #self.setFixedSize(800, 500)
        self.setMinimumSize(QSize(600, 500))
        self.Mainwidget = QWidget(self)
        self.Mainwidget.setObjectName("Mainwidget")
        self.Mainwidget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        
        self.MainHLayout = QHBoxLayout(self.Mainwidget)
        self.MainHLayout.setObjectName("MainHLayout")
        self.MainHLayout.setSpacing(3)
        self.MainHLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.MainHLayout.setContentsMargins(5, 5, 5, 5)

        UIData['Projectlist'] = self.ProjectlistWidget = QListWidget(self.Mainwidget)
        self.ProjectlistWidget.setObjectName("ProjectlistWidget")
        self.ProjectlistWidget.setMaximumSize(QSize(200, 500))
        self.ProjectlistWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.MainHLayout.addWidget(self.ProjectlistWidget)

        CLine = QFrame(self.Mainwidget)
        CLine.setFrameShadow(QFrame.Plain)
        CLine.setStyleSheet('color:#7d7d7d;')
        CLine.setFrameShape(QFrame.VLine)
        CLine.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.MainHLayout.addWidget(CLine)

        self.ConfigVLayout = QVBoxLayout()
        self.ConfigVLayout.setObjectName(u"ConfigVLayout")
        self.ConfigVLayout.setContentsMargins(5, 5, 5, 5)

        _tempHLayout = QHBoxLayout()
        _tempHLayout.setSpacing(10)
        self.ProjectPathlabel = QLabel(self.Mainwidget)
        #self.ProjectPathlabel.setMaximumSize(QSize(50, 20))
        _tempHLayout.addWidget(self.ProjectPathlabel)
        UIData['ProjecPath'] = self.ProjectPathLine = QLineEdit(self.Mainwidget)
        self.ProjectPathLine.setObjectName("ProjectPathLine")
        self.ProjectPathLine.setContextMenuPolicy(Qt.CustomContextMenu)
        _tempHLayout.addWidget(self.ProjectPathLine)
        self.ProjectNamelabel = QLabel(self.Mainwidget)
        #self.ProjectNamelabel.setMaximumSize(QSize(50, 20))
        _tempHLayout.addWidget(self.ProjectNamelabel)
        UIData['ProjecName'] = self.ProjectNameLine = QLineEdit(self.Mainwidget)
        self.ProjectNameLine.setObjectName("ProjectNameLine")
        self.ProjectNameLine.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ProjectNameLine.setReadOnly(True)
        _tempHLayout.addWidget(self.ProjectNameLine)
        self.ConfigVLayout.addLayout(_tempHLayout)
        
        _tempHLayout = QHBoxLayout()
        _tempHLayout.setSpacing(10)
        self.BackupPathlabel = QLabel(self.Mainwidget)
        #self.BackupPathlabel.setMaximumSize(QSize(50, 20))
        _tempHLayout.addWidget(self.BackupPathlabel)
        UIData['BackupPath'] = self.BackupPathLine = QLineEdit(self.Mainwidget)
        self.BackupPathLine.setObjectName("BackupPathLine")
        self.BackupPathLine.setContextMenuPolicy(Qt.CustomContextMenu)
        _tempHLayout.addWidget(self.BackupPathLine)
        self.BackupTimelabel = QLabel(self.Mainwidget)
        #self.BackupTimelabel.setMaximumSize(QSize(50, 20))
        _tempHLayout.addWidget(self.BackupTimelabel)
        UIData['BackupTime'] = self.BackupTimeLine = QLineEdit(self.Mainwidget)
        self.BackupTimeLine.setObjectName("BackupTimeLine")
        self.BackupTimeLine.setValidator(QIntValidator())
        self.BackupTimeLine.setContextMenuPolicy(Qt.CustomContextMenu)
        _tempHLayout.addWidget(self.BackupTimeLine)
        self.ConfigVLayout.addLayout(_tempHLayout)

        _tempHLayout = QHBoxLayout()
        _tempHLayout.setSpacing(10)
        UIData['StartButton'] = self.StartButton = QPushButton(self.Mainwidget)
        self.StartButton.setObjectName(u"StartButton")
        _tempHLayout.addWidget(self.StartButton)
        self.NowCheckButton = QPushButton(self.Mainwidget)
        self.NowCheckButton.setObjectName(u"NowCheckButton")
        _tempHLayout.addWidget(self.NowCheckButton)
        self.ConfigVLayout.addLayout(_tempHLayout)

        self.StopButton = QPushButton(self.Mainwidget)
        self.StopButton.setObjectName(u"StopButton")
        self.ConfigVLayout.addWidget(self.StopButton)

        UIData['LogWidget'] = self.LogListWidget = QListWidget(self.Mainwidget)
        self.LogListWidget.setObjectName("LogListWidget")
        self.LogListWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.ConfigVLayout.addWidget(self.LogListWidget)

        self.MainHLayout.addLayout(self.ConfigVLayout)

        self.setWindowTitle(self.UiName)
        self.ProjectlistWidget.customContextMenuRequested[QPoint].connect(self._openDirMenu)
        self.ProjectPathlabel.setText(u'项目目录')
        self.ProjectPathLine.textChanged.connect(lambda *args: self.ProjectPathLine.setStyleSheet("color: black;"))
        self.ProjectPathLine.editingFinished.connect(self.addProjectItem)
        self.ProjectNamelabel.setText(u'监控项目')
        self.BackupPathlabel.setText(u'备份目录')
        self.BackupPathLine.editingFinished.connect(self.checkBackupPath)
        self.BackupTimelabel.setText(u'备份间隔')
        self.BackupTimeLine.setText('8')
        self.StartButton.setText(u'开始监控')
        self.StartButton.clicked.connect(lambda *args: StartMonitor())
        self.NowCheckButton.setText(u'立即检查')
        self.NowCheckButton.clicked.connect(lambda *args: NowCheckMonitor())
        self.StopButton.setText(u'停止监控')
        self.StopButton.clicked.connect(lambda *args: StopMonitor())

        QMetaObject.connectSlotsByName(self)
        self.setWindowFlags(Qt.Window)
        self.setCentralWidget(self.Mainwidget)

        self._GetConfig()
        self.addProjectItem()

    def closeEvent(self, event):
        #保存填写的项目路径
        if self.proPath:
            with open(self.configPath, 'w') as wconfig:
                wconfig.write(f'{self.proPath}\n')
                wconfig.write(self.BackupPathLine.text())
        
        #确认线程状态
        try:
            if monitorThread and monitorThread.is_alive():
                _outLog(u'正在结束监控')
                StopMonitor()
                monitorThread.join()
        except NameError:
            pass

        event.accept()

    def checkBackupPath(self):
        if not os.path.exists(self.BackupPathLine.text()):
            _outLog(u'指定备份目录不存在', 'red')

    def _GetConfig(self):
        self.configPath = _configPath = f"{os.getcwd()}\Config.bc"
        if os.path.exists(_configPath):
            with open(_configPath, "r") as CFile:
                line = CFile.readline().strip()
                if line and os.path.exists(line):
                    self.ProjectPathLine.setText(line)
                line = CFile.readline().strip()
                if line and os.path.exists(line):
                    self.BackupPathLine.setText(line)
        else:
            with open(_configPath, "w") as CFile:
                CFile.write('')

    def addProjectItem(self):
        Projectpath = self.ProjectPathLine.text()
        if Projectpath:
            self.ProjectlistWidget.clear()
            if not os.path.exists(Projectpath):
                self.proPath = ''
                _outLog(u'指定项目目录不存在', 'red')
                return
            self.ProjectPathLine.setStyleSheet("color: green;")
            self.proPath = Projectpath
            dirs = os.listdir(Projectpath)
            for i in dirs:
                if os.path.isdir(f'{Projectpath}/{i}'):
                    QListWidgetItem(i, self.ProjectlistWidget)

    def _openDirMenu(self, point):
        ProjectlistMenu = QMenu()
        ProjectlistMenu.addAction(QAction(u'打开项目文件夹', self, triggered = lambda *args: self._openDir('project')))
        ProjectlistMenu.addAction(QAction(u'打开备份文件夹', self, triggered = lambda *args: self._openDir('backup')))
        ProjectlistMenu.exec_(QCursor.pos())

    def _openDir(self, type):
        projectName = self.ProjectlistWidget.selectedItems()
        if not projectName:
            return
        projectName = projectName[0].text()
        if type == 'project':
            os.startfile(f'{self.ProjectPathLine.text()}/{projectName}')
        else:
            backupPath = f'{self.BackupPathLine.text()}/{projectName}'
            if os.path.exists(backupPath):
                os.startfile(backupPath)
            else:
                _outLog(f'项目 - {projectName}, 没有备份文件')


def _GetTime():
    return str(datetime.now()).split('.')[0]

def _outLog(Text, mode = 'black'):
    _Info = QListWidgetItem(f'{_GetTime()}:{Text}', UIData['LogWidget'])
    _Info.setForeground(QColor(mode))
    with open(UIData['LogFile'], 'a') as Log:
        Log.write(f'{_GetTime()}:{Text}\n')
    UIData['LogWidget'].setCurrentRow(UIData['LogWidget'].count() - 1)

_SetRun_ = 0
monitorThread = 0
tevent = threading.Event()

def StartMonitor():
    global _SetRun_
    _SetRun_ = 1
    
    tevent.clear()
    global monitorThread
    if monitorThread and monitorThread.is_alive():
        _outLog(u'监控已在运行')
        return
    #global monitorThread
    monitorThread = threading.Thread(target=OneThread)   #args=(ProjectList,)
    monitorThread.start()
    _outLog(u'开始运行')
    UIData['StartButton'].setStyleSheet(u'color: rgb(54, 162, 79);')

def NowCheckMonitor():
    if monitorThread and monitorThread.is_alive():
        tevent.set()
        tevent.clear()
    else:
        StartMonitor()
        StopMonitor()
    
def StopMonitor():
    global _SetRun_
    _SetRun_ = 0
    tevent.set()
    #_outLog(u'请等待线程结束')
    UIData['StartButton'].setStyleSheet(u'color: rgb(0, 0, 0);')

def OneThread():
    backupPath = UIData['BackupPath'].text()
    if not os.path.exists(backupPath):
        _outLog(u'指定备份目录不存在', 'red')
        return
    
    while(_SetRun_):
        BFUi.addProjectItem()
        #ProjectList的内容 [项目总目录, 项目名称]
        PPth = UIData['ProjecPath'].text()
        ProjectList = [[PPth, UIData['Projectlist'].item(i).text()] for i in range(UIData['Projectlist'].count())]
        if not ProjectList:
            _outLog(u'没有获取到项目', 'red')
            return
        _outLog('开始查询')
        for i in ProjectList:
            if os.path.exists(f'{i[0]}/{i[1]}/Scenes.revisions/'):
                
                #项目文件时间
                prorevisionsTime = []
                prorevisionsTimeapp = prorevisionsTime.append
                for root, dirs, files in os.walk(f'{i[0]}/{i[1]}/Scenes.revisions/'):
                    for f in files:
                        prorevisionsTimeapp([f'{root}/{f}', f, os.stat(f'{root}/{f}').st_mtime])
                
                #备份文件时间
                backupTime = []
                _backupTimeapp = backupTime.append
                if os.path.exists(f'{backupPath}/{i[1]}'):
                    for root, dirs, files in os.walk(f'{backupPath}/{i[1]}'):
                        for f in files:
                            _backupTimeapp(os.stat(f'{root}/{f}').st_mtime)

                for fTime in prorevisionsTime:
                    if not fTime[2] in backupTime:
                        _outLog(f'发现新文件{fTime[0]}')
                        if not os.path.exists(f'{backupPath}/{i[1]}'):
                            os.mkdir(f'{backupPath}/{i[1]}')
                        
                        _Time = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(os.stat(fTime[0]).st_mtime))
                        if fTime[1].rsplit('.', 1)[-1] == 'auto':
                            _newFile = f'{backupPath}/{i[1]}/{fTime[1].split(".vzs")[0]} & {_Time} & AUTO.vzs'
                        else:
                            _newFile = f'{backupPath}/{i[1]}/{fTime[1].split(".vzs")[0]} & {_Time}.vzs'
                        if os.path.exists(_newFile):
                            _outLog(f'发现修改时间重复的文件 请手动检查\n {fTime[0]} 和 {_newFile}', 'red')
                            continue
                        try:
                            shutil.copy2(fTime[0], _newFile)
                        except PermissionError:
                            _outLog(f'文件{fTime[0]}可能正在自动保存, 本次跳过文件', 'orange')
                        _outLog(f'备份完成')   #-新文件{_newFile}
        
        _outLog('本次查询结束')
        print(_GetTime())
        tevent.wait(int(UIData['BackupTime'].text())*60)
    _outLog(u'监控已结束')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    BFUi = BackupFile_Ui()
    BFUi.show()
    sys.exit(app.exec_())