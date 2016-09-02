#
# define make variables
#
JCC = javac
JCCFLAGS = -g -Xlint:all -cp .:./src/luha/wallhavendownloader
JCCDIR = -d ./bin/
JVM = java
JVMFLAGS =
JDOC = javadoc
JDOCFLAGS = -version -author
JDOCDIR = -d ./doc/


#
# for make classes
#
CLASSES = \
	WallhavenDownloader.class

#
# Main
#
MAIN = WallhavenDownloader

default : $(CLASSES)

WallhavenDownloader.class :
	javac -d ./bin/ ./src/luha/wallhavendownloader/WallhavenDownloader.java

run : $(CLASSES)
	java -cp .:./bin/ luha.wallhavendownloader.WallhavenDownloader

doc : $(CLASSES)
	javadoc -version -author -d ./doc/

clean :
	rm -rf ./bin/*
