#pragma once
#include <QtWidgets/QWidget>
#include <QtWidgets/QLabel>
#include <QtGui/QPainter>

class coustomVTextLine : public QLabel
{
	Q_OBJECT

public:
	explicit coustomVTextLine(QWidget* parent = Q_NULLPTR);

private:
	void initPainter(QPainter* painter);
};