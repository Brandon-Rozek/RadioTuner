#include "client.h"
#include <QString>
#include <QTcpSocket>
#include <iostream>


Client::Client(QObject *parent) : QObject(parent) {
    socket = new QTcpSocket(nullptr);

}

Client::~Client() {
     socket->close();
}

void Client::connect(QString hostname, int port) {
    socket->connectToHost(hostname, port);
    socket->waitForConnected();
    std::cout << "Connected" << std::endl;
    this->connected = true;
}

bool Client::isConnected() {
    return this->connected;
}

void Client::send(QString data) {
    std::cout << "SENDING MESSAGE: \"" << data.toStdString() << "\"" << std::endl;
    QByteArray dataStream = data.toUtf8();
    socket->write(dataStream);
}

QString Client::recv(void) {
    socket->waitForReadyRead(1000);
    QByteArray data = socket->readAll();
    QString msg = QString(data);
    std::cout << "RECEIVED MESSAGE SO FAR: \"" << msg.toStdString() << "\"" << std::endl;
    return msg;
}

void Client::setFrequency(double freq) {
    QString msg = QString(":FREQ=");
    msg.push_back(QString::number(freq));
    msg.push_back(";");
    this->send(msg);
}

double Client::getFrequency(void) {
    this->send(QString("?FREQ;"));
    return this->recv().toDouble();
}
