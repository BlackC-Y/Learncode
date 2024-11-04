#include "coustomTreeWidget.h"

#include <iostream>
using namespace std;


coustomTreeWidget::coustomTreeWidget(QWidget* parent) : QTreeWidget(parent)
{
	this->setAcceptDrops(true);
}

void coustomTreeWidget::dragEnterEvent(QDragEnterEvent* event)
{
    if (event->mimeData()->hasUrls())
        event->accept();
    else
        event->ignore();
}

void coustomTreeWidget::dragMoveEvent(QDragMoveEvent* event)
{
}

void coustomTreeWidget::dropEvent(QDropEvent* event)
{   
    auto urlList = event->mimeData()->urls();
    QString locaFile;
    for (QUrl& u : urlList)
    {
        auto a = u.toLocalFile();
        a.sprintf("%s\n", u.toLocalFile());
    }
    /*
    files = [u.toLocalFile() for u in event.mimeData().urls()]
        inlistData = [i.value().data(0, Qt.UserRole) for i in QTreeWidgetItemIterator(uiItem['FiletreeWidget'])]
        #QTreeWidgetItemIterator(treeWidget)   获取treeWidget下的全部child
        if index : = uiItem['tabWidget'].currentIndex() :
            for i in list(set(files).difference(set(inlistData))) :
                if os.path.isdir(i) :
                    for root, dirs, files in os.walk(i) :
                        pass

                        elif os.path.isfile(i) :
                        pass
                else:
    for i in list(set(files).difference(set(inlistData))) :
        self.addFileTreeItem(1, i)
    */
}

void coustomTreeWidget::addFileTreeItem(bool dforf, QString path)
{
}