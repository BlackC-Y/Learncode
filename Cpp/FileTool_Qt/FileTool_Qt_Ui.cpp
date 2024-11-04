#include "FileTool_Qt_Ui.h"
#include "coustomVTextLine.h"
#include "coustomTreeWidget.h"
#include "Windows.h"
#include <string>
#include <iostream>

using namespace std;

FileTool_Qt_Ui::FileTool_Qt_Ui(QWidget* parent) : QMainWindow(parent)
{
    if (this->objectName().isEmpty())
        this->setObjectName(QString::fromUtf8("FileTool_Qt_Ui"));
    this->resize(800, 500);
    this->setMinimumSize(QSize(650, 400));
    Mainwidget = new QWidget(this);
    Mainwidget->setObjectName(QString::fromUtf8("Mainwidget"));
    Mainwidget->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);

    MainHLayout = new QHBoxLayout(Mainwidget);
    MainHLayout->setObjectName(QString::fromUtf8("MainHLayout"));
    MainHLayout->setSpacing(3);
    MainHLayout->setSizeConstraint(QLayout::SetMinimumSize);
    MainHLayout->setContentsMargins(5, 5, 5, 5);

    tabWidget = new QTabWidget(Mainwidget);
    tabWidget->setObjectName(QString::fromUtf8("tabWidget"));
    tabWidget->setMinimumSize(QSize(300, 380));
    reNameTab = new QWidget(tabWidget);
    reNameTab->setObjectName(QString::fromUtf8("reNameTab"));
    reNamePageVLayout = new QVBoxLayout(reNameTab);
    reNamePageVLayout->setObjectName(QString::fromUtf8("reNamePageVLayout"));

    //Page 1 reName
    _tempHLayout = new QHBoxLayout();
    createText = coustomTextLine(reNameTab, _tempHLayout);
    reNamePageVLayout->addLayout(_tempHLayout);

    _tempHLayout = new QHBoxLayout();
    _tempHLayout->setSpacing(20);
    rulesNameCB = new QCheckBox(reNameTab);
    rulesNameCB->setObjectName(QString::fromUtf8("rulesNameCB"));
    _tempHLayout->addWidget(rulesNameCB);
    rulesNameTextEdit = new QLineEdit(reNameTab);
    rulesNameTextEdit->setObjectName(QString::fromUtf8("rulesNameTextEdit"));
    _tempHLayout->addWidget(rulesNameTextEdit);
    _tempHLayout->addItem(new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum));
    reNamePageVLayout->addLayout(_tempHLayout);

    _tempHLayout = new QHBoxLayout();
    _tempHLayout->setSpacing(20);
    prefixCB = new QCheckBox(reNameTab);
    prefixCB->setObjectName(QString::fromUtf8("prefixCB"));
    _tempHLayout->addWidget(prefixCB);
    prefixTextEdit = new QLineEdit(reNameTab);
    prefixTextEdit->setObjectName(QString::fromUtf8("prefixTextEdit"));
    _tempHLayout->addWidget(prefixTextEdit);
    _tempHLayout->addItem(new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum));
    reNamePageVLayout->addLayout(_tempHLayout);

    _tempHLayout = new QHBoxLayout();
    _tempHLayout->setSpacing(20);
    suffixCB = new QCheckBox(reNameTab);
    suffixCB->setObjectName(QString::fromUtf8("suffixCB"));
    _tempHLayout->addWidget(suffixCB);
    suffixTextEdit = new QLineEdit(reNameTab);
    suffixTextEdit->setObjectName(QString::fromUtf8("suffixTextEdit"));
    _tempHLayout->addWidget(suffixTextEdit);
    _tempHLayout->addItem(new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum));
    reNamePageVLayout->addLayout(_tempHLayout);

    _tempHLayout = new QHBoxLayout();
    _tempHLayout->setSpacing(20);
    extensionCB = new QCheckBox(reNameTab);
    extensionCB->setObjectName(QString::fromUtf8("extensionCB"));
    _tempHLayout->addWidget(extensionCB);
    extensionTextEdit = new QLineEdit(reNameTab);
    extensionTextEdit->setObjectName(QString::fromUtf8("extensionTextEdit"));
    _tempHLayout->addWidget(extensionTextEdit);
    _tempHLayout->addItem(new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum));
    reNamePageVLayout->addLayout(_tempHLayout);

    _tempVLayout = new QVBoxLayout();
    _tempHLayout = new QHBoxLayout();
    _tempHLayout->setSpacing(20);
    replaceCB = new QCheckBox(reNameTab);
    replaceCB->setObjectName(QString::fromUtf8("replaceCB"));
    _tempHLayout->addWidget(replaceCB);
    replaceSTextEdit = new QLineEdit(reNameTab);
    replaceSTextEdit->setObjectName(QString::fromUtf8("replaceSTextEdit"));
    _tempHLayout->addWidget(replaceSTextEdit);
    _tempHLayout->addItem(new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum));
    _tempVLayout->addLayout(_tempHLayout);

    _tempHLayout = new QHBoxLayout();
    _tempHLayout->setSpacing(20);
    replacelabel = new QLabel(reNameTab);
    _tempHLayout->addWidget(replacelabel);
    replaceTTextEdit = new QLineEdit(reNameTab);
    replaceTTextEdit->setObjectName(QString::fromUtf8("replaceTTextEdit"));
    _tempHLayout->addWidget(replaceTTextEdit);
    _tempHLayout->addItem(new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum));
    _tempVLayout->addLayout(_tempHLayout);
    reNamePageVLayout->addLayout(_tempVLayout);

    //delete
    _tempHLayout = new QHBoxLayout();
    deleteText = coustomTextLine(reNameTab, _tempHLayout);
    reNamePageVLayout->addLayout(_tempHLayout);

    _tempVLayout = new QVBoxLayout();
    _tempHLayout = new QHBoxLayout();
    _tempHLayout->setSpacing(20);
    toLocationCB = new QCheckBox(reNameTab);
    toLocationCB->setObjectName(QString::fromUtf8("toLocationCB"));
    _tempHLayout->addWidget(toLocationCB);
    startLocationSB = new QSpinBox(reNameTab);
    startLocationSB->setObjectName(QString::fromUtf8("startLocationSB"));
    startLocationSB->setMinimumSize(QSize(45, 20));
    startLocationSB->setMinimum(1);
    _tempHLayout->addWidget(startLocationSB);
    TextLoclabelB = new QLabel(reNameTab);
    _tempHLayout->addWidget(TextLoclabelB);
    _tempHLayout->addItem(new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum));
    _tempVLayout->addLayout(_tempHLayout);

    _tempHLayout = new QHBoxLayout();
    _tempHLayout->setSpacing(20);
    TextLoclabelC = new QLabel(reNameTab);
    _tempHLayout->addWidget(TextLoclabelC);
    endLocationSB = new QSpinBox(reNameTab);
    endLocationSB->setObjectName(QString::fromUtf8("endLocationSB"));
    endLocationSB->setMinimumSize(QSize(45, 20));
    endLocationSB->setMinimum(1);
    _tempHLayout->addWidget(endLocationSB);
    TextLoclabelD = new QLabel(reNameTab);
    _tempHLayout->addWidget(TextLoclabelD);
    _tempHLayout->addItem(new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum));
    _tempVLayout->addLayout(_tempHLayout);
    reNamePageVLayout->addLayout(_tempVLayout);

    reNamebutton = new QPushButton(reNameTab);
    reNamebutton->setMinimumSize(QSize(80, 26));
    reNamebutton->setObjectName(QString::fromUtf8("reNamebutton"));
    reNamePageVLayout->addItem(new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding));
    reNamePageVLayout->addWidget(reNamebutton);
    tabWidget->addTab(reNameTab, "");

    //Page 2 File
    fileTab = new QWidget(tabWidget);
    fileTab->setObjectName(QString::fromUtf8("fileTab"));

    tabWidget->addTab(fileTab, "");
    tabWidget->setCurrentIndex(0);
    MainHLayout->addWidget(tabWidget);

    twHLayout = new QHBoxLayout();
    twHLayout->setObjectName(QString::fromUtf8("twHLayout"));
    FiletreeWidget = new coustomTreeWidget(Mainwidget);
    FiletreeWidget->setObjectName(QString::fromUtf8("FiletreeWidget"));
    FiletreeWidget->setMinimumSize(QSize(300, 380));
    FiletreeWidget->setRootIsDecorated(false);
    FiletreeWidget->setSelectionMode(QAbstractItemView::ExtendedSelection);
    FiletreeWidget->setSortingEnabled(true);
    //FiletreeWidget.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum));
    //icon = QIcon();
    //icon.addFile("C:/Users/yangbanghui/Desktop/aaa.png", QSize(), QIcon.Normal, QIcon.Off);
    //item_0 = QTreeWidgetItem(FiletreeWidget);
    //item_0.setIcon(0, icon);
    twHLayout->addWidget(FiletreeWidget);

    buttonVLayout = new QVBoxLayout();
    buttonVLayout->setSpacing(3);
    buttonVLayout->setObjectName(QString::fromUtf8("buttonVLayout"));
    buttonVLayout->setContentsMargins(2, 0, 2, 0);

    unDobutton = new QPushButton(Mainwidget);
    unDobutton->setObjectName(QString::fromUtf8("unDobutton"));
    unDobutton->setMaximumSize(QSize(35, 35));
    buttonVLayout->addWidget(unDobutton);
    buttonVLayout->addItem(new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding));

    upMoveItembutton = new QPushButton(Mainwidget);
    upMoveItembutton->setObjectName(QString::fromUtf8("upMoveItembutton"));
    upMoveItembutton->setMaximumSize(QSize(35, 35));
    buttonVLayout->addWidget(upMoveItembutton);

    deleteItembutton = new QPushButton(Mainwidget);
    deleteItembutton->setObjectName(QString::fromUtf8("deleteItembutton"));
    deleteItembutton->setMaximumSize(QSize(35, 35));
    buttonVLayout->addWidget(deleteItembutton);

    dnMoveItembutton = new QPushButton(Mainwidget);
    dnMoveItembutton->setObjectName(QString::fromUtf8("dnMoveItembutton"));
    dnMoveItembutton->setMaximumSize(QSize(35, 35));
    buttonVLayout->addWidget(dnMoveItembutton);
    buttonVLayout->addItem(new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding));

    twHLayout->addLayout(buttonVLayout);
    MainHLayout->addLayout(twHLayout);

    this->setWindowTitle(QString::fromUtf8("FileTool"));
    tabWidget->setTabText(tabWidget->indexOf(reNameTab), QString::fromUtf8("重命名"));
    tabWidget->setTabText(tabWidget->indexOf(fileTab), QString::fromUtf8("File"));
    QObject::connect(tabWidget, SIGNAL(currentChanged(int)), this, SLOT(changeTab()));
    createText->setText(QString::fromUtf8("添加/替换"));
    rulesNameCB->setText(QString::fromUtf8("规则命名"));
    QObject::connect(rulesNameCB, SIGNAL(clicked()), this, SLOT(refreshTreeWeight()));
    rulesNameTextEdit->setPlaceholderText("xxx_#1^");
    rulesNameTextEdit->setToolTip(QString::fromUtf8("#代表字符数量\n接初始序号 再用+号可添加步进或步减\n^进行结尾\n \
                                  \neg:aa_###1 + 2 ^ _zz = aa_001_zz / aa_003_zz \neg : aa_##10 + -2 ^ _zz = aa_10_zz / aa_08_zz"));
    QObject::connect(rulesNameTextEdit, SIGNAL(textEdited(QString)), this, SLOT(textConfirm(QString)));
    prefixCB->setText(QString::fromUtf8("前缀名  "));
    QObject::connect(prefixCB, SIGNAL(clicked()), this, SLOT(refreshTreeWeight()));
    prefixTextEdit->setPlaceholderText(QString::fromUtf8("prefix_"));
    QObject::connect(prefixTextEdit, SIGNAL(textEdited(QString)), this, SLOT(textConfirm(QString)));
    suffixCB->setText(QString::fromUtf8("后缀名  "));
    QObject::connect(suffixCB, SIGNAL(clicked()), this, SLOT(refreshTreeWeight()));
    suffixTextEdit->setPlaceholderText(QString::fromUtf8("_suffix"));
    QObject::connect(suffixTextEdit, SIGNAL(textEdited(QString)), this, SLOT(textConfirm(QString)));
    extensionCB->setText(QString::fromUtf8("扩展名  "));
    QObject::connect(extensionCB, SIGNAL(clicked()), this, SLOT(refreshTreeWeight()));
    extensionTextEdit->setPlaceholderText(QString::fromUtf8("xxx"));
    QObject::connect(extensionTextEdit, SIGNAL(textEdited(QString)), this, SLOT(textConfirm(QString)));
    replaceCB->setText(QString::fromUtf8("把内容  "));
    QObject::connect(replaceCB, SIGNAL(clicked()), this, SLOT(refreshTreeWeight()));
    QObject::connect(replaceSTextEdit, SIGNAL(textEdited()), this, SLOT(refreshTreeWeight()));
    replacelabel->setText(QString::fromUtf8("   替换为   "));
    QObject::connect(replaceTTextEdit, SIGNAL(textEdited(QString)), this, SLOT(textConfirm(QString)));
    deleteText->setText(QString::fromUtf8("删除"));

    toLocationCB->setText(QString::fromUtf8("从第"));
    QObject::connect(toLocationCB, SIGNAL(clicked()), this, SLOT(refreshTreeWeight()));
    QObject::connect(startLocationSB, SIGNAL(valueChanged()), this, SLOT(refreshTreeWeight()));
    TextLoclabelB->setText(QString::fromUtf8("个字符开始"));
    TextLoclabelC->setText(QString::fromUtf8("   删除 "));
    QObject::connect(endLocationSB, SIGNAL(valueChanged()), this, SLOT(refreshTreeWeight()));
    TextLoclabelD->setText(QString::fromUtf8("个字符"));
    reNamebutton->setText(QString::fromUtf8("重命名"));
    QObject::connect(reNamebutton, SIGNAL(clicked()), this, SLOT(FileTool_Main::reNameProc()));

    FiletreeWidget->setHeaderLabels({ QString::fromUtf8("源文件名"), QString::fromUtf8("预览文件名")});
    unDobutton->setText(QString::fromUtf8("<-"));
    QObject::connect(unDobutton, SIGNAL(clicked()), this, SLOT(FileTool_Main::unDo()));
    upMoveItembutton->setText(QString::fromUtf8("˄"));
    QObject::connect(upMoveItembutton, SIGNAL(clicked()), this, SLOT(tweaksSequence(0)));
    deleteItembutton->setText(QString::fromUtf8("-"));
    QObject::connect(deleteItembutton, SIGNAL(clicked()), this, SLOT(deleteSelectFileItem));
    dnMoveItembutton->setText(QString::fromUtf8("˅"));
    QObject::connect(dnMoveItembutton, SIGNAL(clicked()), this, SLOT(tweaksSequence(1)));

    QMetaObject::connectSlotsByName(this);
    this->setWindowFlags(Qt::Window);
    this->setCentralWidget(Mainwidget);

    //OutputDebugString(L"1\n\n");
    
}

QLabel* FileTool_Qt_Ui::coustomTextLine(QWidget* parent, QHBoxLayout* HLy)
{
    Line = new QFrame(parent);
    Line->setFrameShadow(QFrame::Plain);
    Line->setStyleSheet("color:#7d7d7d;");
    Label = new QLabel(parent);
    Line->setFrameShape(QFrame::HLine);
    //HLy = new QHBoxLayout();
    Label->setSizePolicy(QSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred));
    Label->setStyleSheet("color:#7d7d7d;");
    Label->setAlignment(Qt::AlignCenter);
    Line->setSizePolicy(QSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred));
    HLy->addWidget(Label);
    HLy->addWidget(Line);
    HLy->setStretch(1, 1);
    return Label;
}

QLabel* FileTool_Qt_Ui::coustomTextLine(QWidget* parent, QVBoxLayout* VLy)
{
    Line = new QFrame(parent);
    Line->setFrameShadow(QFrame::Plain);
    Line->setStyleSheet("color:#7d7d7d;");
    Label = new coustomVTextLine(parent);
    //oldheight = Label->height();
    Label->setFixedHeight(Label->width());
    //Label->setFixedWidth(oldheight);
    Line->setFrameShape(QFrame::VLine);
    //VLy = new QVBoxLayout();
    Label->setSizePolicy(QSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred));
    Label->setStyleSheet("color:#7d7d7d;");
    Label->setAlignment(Qt::AlignCenter);
    Line->setSizePolicy(QSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred));
    VLy->addWidget(Label);
    VLy->addWidget(Line);
    VLy->setStretch(1, 1);
    return Label;
}

void FileTool_Qt_Ui::changeTab()
{
    FiletreeWidget->clear();
    int index = tabWidget->currentIndex();
    if (index == 0)
    {
        FiletreeWidget->setColumnCount(2);
        FiletreeWidget->setHeaderLabels({ "源文件名", "预览文件名" });
    }
    else if (index == 1)
    {
        FiletreeWidget->setColumnCount(3);
        FiletreeWidget->setHeaderLabels({ "名称", "大小", "修改日期" });
    }
}

void FileTool_Qt_Ui::textConfirm(QString text)
{
    if (!text.isEmpty())
    {
        QChar errorchar[9] = { '\\', '/', ':', '*', '?', '"', ' < ', ' > ', ' | ' };
        for (QChar& i : errorchar)
        {
            QCharRef temp = text.back();
            if (temp == i)
            {   
                if (text == rulesNameTextEdit->text())
                    rulesNameTextEdit->backspace();
                else if (text == prefixTextEdit->text())
                    prefixTextEdit->backspace();
                else if (text == suffixTextEdit->text())
                    suffixTextEdit->backspace();
                else if (text == replaceTTextEdit->text())
                    replaceTTextEdit->backspace();
            }
            else
                refreshTreeWeight();
        }
    }
    else
        refreshTreeWeight();
}

void FileTool_Qt_Ui::refreshTreeWeight()
{
    QTreeWidgetItemIterator _treeWidgetList = QTreeWidgetItemIterator(FiletreeWidget);
}

void FileTool_Qt_Ui::tweaksSequence(int mode)
{

}

void FileTool_Qt_Ui::deleteSelectFileItem()
{

}