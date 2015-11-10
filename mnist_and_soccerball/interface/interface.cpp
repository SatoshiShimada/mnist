
#include <QtGui>
#include "interface.h"

int main(int argc, char **argv)
{
	QApplication app(argc, argv);
	Interface *interface = new Interface;
	//interface->resize(300, 300)

	interface->show();
	return app.exec();
}

Interface::Interface()
{
	setAcceptDrops(true);
	createWindow();
}

Interface::~Interface()
{
}

void Interface::createWindow(void)
{
	window        = new QWidget;
	titleLabel    = new QLabel("mnist and ball");
	image         = new QLabel();
	filenameLabel = new QLabel("Image file name: ");
	resultLabel   = new QLabel("Result: ");
	valueLabel    = new QLabel("Value: ");
	mainLayout    = new QVBoxLayout;
	winLayout     = new QHBoxLayout;
	labelLayout   = new QVBoxLayout;
	inputLayout   = new QVBoxLayout;
	filenameLine  = new QLineEdit;
	resultLine    = new QLineEdit;
	valueLine     = new QLineEdit;

	resultLine->setReadOnly(true);
	valueLine->setReadOnly(true);
	//resultLine->setText("2");

	labelLayout->addWidget(filenameLabel);
	labelLayout->addWidget(resultLabel);
	labelLayout->addWidget(valueLabel);

	inputLayout->addWidget(filenameLine);
	inputLayout->addWidget(resultLine);
	inputLayout->addWidget(valueLine);

	winLayout->addLayout(labelLayout);
	winLayout->addLayout(inputLayout);
	winLayout->addWidget(image);
	mainLayout->addWidget(titleLabel);
	mainLayout->addLayout(winLayout);

	window->setLayout(mainLayout);
	setCentralWidget(window);
}

void Interface::loadImage(QString image_filename)
{
	QImage image_buf(image_filename);
	if(image_buf.isNull()) {
		return;
	}
	image->setPixmap(QPixmap::fromImage(image_buf));
}

void Interface::loadImage(const char *image_filename)
{
	QImage image_buf(image_filename);
	if(image_buf.isNull()) {
		return;
	}
	image->setPixmap(QPixmap::fromImage(image_buf));
}

void Interface::dragEnterEvent(QDragEnterEvent *e)
{
	if(e->mimeData()->hasFormat("text/uri-list"))
	{
		e->acceptProposedAction();
	}
}

void Interface::dropEvent(QDropEvent *e)
{
	filenameDrag = e->mimeData()->urls().first().toLocalFile();
	titleLabel->setText(e->mimeData()->urls().first().toLocalFile());
	//loadImage("../ball_image/ball_0001.png");
	loadImage(filenameDrag);
}

