
#include <iostream>
#include <QtGui>
#include <QtCore>
#include <QApplication>
#include <QPushButton>
#include <QLabel>
#include <QTextEdit> /* multi line */
#include <QLineEdit> /* single line */
#include <QMainWindow>
#include <QDropEvent>
#include <QDrag>
#include <QUrl>
#include <QMimeData>
#include <QString>

#include "paint.h"

class Interface : public QMainWindow
{
	Q_OBJECT

private:
	PaintArea *paintarea;
	QString filenameDrag;
	QWidget *window;
	QLabel *titleLabel;
	QLabel *image;
	QLabel *filenameLabel;
	QLabel *resultLabel, *valueLabel;
	QLabel *penWidthLabel;
	QPushButton *clearButton;
	QPushButton *saveButton;
	QPushButton *evaluateButton;
	QLineEdit *filenameLine;
	QLineEdit *resultLine, *valueLine;
	QSlider *penWidthSlider;
	QVBoxLayout *mainLayout;
	QGridLayout *labelLayout;
	QHBoxLayout *winLayout;
	void connection(void);

public:
	Interface();
	~Interface();
	void createWindow(void);
	void loadImage(const char *);
	void loadImage(QString);
	void dragEnterEvent(QDragEnterEvent *e);
	void dropEvent(QDropEvent *e);

private slots:
	void clearImage(void);
	void saveImage(void);
	void evaluateImage(void);
	void penWidthChanged(void);
};

