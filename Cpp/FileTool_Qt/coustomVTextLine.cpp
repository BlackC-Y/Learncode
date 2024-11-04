#include "coustomVTextLine.h"

coustomVTextLine::coustomVTextLine(QWidget* parent) : QLabel(parent)
{
}

void coustomVTextLine::initPainter(QPainter* painter)
{
	painter->translate(this->width() / 2, this->height() / 2);
	painter->rotate(90);
	painter->translate(-this->width() / 2, -this->height() / 2);
}