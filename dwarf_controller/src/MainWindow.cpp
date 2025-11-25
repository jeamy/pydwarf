#include "MainWindow.h"
#include <QHBoxLayout>
#include <QLabel>
#include <QMessageBox>
#include <QStatusBar>
#include <QVBoxLayout>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), m_wsClient(nullptr) {
  setupUi();
}

MainWindow::~MainWindow() {
  if (m_wsClient) {
    m_wsClient->disconnect();
    delete m_wsClient;
  }
}

void MainWindow::setupUi() {
  setWindowTitle("DWARF II Controller");
  resize(1280, 720);

  // Central Widget
  QWidget *centralWidget = new QWidget(this);
  setCentralWidget(centralWidget);

  QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);

  // Connection Panel
  QHBoxLayout *connectionLayout = new QHBoxLayout();

  QLabel *ipLabel = new QLabel("DWARF II IP:", this);
  m_ipInput = new QLineEdit(this);
  m_ipInput->setText("192.168.88.1");
  m_ipInput->setPlaceholderText("Enter IP address");

  m_connectButton = new QPushButton("Connect", this);
  connect(m_connectButton, &QPushButton::clicked, this,
          &MainWindow::onConnectClicked);

  m_statusLabel = new QLabel("Disconnected", this);
  m_statusLabel->setStyleSheet("QLabel { color: #FF5555; font-weight: bold; }");

  connectionLayout->addWidget(ipLabel);
  connectionLayout->addWidget(m_ipInput);
  connectionLayout->addWidget(m_connectButton);
  connectionLayout->addWidget(m_statusLabel);
  connectionLayout->addStretch();

  mainLayout->addLayout(connectionLayout);

  // Placeholder
  QLabel *placeholderLabel = new QLabel("Live Stream Area", this);
  placeholderLabel->setAlignment(Qt::AlignCenter);
  QFont font = placeholderLabel->font();
  font.setPointSize(24);
  placeholderLabel->setFont(font);
  placeholderLabel->setMinimumHeight(500);

  mainLayout->addWidget(placeholderLabel);

  statusBar()->showMessage("Ready");
}

void MainWindow::onConnectClicked() {
  QString ip = m_ipInput->text().trimmed();

  if (ip.isEmpty()) {
    QMessageBox::warning(this, "Error", "Please enter an IP address");
    return;
  }

  if (m_wsClient && m_wsClient->isConnected()) {
    m_wsClient->disconnect();
    delete m_wsClient;
    m_wsClient = nullptr;
    m_connectButton->setText("Connect");
    m_statusLabel->setText("Disconnected");
    m_statusLabel->setStyleSheet(
        "QLabel { color: #FF5555; font-weight: bold; }");
    statusBar()->showMessage("Disconnected");
  } else {
    m_wsClient = new DwarfWebSocketClient(ip, this);

    connect(m_wsClient, &DwarfWebSocketClient::connected, this,
            &MainWindow::onWebSocketConnected);
    connect(m_wsClient, &DwarfWebSocketClient::disconnected, this,
            &MainWindow::onWebSocketDisconnected);
    connect(m_wsClient, &DwarfWebSocketClient::errorOccurred, this,
            &MainWindow::onWebSocketError);

    m_wsClient->connectToDevice();
    m_statusLabel->setText("Connecting...");
    m_statusLabel->setStyleSheet(
        "QLabel { color: #FFA500; font-weight: bold; }");
    statusBar()->showMessage("Connecting to " + ip);
  }
}

void MainWindow::onWebSocketConnected() {
  m_connectButton->setText("Disconnect");
  m_statusLabel->setText("Connected");
  m_statusLabel->setStyleSheet("QLabel { color: #55FF55; font-weight: bold; }");
  statusBar()->showMessage("Connected to DWARF II");
}

void MainWindow::onWebSocketDisconnected() {
  m_connectButton->setText("Connect");
  m_statusLabel->setText("Disconnected");
  m_statusLabel->setStyleSheet("QLabel { color: #FF5555; font-weight: bold; }");
  statusBar()->showMessage("Disconnected from DWARF II");
}

void MainWindow::onWebSocketError(const QString &error) {
  QMessageBox::critical(this, "Connection Error", error);
  m_statusLabel->setText("Error");
  m_statusLabel->setStyleSheet("QLabel { color: #FF0000; font-weight: bold; }");
  statusBar()->showMessage("Error: " + error);
}
