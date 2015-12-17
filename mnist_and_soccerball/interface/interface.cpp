
#include <QtGui>
#include "interface.h"
#include "paint.h"
#include <iostream>
#include <string.h>

void callPython(std::string, char *);

Interface::Interface()
{
	setAcceptDrops(true);
	createWindow();
	connection();
	this->resize(840, 320);
}

Interface::~Interface()
{
}

void Interface::createWindow(void)
{
	window         = new QWidget;
	titleLabel     = new QLabel("Hand-written numeral recognition");
	image          = new QLabel;
	filenameLabel  = new QLabel("Image file name: ");
	resultLabel    = new QLabel("Result: ");
	valueLabel     = new QLabel("Value: ");
	penWidthLabel  = new QLabel("Pen width: ");
	clearButton    = new QPushButton("Clear");
	saveButton     = new QPushButton("Save");
	evaluateButton = new QPushButton("Evalulate");
	filenameLine   = new QLineEdit;
	resultLine     = new QLineEdit;
	valueLine      = new QLineEdit;
	paintarea      = new PaintArea;
	penWidthSlider = new QSlider;
	mainLayout     = new QVBoxLayout;
	winLayout      = new QHBoxLayout;
	labelLayout    = new QGridLayout;

	image->setMinimumSize(280, 280);
	image->setSizePolicy(QSizePolicy::Minimum, QSizePolicy::Preferred);

	penWidthSlider->setTickPosition(QSlider::TicksBelow);
	penWidthSlider->setOrientation(Qt::Horizontal);
	penWidthSlider->setRange(1, 30);
	penWidthLabel->setText("Pen width: 15");

	resultLine->setReadOnly(true);
	valueLine->setReadOnly(true);

	labelLayout->addWidget(filenameLabel, 1, 1);
	labelLayout->addWidget(resultLabel, 2, 1);
	labelLayout->addWidget(valueLabel, 3, 1);
	labelLayout->addWidget(clearButton, 4, 1);
	labelLayout->addWidget(saveButton, 5, 1);
	labelLayout->addWidget(evaluateButton, 5, 2);

	labelLayout->addWidget(filenameLine, 1, 2);
	labelLayout->addWidget(resultLine, 2, 2);
	labelLayout->addWidget(valueLine, 3, 2);

	labelLayout->addWidget(penWidthSlider, 6, 1);
	labelLayout->addWidget(penWidthLabel, 6, 2);

	winLayout->addLayout(labelLayout);
	winLayout->addWidget(image);
	winLayout->addWidget(paintarea);
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
	std::cout << buf << std::endl;
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
	/*
	if(!strcmp(dimension, "0"))
		resultLine->setText("No ball");
	else if(!strcmp(dimension, "1"))
		resultLine->setText("Ball exist!");
	else if(!strcmp(dimension, "2"))
		resultLine->setText("Middle");
	else if(!strcmp(dimension, "3"))
		resultLine->setText("Far");
	else
		resultLine->setText("Unknown");
	valueLine->setText(value);
	*/
}

void Interface::connection(void)
{
	QObject::connect(clearButton, SIGNAL(clicked()), this, SLOT(clearImage()));
	QObject::connect(saveButton, SIGNAL(clicked()), this, SLOT(saveImage()));
	QObject::connect(evaluateButton, SIGNAL(clicked()), this, SLOT(evaluateImage()));
	QObject::connect(penWidthSlider, SIGNAL(sliderReleased()), this, SLOT(penWidthChanged()));
}

void Interface::clearImage(void)
{
	paintarea->resetPixmapArea();
}

void Interface::saveImage(void)
{
	paintarea->savePixmapImage();
}

void Interface::evaluateImage(void)
{
	paintarea->savePixmapImage();
	QString filename = QString("out.png");
	loadImage(filename);
	
	/* save image filename to file */
	char buf[1024];
	callPython(filename.toStdString(), buf);
	char dimension[1024], value[1024];

	/* split result to dimension and value */
	std::cout << buf << std::endl;
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
}

void Interface::penWidthChanged(void)
{
	paintarea->setPenWidth(penWidthSlider->value());
	char buf[1024];
	sprintf(buf, "Pen width: %d", penWidthSlider->value());
	penWidthLabel->setText(buf);
}

