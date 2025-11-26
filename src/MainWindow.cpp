#include "MainWindow.h"
#include <QDebug>
#include <QHBoxLayout>
#include <QLabel>
#include <QMessageBox>
#include <QStatusBar>
#include <QVBoxLayout>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), m_wsClient(nullptr), m_dispatcher(nullptr) {
  m_finder = new DwarfFinder(this);
  connect(m_finder, &DwarfFinder::deviceFound, this,
          &MainWindow::onDeviceFound);
  connect(m_finder, &DwarfFinder::scanFinished, this,
          &MainWindow::onScanFinished);
  connect(m_finder, &DwarfFinder::scanProgress, this,
          &MainWindow::onScanProgress);

  m_dispatcher = new DwarfMessageDispatcher(this);

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

  // Grid Layout for Controls
  QGridLayout *gridLayout = new QGridLayout();
  gridLayout->setColumnStretch(1, 1); // Make input column stretch

  // Row 0: Scan
  QLabel *subnetLabel = new QLabel("Scan Subnet:", this);
  m_subnetInput = new QLineEdit(this);
  // Pre-fill with detected subnet
  QStringList subnets = m_finder->getLocalSubnets();
  if (!subnets.isEmpty()) {
    m_subnetInput->setText(subnets.first());
  } else {
    m_subnetInput->setText("192.168.88");
  }
  m_subnetInput->setPlaceholderText("e.g. 192.168.1");
  connect(m_subnetInput, &QLineEdit::textChanged, this,
          &MainWindow::onSubnetTextChanged);

  m_scanButton = new QPushButton("Scan", this);
  connect(m_scanButton, &QPushButton::clicked, this,
          &MainWindow::onScanClicked);

  m_cancelScanButton = new QPushButton("Cancel", this);
  m_cancelScanButton->setEnabled(false);
  connect(m_cancelScanButton, &QPushButton::clicked, this,
          &MainWindow::onCancelScanClicked);

  gridLayout->addWidget(subnetLabel, 0, 0);
  gridLayout->addWidget(m_subnetInput, 0, 1);
  gridLayout->addWidget(m_scanButton, 0, 2);
  gridLayout->addWidget(m_cancelScanButton, 0, 3);

  // Row 1: Connect
  QLabel *ipLabel = new QLabel("DWARF II IP:", this);
  m_ipInput = new QLineEdit(this);
  m_ipInput->setText("192.168.88.1");
  m_ipInput->setPlaceholderText("Enter IP address");

  m_connectButton = new QPushButton("Connect", this);
  connect(m_connectButton, &QPushButton::clicked, this,
          &MainWindow::onConnectClicked);

  m_cancelConnectButton = new QPushButton("Cancel", this);
  m_cancelConnectButton->setEnabled(false);
  connect(m_cancelConnectButton, &QPushButton::clicked, this,
          &MainWindow::onCancelConnectClicked);

  gridLayout->addWidget(ipLabel, 1, 0);
  gridLayout->addWidget(m_ipInput, 1, 1);
  gridLayout->addWidget(m_connectButton, 1, 2);
  gridLayout->addWidget(m_cancelConnectButton, 1, 3);

  // Status Label
  m_statusLabel = new QLabel("Disconnected", this);
  m_statusLabel->setStyleSheet("QLabel { color: #FF5555; font-weight: bold; }");
  m_statusLabel->setAlignment(Qt::AlignCenter);

  mainLayout->addLayout(gridLayout);
  mainLayout->addWidget(m_statusLabel);

  // Device List (Hidden by default or shown?)
  // Let's show it always for now, or maybe collapsible.
  // User wants to see found dwarfs.
  m_deviceList = new QListWidget(this);
  m_deviceList->setMaximumHeight(100);
  connect(m_deviceList, &QListWidget::itemClicked, this,
          &MainWindow::onDeviceSelected);
  mainLayout->addWidget(m_deviceList);

  // Tab widget for modules
  m_tabWidget = new QTabWidget(this);

  QWidget *cameraTab = new QWidget(this);
  QVBoxLayout *cameraLayout = new QVBoxLayout(cameraTab);
  QLabel *placeholderLabel = new QLabel("Live Stream Area", cameraTab);
  placeholderLabel->setAlignment(Qt::AlignCenter);
  QFont font = placeholderLabel->font();
  font.setPointSize(24);
  placeholderLabel->setFont(font);
  placeholderLabel->setMinimumHeight(400);
  cameraLayout->addWidget(placeholderLabel);
  cameraTab->setLayout(cameraLayout);

  QWidget *motorAstroTab = new QWidget(this);
  QVBoxLayout *motorAstroLayout = new QVBoxLayout(motorAstroTab);
  QLabel *motorAstroLabel = new QLabel("Motor & Astro Controls (TODO)", motorAstroTab);
  motorAstroLabel->setAlignment(Qt::AlignCenter);
  motorAstroLayout->addWidget(motorAstroLabel);
  motorAstroTab->setLayout(motorAstroLayout);

  QWidget *mediaTab = new QWidget(this);
  QVBoxLayout *mediaLayout = new QVBoxLayout(mediaTab);
  QLabel *mediaLabel = new QLabel("Media Panel (TODO)", mediaTab);
  mediaLabel->setAlignment(Qt::AlignCenter);
  mediaLayout->addWidget(mediaLabel);
  mediaTab->setLayout(mediaLayout);

  m_tabWidget->addTab(cameraTab, "Camera");
  m_tabWidget->addTab(motorAstroTab, "Motor & Astro");
  m_tabWidget->addTab(mediaTab, "Media");

  mainLayout->addWidget(m_tabWidget);

  statusBar()->showMessage("Ready");
}

void MainWindow::onScanClicked() {
  QString subnet = m_subnetInput->text().trimmed();
  qDebug() << "Scan button clicked, subnet:" << subnet;
  m_deviceList->clear();
  m_scanButton->setEnabled(false);
  m_cancelScanButton->setEnabled(true);
  m_statusLabel->setText(QString("Scanning %1.0/24...").arg(subnet));
  m_statusLabel->setStyleSheet("QLabel { color: #FFA500; font-weight: bold; }");
  m_finder->startScan(subnet);
}

void MainWindow::onCancelScanClicked() {
  m_finder->stopScan();
  m_statusLabel->setText("Scan Cancelled");
  m_statusLabel->setStyleSheet("QLabel { color: #FF5555; font-weight: bold; }");
}

void MainWindow::onScanProgress(int percent) {
  QString subnet = m_subnetInput->text().trimmed();
  m_statusLabel->setText(
      QString("Scanning %1.0/24... %2%").arg(subnet).arg(percent));
}

void MainWindow::onDeviceFound(const DwarfDeviceInfo &info) {
  QString label = QString("%1 - %2").arg(info.ip).arg(info.name);
  QListWidgetItem *item = new QListWidgetItem(label);
  item->setData(Qt::UserRole, info.ip);
  m_deviceList->addItem(item);
}

void MainWindow::onScanFinished() {
  qDebug() << "Scan finished, re-enabling scan button";
  m_scanButton->setEnabled(true);
  m_cancelScanButton->setEnabled(false);

  if (m_statusLabel->text() == "Scan Cancelled") {
    // Keep cancelled status
    qDebug() << "Scan was cancelled";
  } else if (m_deviceList->count() == 0) {
    m_statusLabel->setText("No devices found");
    m_statusLabel->setStyleSheet(
        "QLabel { color: #FF5555; font-weight: bold; }");
    qDebug() << "No devices found";
  } else {
    m_statusLabel->setText(
        QString("Found %1 devices").arg(m_deviceList->count()));
    m_statusLabel->setStyleSheet(
        "QLabel { color: #55FF55; font-weight: bold; }");
    qDebug() << "Found" << m_deviceList->count() << "devices";
  }
}

void MainWindow::onDeviceSelected(QListWidgetItem *item) {
  QString ip = item->data(Qt::UserRole).toString();
  m_ipInput->setText(ip);
  onConnectClicked();
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
    m_cancelConnectButton->setEnabled(false);
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

    if (!m_dispatcher) {
      m_dispatcher = new DwarfMessageDispatcher(this);
    }

    connect(m_wsClient, &DwarfWebSocketClient::messageReceived, m_dispatcher,
            &DwarfMessageDispatcher::dispatch);

    m_wsClient->connectToDevice();
    m_connectButton->setEnabled(false); // Disable connect while connecting
    m_cancelConnectButton->setEnabled(true);
    m_statusLabel->setText("Connecting...");
    m_statusLabel->setStyleSheet(
        "QLabel { color: #FFA500; font-weight: bold; }");
    statusBar()->showMessage("Connecting to " + ip);
  }
}

void MainWindow::onCancelConnectClicked() {
  if (m_wsClient) {
    // If we are connecting, this should abort it.
    // DwarfWebSocketClient might not have an abort method exposed easily,
    // but deleting it or calling disconnect should work.
    m_wsClient->disconnect();
    delete m_wsClient;
    m_wsClient = nullptr;
  }

  m_connectButton->setEnabled(true);
  m_connectButton->setText("Connect");
  m_cancelConnectButton->setEnabled(false);
  m_statusLabel->setText("Cancelled");
  m_statusLabel->setStyleSheet("QLabel { color: #FF5555; font-weight: bold; }");
  statusBar()->showMessage("Connection cancelled");
}

void MainWindow::onSubnetTextChanged(const QString &text) {
  // If the subnet looks valid (e.g. 3 parts), update the IP input
  QStringList parts = text.split('.');
  if (parts.size() >= 3) {
    QString ip =
        QString("%1.%2.%3.1").arg(parts[0]).arg(parts[1]).arg(parts[2]);
    m_ipInput->setText(ip);
  }
}

void MainWindow::onWebSocketConnected() {
  m_connectButton->setEnabled(true);
  m_connectButton->setText("Disconnect");
  m_cancelConnectButton->setEnabled(
      false); // Can't cancel if already connected, use Disconnect
  m_statusLabel->setText("Connected");
  m_statusLabel->setStyleSheet("QLabel { color: #55FF55; font-weight: bold; }");
  statusBar()->showMessage("Connected to DWARF II");
}

void MainWindow::onWebSocketDisconnected() {
  m_connectButton->setEnabled(true);
  m_connectButton->setText("Connect");
  m_cancelConnectButton->setEnabled(false);
  m_statusLabel->setText("Disconnected");
  m_statusLabel->setStyleSheet("QLabel { color: #FF5555; font-weight: bold; }");
  statusBar()->showMessage("Disconnected from DWARF II");
}

void MainWindow::onWebSocketError(const QString &error) {
  QMessageBox::critical(this, "Connection Error", error);
  m_connectButton->setEnabled(true);
  m_connectButton->setText("Connect");
  m_cancelConnectButton->setEnabled(false);
  m_statusLabel->setText("Error");
  m_statusLabel->setStyleSheet("QLabel { color: #FF0000; font-weight: bold; }");
  statusBar()->showMessage("Error: " + error);
}
