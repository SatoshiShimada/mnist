
#include <QtGui>
#include "interface.h"

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>

int main(int argc, char **argv)
{
	QApplication app(argc, argv);
	Interface *interface = new Interface;
	/* set window size */
	interface->resize(600, 350);

	interface->show();
	return app.exec();
}

void callPython(std::string filename, char *ret)
{
	int len = filename.length();
	char *name = new char[len+1];
	memcpy(name, filename.c_str(), len+1);

	FILE *fp;
	char command[1024];
	char buf[1024];

	/* execute 'src/ball.py' with argument that is filename of image */
	strcpy(command, "src/ball.py ");
	strcat(command, name);
	fp = popen(command, "r");
	/* get string of output of 'src/ball.py' */
	fgets(buf, sizeof(buf), fp);
	pclose(fp);

	strcpy(ret, buf);
	return;
}

