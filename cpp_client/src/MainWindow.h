#pragma once

#include "net/DwarfWebSocketClient.h"
#include <QLabel>
#include <QLineEdit>
#include <QMainWindow>
#include <QPushButton>

class MainWindow : public QMainWindow {
  Q_OBJECT

public:
  MainWindow(QWidget *parent = nullptr);
  ~MainWindow();

private slots:
  void onConnectClicked();
  void onWebSocketConnected();
  void onWebSocketDisconnected();
  void onWebSocketError(const QString &error);

private:
  void setupUi();

  QLineEdit *m_ipInput;
  QPushButton *m_connectButton;
  QLabel *m_statusLabel;
  DwarfWebSocketClient *m_wsClient;
};
