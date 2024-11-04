#include "FileTool_Qt_Ui.h"
#include <QtWidgets/QApplication>

int main(int argc, char* argv[])
{
	QApplication a(argc, argv);
	FileTool_Qt_Ui w;
	w.show();
	return a.exec();
}