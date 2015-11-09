
#include <QtGui>
#include <QtCore>
#include <QApplication>
#include <QPushButton>
#include <QLabel>
#include <QHBoxLayout>
#include <QTextEdit> /* multi line */
#include <QLineEdit> /* single line */
#include <QMainWindow>
#include <QDropEvent>
#include <QDrag>
#include <QUrl>
#include <QMimeData>

class Interface : public QMainWindow
{
	Q_OBJECT

private:
	QWidget *window;
	QLabel *titleLabel;
	QLabel *image;
	QLabel *filenameLabel;
	QLabel *resultLabel, *valueLabel;
	QVBoxLayout *mainLayout;
	QVBoxLayout *labelLayout;
	QVBoxLayout *inputLayout;
	QHBoxLayout *winLayout;
	QLineEdit *filenameLine;
	QLineEdit *resultLine, *valueLine;

public:
	Interface();
	~Interface();
	void createWindow(void);
	void loadImage(char *);
	//void dragEnterEvent(QDragEnterEvent *e);
	//void dropEvent(QDropEvent *e);
};
