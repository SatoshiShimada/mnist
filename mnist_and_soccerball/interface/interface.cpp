
#include <QtGui>
#include "interface.h"
#include <iostream>
#include <string.h>

void callPython(std::string, char *);

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
		std::cerr << "Error: can\'t open image file" << std::endl;
		return;
	}
	QPixmap map = QPixmap::fromImage(image_buf);
	map = map.scaled(280, 280);
	image->setPixmap(map);
}

void Interface::loadImage(const char *image_filename)
{
	QImage image_buf(image_filename);
	if(image_buf.isNull()) {
		std::cerr << "Error: can\'t open image file" << std::endl;
		return;
	}
	QPixmap map = QPixmap::fromImage(image_buf);
	map = map.scaled(280, 280);
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
	filenameLine->setText(filenameDrag);
	loadImage(filenameDrag);
	
	/* save image filename to file */
	char buf[1024];
	callPython(filenameDrag.toStdString(), buf);
	char dimension[1024], value[1024];

	/* split result to dimension and value */
	int j = 0;
	for(int i = 0; buf[i] != '\0'; i++) {
		if(buf[i] == ',') {
			dimension[j++] = '\0';
			break;
		}
		dimension[j++] = buf[i];
	}
	strcpy(value, buf + j);

	if(!strcmp(dimension, "10")) {
		resultLine->setText("Ball");
	} else {
		resultLine->setText(dimension);
	}
	valueLine->setText(value);
}

