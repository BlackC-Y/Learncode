# -*- coding: utf-8 -*-
from PySide6 import QtCore, QtGui, QtWidgets
import time
import sys
import os
import re

uiItem = {}
unDoData = []

class FileTool_BlackC_Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(FileTool_BlackC_Ui, self).__init__()
        self.UiName = 'FileTool'
        if not self.objectName():
            self.setFocus()
            self.setupUi()

    def setupUi(self):
        self.setObjectName(self.UiName)
        self.resize(800, 500)
        #self.setFixedSize(800, 500)
        self.setMinimumSize(QtCore.QSize(650, 400))
        self.Mainwidget = QtWidgets.QWidget(self)
        self.Mainwidget.setObjectName("Mainwidget")
        self.Mainwidget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        
        self.MainHLayout = QtWidgets.QHBoxLayout(self.Mainwidget)
        self.MainHLayout.setObjectName("MainHLayout")
        self.MainHLayout.setSpacing(3)
        self.MainHLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.MainHLayout.setContentsMargins(5, 5, 5, 5)

        uiItem['tabWidget'] = self.tabWidget = QtWidgets.QTabWidget(self.Mainwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setMinimumSize(QtCore.QSize(300, 380))

        #Page 1 reName
        self.reNameTab = QtWidgets.QWidget()
        self.reNameTab.setObjectName("reNameTab")
        self.reNamePageVLayout = QtWidgets.QVBoxLayout(self.reNameTab)
        self.reNamePageVLayout.setObjectName("reNamePageVLayout")
        
        self.createText, _tempHLayout = self.coustomTextLine('H', self.reNameTab)
        self.reNamePageVLayout.addLayout(_tempHLayout)

        _tempHLayout = QtWidgets.QHBoxLayout()
        _tempHLayout.setSpacing(20)
        uiItem['rulesNameCB'] = self.rulesNameCB = QtWidgets.QCheckBox(self.reNameTab)
        self.rulesNameCB.setObjectName("rulesNameCB")
        _tempHLayout.addWidget(self.rulesNameCB)
        uiItem['rulesNameTextEdit'] = self.rulesNameTextEdit = QtWidgets.QLineEdit(self.reNameTab)
        self.rulesNameTextEdit.setObjectName("rulesNameTextEdit")
        _tempHLayout.addWidget(self.rulesNameTextEdit)
        _tempHLayout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.reNamePageVLayout.addLayout(_tempHLayout)
        
        _tempHLayout = QtWidgets.QHBoxLayout()
        _tempHLayout.setSpacing(20)
        uiItem['prefixCB'] = self.prefixCB = QtWidgets.QCheckBox(self.reNameTab)
        self.prefixCB.setObjectName("prefixCB")
        _tempHLayout.addWidget(self.prefixCB)
        uiItem['prefixTextEdit'] = self.prefixTextEdit = QtWidgets.QLineEdit(self.reNameTab)
        self.prefixTextEdit.setObjectName("prefixTextEdit")
        _tempHLayout.addWidget(self.prefixTextEdit)
        _tempHLayout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.reNamePageVLayout.addLayout(_tempHLayout)
        
        _tempHLayout = QtWidgets.QHBoxLayout()
        _tempHLayout.setSpacing(20)
        uiItem['suffixCB'] = self.suffixCB = QtWidgets.QCheckBox(self.reNameTab)
        self.suffixCB.setObjectName("suffixCB")
        _tempHLayout.addWidget(self.suffixCB)
        uiItem['suffixTextEdit'] = self.suffixTextEdit = QtWidgets.QLineEdit(self.reNameTab)
        self.suffixTextEdit.setObjectName("suffixTextEdit")
        _tempHLayout.addWidget(self.suffixTextEdit)
        _tempHLayout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.reNamePageVLayout.addLayout(_tempHLayout)

        _tempHLayout = QtWidgets.QHBoxLayout()
        _tempHLayout.setSpacing(20)
        uiItem['extensionCB'] = self.extensionCB = QtWidgets.QCheckBox(self.reNameTab)
        self.extensionCB.setObjectName("extensionCB")
        _tempHLayout.addWidget(self.extensionCB)
        uiItem['extensionTextEdit'] = self.extensionTextEdit = QtWidgets.QLineEdit(self.reNameTab)
        self.extensionTextEdit.setObjectName("extensionTextEdit")
        _tempHLayout.addWidget(self.extensionTextEdit)
        _tempHLayout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.reNamePageVLayout.addLayout(_tempHLayout)
        
        _tempVLayout = QtWidgets.QVBoxLayout()
        _tempHLayout = QtWidgets.QHBoxLayout()
        _tempHLayout.setSpacing(20)
        uiItem['replaceCB'] = self.replaceCB = QtWidgets.QCheckBox(self.reNameTab)
        self.replaceCB.setObjectName("replaceCB")
        _tempHLayout.addWidget(self.replaceCB)
        uiItem['replaceSTextEdit'] = self.replaceSTextEdit = QtWidgets.QLineEdit(self.reNameTab)
        self.replaceSTextEdit.setObjectName("replaceSTextEdit")
        _tempHLayout.addWidget(self.replaceSTextEdit)
        _tempHLayout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        _tempVLayout.addLayout(_tempHLayout)
        
        _tempHLayout = QtWidgets.QHBoxLayout()
        _tempHLayout.setSpacing(20)
        self.replacelabel = QtWidgets.QLabel(self.reNameTab)
        _tempHLayout.addWidget(self.replacelabel)
        uiItem['replaceTTextEdit'] = self.replaceTTextEdit = QtWidgets.QLineEdit(self.reNameTab)
        self.replaceTTextEdit.setObjectName("replaceTTextEdit")
        _tempHLayout.addWidget(self.replaceTTextEdit)
        _tempHLayout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        _tempVLayout.addLayout(_tempHLayout)
        self.reNamePageVLayout.addLayout(_tempVLayout)
        
        #delete
        self.deleteText, _tempHLayout = self.coustomTextLine('H', self.reNameTab)
        self.reNamePageVLayout.addLayout(_tempHLayout)

        _tempVLayout = QtWidgets.QVBoxLayout()
        _tempHLayout = QtWidgets.QHBoxLayout()
        uiItem['toLocationCB'] = self.toLocationCB = QtWidgets.QCheckBox(self.reNameTab)
        self.toLocationCB.setObjectName("toLocationCB")
        _tempHLayout.addWidget(self.toLocationCB)
        uiItem['startLocationSB'] = self.startLocationSB = QtWidgets.QSpinBox(self.reNameTab)
        self.startLocationSB.setObjectName("startLocationSB")
        self.startLocationSB.setMinimumSize(QtCore.QSize(55, 20))
        self.startLocationSB.setMinimum(1)
        _tempHLayout.addWidget(self.startLocationSB)
        self.TextLoclabelB = QtWidgets.QLabel(self.reNameTab)
        _tempHLayout.addWidget(self.TextLoclabelB)
        _tempHLayout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        _tempVLayout.addLayout(_tempHLayout)
        
        _tempHLayout = QtWidgets.QHBoxLayout()
        self.TextLoclabelC = QtWidgets.QLabel(self.reNameTab)
        _tempHLayout.addWidget(self.TextLoclabelC)
        uiItem['numLocationSB'] = self.numLocationSB = QtWidgets.QSpinBox(self.reNameTab)
        self.numLocationSB.setObjectName("numLocationSB")
        self.numLocationSB.setMinimumSize(QtCore.QSize(55, 20))
        self.numLocationSB.setMinimum(1)
        _tempHLayout.addWidget(self.numLocationSB)
        self.TextLoclabelD = QtWidgets.QLabel(self.reNameTab)
        _tempHLayout.addWidget(self.TextLoclabelD)
        _tempHLayout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        _tempVLayout.addLayout(_tempHLayout)
        self.reNamePageVLayout.addLayout(_tempVLayout)
        
        _tempHLayout = QtWidgets.QHBoxLayout()
        uiItem['endLocationCB'] = self.endLocationCB = QtWidgets.QCheckBox(self.reNameTab)
        self.endLocationCB.setObjectName("endLocationCB")
        _tempHLayout.addWidget(self.endLocationCB)
        uiItem['endNumLocationSB'] = self.endNumLocationSB = QtWidgets.QSpinBox(self.reNameTab)
        self.endNumLocationSB.setObjectName("endNumLocationSB")
        self.endNumLocationSB.setMinimumSize(QtCore.QSize(55, 20))
        self.endNumLocationSB.setMinimum(1)
        _tempHLayout.addWidget(self.endNumLocationSB)
        self.TextLoclabelE = QtWidgets.QLabel(self.reNameTab)
        _tempHLayout.addWidget(self.TextLoclabelE)
        _tempHLayout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.reNamePageVLayout.addLayout(_tempHLayout)

        self.reNamebutton = QtWidgets.QPushButton(self.reNameTab)
        self.reNamebutton.setMinimumSize(QtCore.QSize(80, 26))
        self.reNamebutton.setObjectName("reNamebutton")
        self.reNamePageVLayout.addWidget(self.reNamebutton)
        
        self.Testbutton = QtWidgets.QPushButton(self.reNameTab)
        self.Testbutton.setMinimumSize(QtCore.QSize(80, 26))
        self.Testbutton.setObjectName("Testbutton")
        self.Testbutton.clicked.connect(lambda *args: self.testbutton()) #####
        self.Testbutton.setText(u"Testbutton")
        self.reNamePageVLayout.addWidget(self.Testbutton)
        self.reNamePageVLayout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.tabWidget.addTab(self.reNameTab, "")

        #Page 2 File
        self.FileProcTab = QtWidgets.QWidget()
        self.FileProcTab.setObjectName("fileTab")
        self.FileProcPageVLayout = QtWidgets.QVBoxLayout(self.FileProcTab)
        self.FileProcPageVLayout.setObjectName("FileProcPageVLayout")

        _tempHLayout = QtWidgets.QHBoxLayout()
        _tempHLayout.setSpacing(10)
        self.createNulllabel = QtWidgets.QLabel(self.FileProcTab)
        _tempHLayout.addWidget(self.createNulllabel)
        uiItem['createNullTextEdit'] = self.createNullTextEdit = QtWidgets.QLineEdit(self.FileProcTab)
        self.createNullTextEdit.setObjectName("createNullTextEdit")
        _tempHLayout.addWidget(self.createNullTextEdit)
        self.createNullButton = QtWidgets.QPushButton(self.FileProcTab)
        self.createNullButton.setObjectName("createNullButton")
        _tempHLayout.addWidget(self.createNullButton)
        _tempHLayout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.FileProcPageVLayout.addLayout(_tempHLayout)
        
        self.FileProcPageVLayout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.tabWidget.addTab(self.FileProcTab, "")
        self.tabWidget.setCurrentIndex(0)
        self.MainHLayout.addWidget(self.tabWidget)

        self.twHLayout = QtWidgets.QHBoxLayout()
        self.twHLayout.setObjectName("twHLayout")
        uiItem['FiletreeWidget'] = self.FiletreeWidget = coustomTreeWidget(self.Mainwidget)
        self.FiletreeWidget.setObjectName("FiletreeWidget")
        self.FiletreeWidget.setMinimumSize(QtCore.QSize(300, 380))
        self.FiletreeWidget.setRootIsDecorated(False)
        self.FiletreeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.FiletreeWidget.setSortingEnabled(True)
        #self.FiletreeWidget.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        #icon = QtGui.QIcon()
        #icon.addFile("C:/Users/yangbanghui/Desktop/aaa.png", QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #item_0 = QTreeWidgetItem(self.FiletreeWidget)
        #item_0.setIcon(0, icon)
        self.twHLayout.addWidget(self.FiletreeWidget)
        
        self.buttonVLayout = QtWidgets.QVBoxLayout()
        self.buttonVLayout.setSpacing(3)
        self.buttonVLayout.setObjectName("buttonVLayout")
        self.buttonVLayout.setContentsMargins(2, 0, 2, 0)
        
        self.unDobutton = QtWidgets.QPushButton(self.Mainwidget)
        self.unDobutton.setObjectName("unDobutton")
        self.unDobutton.setMaximumSize(QtCore.QSize(35, 35))
        self.buttonVLayout.addWidget(self.unDobutton)
        self.buttonVLayout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        
        self.upMoveItembutton = QtWidgets.QPushButton(self.Mainwidget)
        self.upMoveItembutton.setObjectName("upMoveItembutton")
        self.upMoveItembutton.setMaximumSize(QtCore.QSize(35, 35))
        self.buttonVLayout.addWidget(self.upMoveItembutton)
        
        self.deleteItembutton = QtWidgets.QPushButton(self.Mainwidget)
        self.deleteItembutton.setObjectName("deleteItembutton")
        self.deleteItembutton.setMaximumSize(QtCore.QSize(35, 35))
        self.buttonVLayout.addWidget(self.deleteItembutton)

        self.dnMoveItembutton = QtWidgets.QPushButton(self.Mainwidget)
        self.dnMoveItembutton.setObjectName("dnMoveItembutton")
        self.dnMoveItembutton.setMaximumSize(QtCore.QSize(35, 35))
        self.buttonVLayout.addWidget(self.dnMoveItembutton)
        self.buttonVLayout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        
        self.twHLayout.addLayout(self.buttonVLayout)
        self.MainHLayout.addLayout(self.twHLayout)

        self.setWindowTitle(self.UiName)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.reNameTab), "重命名")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.FileProcTab), "File")
        self.tabWidget.currentChanged.connect(self.changeTab)
        self.createText.setText('添加/替换')
        self.rulesNameCB.setText("规则命名")
        self.rulesNameCB.clicked.connect(self.refreshTreeWeight)
        self.rulesNameTextEdit.setPlaceholderText('xxx_#1^')
        self.rulesNameTextEdit.setToolTip('#代表字符数量\n接初始序号 再用+号可添加步进或步减\n^进行结尾\n \
                                            \neg:  aa_###1+2^_zz  =  aa_001_zz/aa_003_zz \neg: aa_##10+-2^_zz  =  aa_10_zz/aa_08_zz')
        self.rulesNameTextEdit.textEdited.connect(self.textConfirm)
        self.prefixCB.setText("前缀名  ")
        self.prefixCB.clicked.connect(self.refreshTreeWeight)
        self.prefixTextEdit.setPlaceholderText('prefix_')
        self.prefixTextEdit.textEdited.connect(self.textConfirm)
        self.suffixCB.setText("后缀名  ")
        self.suffixCB.clicked.connect(self.refreshTreeWeight)
        self.suffixTextEdit.setPlaceholderText('_suffix')
        self.suffixTextEdit.textEdited.connect(self.textConfirm)
        self.extensionCB.setText("扩展名  ")
        self.extensionCB.clicked.connect(self.refreshTreeWeight)
        self.extensionTextEdit.setPlaceholderText('xxx')
        self.extensionTextEdit.textEdited.connect(self.textConfirm)
        self.replaceCB.setText("把内容  ")
        self.replaceCB.clicked.connect(self.refreshTreeWeight)
        self.replaceSTextEdit.textEdited.connect(self.refreshTreeWeight)
        self.replacelabel.setText("   替换为   ")
        self.replaceTTextEdit.textEdited.connect(self.textConfirm)
        self.deleteText.setText("删除")
        
        self.toLocationCB.setText("从第")
        self.toLocationCB.clicked.connect(self.refreshTreeWeight)
        self.startLocationSB.valueChanged.connect(self.refreshTreeWeight)
        self.TextLoclabelB.setText("个字符开始")
        self.TextLoclabelC.setText("   删除 ")
        self.numLocationSB.valueChanged.connect(self.refreshTreeWeight)
        self.TextLoclabelD.setText("个字符")
        self.endLocationCB.setText("从结尾删除")
        self.endLocationCB.clicked.connect(self.refreshTreeWeight)
        self.endNumLocationSB.valueChanged.connect(self.refreshTreeWeight)
        self.TextLoclabelE.setText("个字符")
        self.reNamebutton.setText("重命名")
        self.reNamebutton.clicked.connect(lambda *args: FileTool_BlackC().reNameProc())
        
        self.createNulllabel.setText("创建同名空文件")
        self.createNullTextEdit.setPlaceholderText('目标路径')
        self.createNullButton.setText("Run")

        self.FiletreeWidget.setHeaderLabels(['源文件名', '预览文件名']) #First
        self.unDobutton.setText('<-')
        self.unDobutton.clicked.connect(lambda *args: FileTool_BlackC().unDo())
        self.upMoveItembutton.setText("˄")
        self.upMoveItembutton.clicked.connect(lambda *args: self.tweaksSequence(0))
        self.deleteItembutton.setText("-")
        self.deleteItembutton.clicked.connect(self.deleteSelectFileItem)
        self.dnMoveItembutton.setText("˅")
        self.dnMoveItembutton.clicked.connect(lambda *args: self.tweaksSequence(1))
        
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setCentralWidget(self.Mainwidget)
        
    #def keyPressEvent(self, event):
    #    print(self.focusPreviousChild())
    #    if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
    #        print('delete')
    
    def coustomTextLine(self, direction, parent):
        Line = QtWidgets.QFrame(parent)
        Line.setFrameShadow(QtWidgets.QFrame.Plain)
        Line.setStyleSheet('color:#7d7d7d;')
        if direction == 'H':
            Label = QtWidgets.QLabel(parent)
            Line.setFrameShape(QtWidgets.QFrame.HLine)
            HLy = QtWidgets.QHBoxLayout()
        else:
            Label = coustomVTextLine(parent)
            #oldheight = Label.height()
            Label.setFixedHeight(Label.width())
            #Label.setFixedWidth(oldheight)
            Line.setFrameShape(QtWidgets.QFrame.VLine)
            HLy = QtWidgets.QVBoxLayout()
        Label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred))
        Label.setStyleSheet('color:#7d7d7d;')
        Label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        Line.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred))
        HLy.addWidget(Label)
        HLy.addWidget(Line)
        HLy.setStretch(1, 1)
        return Label, HLy
        #QPainter.initPainter
    
    def changeTab(self, intt):
        #index = self.tabWidget.currentIndex()
        self.FiletreeWidget.clear()
        if index := self.tabWidget.currentIndex():
            self.unDobutton.setVisible(0)
            self.FiletreeWidget.setColumnCount(3)
            self.FiletreeWidget.setHeaderLabels(['名称', '大小', '修改日期'])
        else:
            self.unDobutton.setVisible(1)
            self.FiletreeWidget.setColumnCount(2)
            self.FiletreeWidget.setHeaderLabels(['源文件名', '预览文件名'])
            
    def textConfirm(self, text):
        if text:
            if text[-1] in set(['\\', '/', ':', '*', '?', '"', '<', '>', '|']):
                if text == self.rulesNameTextEdit.text():
                    self.rulesNameTextEdit.backspace()
                elif text == self.prefixTextEdit.text():
                    self.prefixTextEdit.backspace()
                elif text == self.suffixTextEdit.text():
                    self.suffixTextEdit.backspace()
                elif text == self.replaceTTextEdit.text():
                    self.replaceTTextEdit.backspace()
            else:
                self.refreshTreeWeight()
        else:
            self.refreshTreeWeight()
    
    def refreshTreeWeight(self):
        if _treeWidgetList := QtWidgets.QTreeWidgetItemIterator(self.FiletreeWidget):
            itemList = [i.value() for i in _treeWidgetList]
            fileList = [i.text(0) for i in itemList]
            if self.rulesNameCB.isChecked():
                rulesText = self.rulesNameTextEdit.text()
                if reCustomRules := re.search("#\S*\^", rulesText):
                    customRules = reCustomRules.group()
                    for i in range(len(customRules[:-1])):
                        if customRules[i] == '#':
                            prenum = i + 1
                    nameText = rulesText.split(customRules, 1)
                    num = customRules[prenum:-1].split('+')
                    indexNum = int(num[0])
                    if len(num) == 2:
                        addNum = int(num[1])
                    for i in range(len(fileList)):
                        addText = str(indexNum).zfill(prenum)
                        fileList[i] = addText.join(nameText)
                        if len(num) == 2:
                            indexNum += addNum
                        else:
                            indexNum += 1
            if self.prefixCB.isChecked():
                addText = self.prefixTextEdit.text()
                for i in range(len(fileList)):
                    fileList[i] = f'{addText}{fileList[i]}'
            if self.suffixCB.isChecked():
                addText = self.suffixTextEdit.text()
                for i in range(len(fileList)):
                    fileList[i] = f'{fileList[i]}{addText}'
            if self.extensionCB.isChecked():
                addText = self.extensionTextEdit.text()
                for i in range(len(fileList)):
                    fileList[i] = f'{fileList[i]}.{addText}'
            if self.replaceCB.isChecked():
                soureText = self.replaceSTextEdit.text()
                targetText = self.replaceTTextEdit.text()
                if soureText:
                    for i in range(len(fileList)):
                        if soureText in fileList[i]:
                            _temp = fileList[i].split(soureText)
                            fileList[i] = targetText.join(_temp)
            
            if self.toLocationCB.isChecked():
                stValue = self.startLocationSB.value() - 1
                edValue = self.numLocationSB.value()
                for i in range(len(fileList)):
                    _item = fileList[i]
                    if not stValue:
                        fileList[i] = _item[stValue + edValue:]
                    else:
                        fileList[i] = f'{_item[:stValue]}{_item[stValue + edValue:]}'
                    if not fileList[i]:
                        fileList[i] = _item[-1]
            if self.endLocationCB.isChecked():
                numValue = self.endNumLocationSB.value()
                for i in range(len(fileList)):
                    _item = fileList[i][:-numValue]
                    #if not _item:
                    #    _item = fileList[i][:1]
                    fileList[i] = _item
            for i, f in zip(itemList, fileList):
                i.setText(1, f)
    
    def tweaksSequence(self, mode):
        items = self.FiletreeWidget.selectedItems()
        if not items:
            return
        #if mode == 0:
        #    for i in items:
        #        self.FiletreeWidget.setCurrentItem(i, 1)
        #elif mode == 1:
        #    self.FiletreeWidget.sortItems(0, Qt.DescendingOrder)
    
    def deleteSelectFileItem(self):
        _treeWidgetList = QtWidgets.QTreeWidgetItemIterator(self.FiletreeWidget)
        index = self.tabWidget.currentIndex()
        items = self.FiletreeWidget.selectedItems()
        if not _treeWidgetList or not items:
            return
        if not index:
            for i in items:
                self.FiletreeWidget.takeTopLevelItem(self.FiletreeWidget.indexOfTopLevelItem(i))
        elif index == 1:
            for i in items:
                parent = i.parent()
                if parent:
                    parent.removeChild(i)
                else:
                    self.FiletreeWidget.takeTopLevelItem(self.FiletreeWidget.indexOfTopLevelItem(i))

    def testbutton(self, one=''):
        pass

        
class coustomTreeWidget(QtWidgets.QTreeWidget):
    
    def __init__(self, parent):
        super(coustomTreeWidget, self).__init__(parent)
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        #event.answerRect()
        #self.repaint()
        pass
    
    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        inlistData = [i.value().data(0, QtCore.Qt.UserRole) for i in QtWidgets.QTreeWidgetItemIterator(uiItem['FiletreeWidget'])]
        #QTreeWidgetItemIterator(treeWidget)   获取treeWidget下的全部child
        if index := uiItem['tabWidget'].currentIndex():
            for i in list(set(files).difference(set(inlistData))):
                if os.path.isdir(i):
                    for root, dirs, files in os.walk(i):
                        pass

                elif os.path.isfile(i):
                    pass
        else:
            for i in list(set(files).difference(set(inlistData))):
                self.addFileTreeItem(1, i)

    def addFileTreeItem(self, dforf, path):
        icon = QtGui.QIcon(QtWidgets.QFileIconProvider().icon(QtCore.QFileInfo(path)))
        filename = os.path.basename(path).rsplit('.', 1)[0]
        if dforf:
            _oneItem = QtWidgets.QTreeWidgetItem(uiItem['FiletreeWidget'], [filename, filename])
        else:
            KBs = round(os.path.getsize(path) / 1024, 0)     # 命令返回的是字节大小
            size = '%s MB' %KBs / 1024 if KBs > 10000 else '%s KB' %KBs
            _oneItem = QtWidgets.QTreeWidgetItem(uiItem['FiletreeWidget'], [filename, time.strftime("%Y-%m-%d %H:%M", time.localtime(os.stat(path).st_mtime)), size])
        _oneItem.setIcon(0, icon)
        _oneItem.setData(0, QtCore.Qt.UserRole, path)

class coustomVTextLine(QtWidgets.QLabel):
    
    def __init__(self, parent):
        super(coustomVTextLine, self).__init__(parent)

    def initPainter(self, painter):
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(90)
        painter.translate(-self.width() / 2, -self.height() / 2)


class informationWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(informationWidget, self).__init__(parent)
        Pwidth = parent.width()
        self.resize(Pwidth, 28)
        _color = QtGui.QColor(151, 238, 238)
        _color.setAlphaF(0.6)
        _palette = QtGui.QPalette()
        _palette.setBrush(self.backgroundRole(), _color)
        self.setPalette(_palette)
        self.setAutoFillBackground(True)
        self.setGeometry(QtCore.QRect(0, -28, Pwidth, 28))

        self.MainHLayout = QtWidgets.QHBoxLayout(self)
        self.MainHLayout.setSpacing(3)
        self.MainHLayout.setContentsMargins(0, 0, 0, 0)
        #self.MainHLayout.setStretch(1, 1)

        self.msg_label = QtWidgets.QLabel(self)
        self.msg_label.setStyleSheet("background-color: transparent;")
        self.msg_label.setScaledContents(True)
        self.msg_label.setMaximumSize(QtCore.QSize(30, 28))
        self.MainHLayout.addWidget(self.msg_label)

        Pheight = self.height()
        self.ask_label = QtWidgets.QLabel(self)
        self.ask_label.setStyleSheet("background-color: transparent; color: black;")
        self.ask_label.setAlignment(QtCore.Qt.AlignCenter)
        self.MainHLayout.addWidget(self.ask_label)
        
        close_button = QtWidgets.QToolButton(self)
        close_pix = self.style().standardPixmap(QtWidgets.QStyle.SP_TitleBarCloseButton)
        close_button.setIcon(close_pix)
        close_button.setStyleSheet("QToolButton{background-color: transparent;}")
        close_button.setCursor(QtCore.Qt.PointingHandCursor)
        close_button.setMaximumSize(QtCore.QSize(30, 28))
        self.MainHLayout.addWidget(close_button)

        close_button.clicked.connect(lambda *args: self.hideMine())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()
        
        self.QanimationVis = QtCore.QPropertyAnimation(self, b"geometry")
        self.QanimationVis.setDuration(300)   #设置动画时间为1秒
        self.QanimationVis.setStartValue(QtCore.QRect(0, -28, self.width(), self.height()))
        self.QanimationVis.setEndValue(QtCore.QRect(0, 0, self.width(), self.height()))
        self.QanimationHid = QtCore.QPropertyAnimation(self, b"geometry")
        self.QanimationHid.setDuration(300)
        self.QanimationHid.setStartValue(QtCore.QRect(0, 0, self.width(), self.height()))
        self.QanimationHid.setEndValue(QtCore.QRect(0, -28, self.width(), self.height()))
        
    def setTextPixmap(self, text, mapfile):
        self.ask_label.setText(text)
        self.msg_label.setPixmap(QtGui.QPixmap(mapfile))
        self.QanimationVis.start()
        
    def hideMine(self):
        self.QanimationHid.start()


class FileTool_BlackC():

    def reNameProc(self):
        _treeWidgetList = QtWidgets.QTreeWidgetItemIterator(uiItem['FiletreeWidget'])
        if not _treeWidgetList:
            return
        itemList = [i.value() for i in _treeWidgetList]
        newNameList = [[i.text(1), i.data(0, QtCore.Qt.UserRole)] for i in itemList]
        unDoData.append([])
        for i, w in zip(newNameList, itemList):
            _dir = os.path.dirname(i[1])
            _ext = os.path.splitext(i[1])[-1]
            _newFile = f'{_dir}/{i[0]}' if uiItem['extensionCB'].isChecked() else f'{_dir}/{i[0]}{_ext}'
            if os.path.exists(_newFile):
                informationWidget(um).setTextPixmap('有重名文件或文件夹, 已经跳过', '')
                continue
            os.rename(i[1], _newFile)
            w.setText(0, i[0])
            w.setData(0, QtCore.Qt.UserRole, _newFile)
            unDoData[-1].append((_newFile, i[1]))

    def unDo(self):
        if unDoData:
            for i in unDoData[-1]:
                os.rename(i[0], i[1])
            del(unDoData[-1])
            uiItem['FiletreeWidget'].clear()   #暂时懒得回写数据
        else:
            informationWidget(um).setTextPixmap('没有可撤销的操作', '')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #print(QStyleFactory.keys())   #当前支持的Style
    #QApplication.setStyle(QStyleFactory.create('Fusion'))
    um = FileTool_BlackC_Ui()
    um.show()
    sys.exit(app.exec_())
