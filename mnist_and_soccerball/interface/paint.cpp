
#include "paint.h"
#include <iostream>

PaintArea::PaintArea() : QLabel()
{
	prev_x = -1;
	prev_y = -1;
	lineWeight = 15;
	mainPixmap = new QPixmap(280, 280);
	QPainter paint(mainPixmap);
	paint.setPen(Qt::black);
	paint.setBrush(Qt::black);
	paint.drawRect(0, 0, 280, 280);
	this->resize(280, 280);
	this->setPixmap(*mainPixmap);
	this->update();
}

/*
void PaintArea::paintEvent(QPaintEvent *event)
{
}
*/

void PaintArea::drawPointOnPixmap(int x, int y)
{
	QPainter paint(mainPixmap);
	const QPen pen(Qt::white, lineWeight);
	paint.setPen(pen);
	paint.setBrush(Qt::white);
	int x_diff = (this->size().width() - 280) / 2;
	int y_diff = (this->size().height() - 280) / 2;
	x = x - x_diff;
	y = y - y_diff;
	if(prev_x == -1 || prev_y == -1) {
		paint.drawPoint(x, y);
	} else {
		paint.drawLine(prev_x, prev_y, x, y);
	}
	this->setPixmap(*mainPixmap);
	this->update();
	prev_x = x;
	prev_y = y;
}

void PaintArea::mousePressEvent(QMouseEvent *event)
{
	if(event->button() == Qt::LeftButton) {
		drawPointOnPixmap(event->x(), event->y());
	}
}

void PaintArea::mouseReleaseEvent(QMouseEvent *event)
{
	if((event->button() & Qt::LeftButton))
		prev_x = prev_y = -1;
}

void PaintArea::mouseMoveEvent(QMouseEvent *event)
{
	if(event->button() == Qt::NoButton) {
		drawPointOnPixmap(event->x(), event->y());
	}
}

void PaintArea::resetPixmapArea(void)
{
	mainPixmap->fill(Qt::black);
	this->setPixmap(*mainPixmap);
	this->update();
}

void PaintArea::savePixmapImage(void)
{
	const char *filename = "out.png";
	QString QFilename = QString(filename);
	mainPixmap->save(QFilename);
}

void PaintArea::setPenWidth(int width)
{
	this->lineWeight = width;
}

