TEMPLATE = app
TARGET = RadioTuner
INCLUDEPATH += .

# The following define makes your compiler warn you if you use any
# feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# Input
HEADERS += client.h
SOURCES += client.cpp main.cpp
RESOURCES += qml.qrc

QT += network qml quick 
