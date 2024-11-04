#pragma once
#include <QtWidgets/QTreeWidget>
#include <QtWidgets/QWidget>
#include <QtGui/QDragEnterEvent>
#include <QtGui/QDragMoveEvent>
#include <QtGui/QDropEvent>
#include <QtCore/QMimeData>
#include <QtCore/QUrl>

class coustomTreeWidget : public QTreeWidget
{
	Q_OBJECT

public:
	explicit coustomTreeWidget(QWidget* parent = Q_NULLPTR);
	void addFileTreeItem(bool dforf, QString path);

protected:
	void dragEnterEvent(QDragEnterEvent* event) override;
	void dragMoveEvent(QDragMoveEvent* event) override;
	void dropEvent(QDropEvent* event) override;
};