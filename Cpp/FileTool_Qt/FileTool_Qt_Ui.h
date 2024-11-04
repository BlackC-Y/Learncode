#pragma once
#pragma execution_character_set("utf-8")
#ifndef MAINWINDOW_H
#define MAINWINDOW_H


#include <QtCore/QVariant>
#include <QtCore/QMetaObject>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QTreeWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>
#include <QtWidgets/QLabel>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QFrame>
#include <QtWidgets/QSpacerItem>
#include <QtCore/QTextCodec>

namespace Ui {
	class FileTool_Qt_Ui;
}

class FileTool_Qt_Ui : public QMainWindow
{
	Q_OBJECT

public:
	QWidget* Mainwidget;
	QHBoxLayout* MainHLayout;
	QTabWidget* tabWidget;
	QWidget* reNameTab;
	QVBoxLayout* reNamePageVLayout;

	QLabel* createText;
	QHBoxLayout* _tempHLayout;
	QVBoxLayout* _tempVLayout;
	QCheckBox* rulesNameCB;
	QLineEdit* rulesNameTextEdit;
	QCheckBox* prefixCB;
	QLineEdit* prefixTextEdit;
	QCheckBox* suffixCB;
	QLineEdit* suffixTextEdit;
	QCheckBox* extensionCB;
	QLineEdit* extensionTextEdit;
	QCheckBox* replaceCB;
	QLineEdit* replaceSTextEdit;
	QLabel* replacelabel;
	QLineEdit* replaceTTextEdit;
	QLabel* deleteText;
	QCheckBox* toLocationCB;
	QSpinBox* startLocationSB;
	QLabel* TextLoclabelB;
	QLabel* TextLoclabelC;
	QSpinBox* endLocationSB;
	QLabel* TextLoclabelD;

	QPushButton* reNamebutton;
	QWidget* fileTab;
	QHBoxLayout* twHLayout;
	QTreeWidget* FiletreeWidget;
	QVBoxLayout* buttonVLayout;
	QPushButton* unDobutton;
	QPushButton* upMoveItembutton;
	QPushButton* deleteItembutton;
	QPushButton* dnMoveItembutton;

	QFrame* Line;
	QLabel* Label;
	QHBoxLayout* HLy;
	QVBoxLayout* VLy;

public:
	explicit FileTool_Qt_Ui(QWidget* parent = Q_NULLPTR);
	//~FileTool_Qt_Ui();
	QLabel* coustomTextLine(QWidget* parent, QHBoxLayout* HLy);
	QLabel* coustomTextLine(QWidget* parent, QVBoxLayout* VLy);
	
public slots:   //声明后意味着任何对象都可以连接
	void changeTab();
	void textConfirm(QString text);
	void refreshTreeWeight();
	void tweaksSequence(int mode);
	void deleteSelectFileItem();

signals:   //发出动作
	void currentChanged(int);
	void clicked();
	void textEdited(QString);


//private:
	//Ui::FileTool_Qt_Ui* ui;
};

#endif // MAINWINDOW_H

