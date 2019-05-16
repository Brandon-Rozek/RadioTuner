#ifndef CLIENT_H
#define CLIENT_H

#include <QObject>
#include <QTcpSocket>

class Client : public QObject {
    Q_OBJECT
public:
    explicit Client(QObject *parent = nullptr);
    ~Client();
    void send(QString data);
    QString recv(void);
    Q_INVOKABLE void setFrequency(double freq);
    Q_INVOKABLE double getFrequency(void);
    Q_INVOKABLE void connect(QString host, int port);
    Q_INVOKABLE bool isConnected();
private:
    QTcpSocket *socket = nullptr;
    bool connected = false;
};

#endif // CLIENT_H
