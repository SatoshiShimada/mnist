
#ifndef __PAINT_H__
#define __PAINT_H__

#include <QtGui>
#include <QWidget>
#include <QPixmap>
#include <QGraphicsPixmapItem>
#include <QPainter>
#include <QLabel>
#include <QPushButton>
#include <QHBoxLayout>

class PaintArea : public QLabel
{
Q_OBJECT
public:
	PaintArea();
	void setPenWidth(int);
protected:
	//void paintEvent(QPaintEvent *event);
	void mousePressEvent(QMouseEvent *event);
	void mouseReleaseEvent(QMouseEvent *event);
	void mouseMoveEvent(QMouseEvent *event);
	void drawPointOnPixmap(int x, int y);
private:
	QPixmap *mainPixmap;
	int prev_x, prev_y;
	int lineWeight;
public slots:
	void resetPixmapArea(void);
	void savePixmapImage(void);
};

#endif //__PAINT_H__
