#include "MainWindow.h"
#include <QDebug>
#include <QDockWidget>
#include <QHBoxLayout>
#include <QLabel>
#include <QMessageBox>
#include <QStatusBar>
#include <QVBoxLayout>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), m_wsClient(nullptr), m_dispatcher(nullptr),
      m_scanCancelled(false) {
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
  setWindowTitle(tr("DWARF II Controller"));
  resize(1280, 720);

  // Central Widget
  QWidget *centralWidget = new QWidget(this);
  setCentralWidget(centralWidget);

  QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);

  QLabel *viewportLabel = new QLabel(tr("Live Stream Area"), centralWidget);
  viewportLabel->setAlignment(Qt::AlignCenter);
  QFont viewportFont = viewportLabel->font();
  viewportFont.setPointSize(24);
  viewportLabel->setFont(viewportFont);
  viewportLabel->setMinimumHeight(400);
  mainLayout->addWidget(viewportLabel);

  // Device List (Hidden by default or shown?)
  // Let's show it always for now, or maybe collapsible.
  // User wants to see found dwarfs.
  m_deviceList = new QListWidget(this);
  m_deviceList->setMaximumHeight(100);
  connect(m_deviceList, &QListWidget::itemClicked, this,
          &MainWindow::onDeviceSelected);

  // Grid Layout for Controls
  QGridLayout *gridLayout = new QGridLayout();
  gridLayout->setColumnStretch(1, 1); // Make input column stretch

  // Row 0: Scan
  QLabel *subnetLabel = new QLabel(tr("Scan Subnet:"), this);
  m_subnetInput = new QLineEdit(this);
  // Pre-fill with detected subnet
  QStringList subnets = m_finder->getLocalSubnets();
  if (!subnets.isEmpty()) {
    m_subnetInput->setText(subnets.first());
  } else {
    m_subnetInput->setText("192.168.88");
  }
  m_subnetInput->setPlaceholderText(tr("e.g. 192.168.1"));
  connect(m_subnetInput, &QLineEdit::textChanged, this,
          &MainWindow::onSubnetTextChanged);

  m_scanButton = new QPushButton(tr("Scan"), this);
  connect(m_scanButton, &QPushButton::clicked, this,
          &MainWindow::onScanClicked);

  m_cancelScanButton = new QPushButton(tr("Cancel"), this);
  m_cancelScanButton->setEnabled(false);
  connect(m_cancelScanButton, &QPushButton::clicked, this,
          &MainWindow::onCancelScanClicked);

  gridLayout->addWidget(subnetLabel, 0, 0);
  gridLayout->addWidget(m_subnetInput, 0, 1);
  gridLayout->addWidget(m_scanButton, 0, 2);
  gridLayout->addWidget(m_cancelScanButton, 0, 3);

  // Row 1: Connect
  QLabel *ipLabel = new QLabel(tr("DWARF II IP:"), this);
  m_ipInput = new QLineEdit(this);
  m_ipInput->setText("192.168.88.1");
  m_ipInput->setPlaceholderText(tr("Enter IP address"));

  m_connectButton = new QPushButton(tr("Connect"), this);
  connect(m_connectButton, &QPushButton::clicked, this,
          &MainWindow::onConnectClicked);

  m_cancelConnectButton = new QPushButton(tr("Cancel"), this);
  m_cancelConnectButton->setEnabled(false);
  connect(m_cancelConnectButton, &QPushButton::clicked, this,
          &MainWindow::onCancelConnectClicked);

  gridLayout->addWidget(ipLabel, 1, 0);
  gridLayout->addWidget(m_ipInput, 1, 1);
  gridLayout->addWidget(m_connectButton, 1, 2);
  gridLayout->addWidget(m_cancelConnectButton, 1, 3);

  // Status Label
  m_statusLabel = new QLabel(tr("Disconnected"), this);
  m_statusLabel->setStyleSheet("QLabel { color: #FF5555; font-weight: bold; }");
  m_statusLabel->setAlignment(Qt::AlignCenter);

  QWidget *systemMediaTab = new QWidget(this);
  QVBoxLayout *systemMediaLayout = new QVBoxLayout(systemMediaTab);
  systemMediaLayout->addLayout(gridLayout);
  systemMediaLayout->addWidget(m_statusLabel);
  systemMediaLayout->addWidget(m_deviceList);
  systemMediaTab->setLayout(systemMediaLayout);

  // Tab widget for modules
  m_tabWidget = new QTabWidget(this);

  QWidget *cameraTab = new QWidget(this);
  QVBoxLayout *cameraLayout = new QVBoxLayout(cameraTab);
  QLabel *cameraControlsLabel =
      new QLabel(tr("Camera controls (TODO)"), cameraTab);
  cameraControlsLabel->setAlignment(Qt::AlignCenter);
  cameraLayout->addWidget(cameraControlsLabel);
  cameraTab->setLayout(cameraLayout);

  QWidget *astroTab = new QWidget(this);
  QVBoxLayout *astroLayout = new QVBoxLayout(astroTab);
  QLabel *astroLabel =
      new QLabel(tr("Astro & Navigation (TODO)"), astroTab);
  astroLabel->setAlignment(Qt::AlignCenter);
  astroLayout->addWidget(astroLabel);
  astroTab->setLayout(astroLayout);

  QWidget *motorFocusTab = new QWidget(this);
  QVBoxLayout *motorFocusLayout = new QVBoxLayout(motorFocusTab);
  QLabel *motorFocusLabel =
      new QLabel(tr("Motor & Focus controls (TODO)"), motorFocusTab);
  motorFocusLabel->setAlignment(Qt::AlignCenter);
  motorFocusLayout->addWidget(motorFocusLabel);
  motorFocusTab->setLayout(motorFocusLayout);

  m_tabWidget->addTab(systemMediaTab, tr("System & Media"));
  m_tabWidget->addTab(motorFocusTab, tr("Motor & Focus"));
m_tabWidget->addTab(cameraTab, tr("Camera & Capture"));
  m_tabWidget->addTab(astroTab, tr("Astro & Navigation"));
  
  m_tabWidget->setTabPosition(QTabWidget::East);

  QDockWidget *controlDock = new QDockWidget(tr("Control Deck"), this);
  controlDock->setAllowedAreas(Qt::RightDockWidgetArea);
  controlDock->setFeatures(static_cast<QDockWidget::DockWidgetFeatures>(
      QDockWidget::DockWidgetClosable | QDockWidget::DockWidgetMovable |
      QDockWidget::DockWidgetFloatable));

  QWidget *dockContents = new QWidget(controlDock);
  QVBoxLayout *dockLayout = new QVBoxLayout(dockContents);
  dockLayout->addWidget(m_tabWidget);
  dockContents->setLayout(dockLayout);
  controlDock->setWidget(dockContents);
  addDockWidget(Qt::RightDockWidgetArea, controlDock);

  statusBar()->showMessage(tr("Ready"));
}

void MainWindow::onScanClicked() {
  QString subnet = m_subnetInput->text().trimmed();
  qDebug() << "Scan button clicked, subnet:" << subnet;
  m_scanCancelled = false;
  m_deviceList->clear();
  m_scanButton->setEnabled(false);
  m_cancelScanButton->setEnabled(true);
  m_statusLabel->setText(tr("Scanning %1.0/24...").arg(subnet));
  m_statusLabel->setStyleSheet("QLabel { color: #FFA500; font-weight: bold; }");
  m_finder->startScan(subnet);
}

void MainWindow::onCancelScanClicked() {
  m_finder->stopScan();
  m_scanCancelled = true;
  m_statusLabel->setText(tr("Scan Cancelled"));
  m_statusLabel->setStyleSheet("QLabel { color: #FF5555; font-weight: bold; }");
}

void MainWindow::onScanProgress(int percent) {
  QString subnet = m_subnetInput->text().trimmed();
  m_statusLabel->setText(
      tr("Scanning %1.0/24... %2%").arg(subnet).arg(percent));
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

  if (m_scanCancelled) {
    // Keep cancelled status
    qDebug() << "Scan was cancelled";
  } else if (m_deviceList->count() == 0) {
    m_statusLabel->setText(tr("No devices found"));
    m_statusLabel->setStyleSheet(
        "QLabel { color: #FF5555; font-weight: bold; }");
    qDebug() << "No devices found";
  } else {
    m_statusLabel->setText(
        tr("Found %1 devices").arg(m_deviceList->count()));
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
    QMessageBox::warning(this, tr("Error"),
                         tr("Please enter an IP address"));
    return;
  }

  if (m_wsClient && m_wsClient->isConnected()) {
    m_wsClient->disconnect();
    delete m_wsClient;
    m_wsClient = nullptr;
    m_connectButton->setText(tr("Connect"));
    m_cancelConnectButton->setEnabled(false);
    m_statusLabel->setText(tr("Disconnected"));
    m_statusLabel->setStyleSheet(
        "QLabel { color: #FF5555; font-weight: bold; }");
    statusBar()->showMessage(tr("Disconnected"));
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
    m_statusLabel->setText(tr("Connecting..."));
    m_statusLabel->setStyleSheet(
        "QLabel { color: #FFA500; font-weight: bold; }");
    statusBar()->showMessage(tr("Connecting to %1").arg(ip));
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
  m_connectButton->setText(tr("Connect"));
  m_cancelConnectButton->setEnabled(false);
  m_statusLabel->setText(tr("Cancelled"));
  m_statusLabel->setStyleSheet("QLabel { color: #FF5555; font-weight: bold; }");
  statusBar()->showMessage(tr("Connection cancelled"));
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
  m_connectButton->setText(tr("Disconnect"));
  m_cancelConnectButton->setEnabled(
      false); // Can't cancel if already connected, use Disconnect
  m_statusLabel->setText(tr("Connected"));
  m_statusLabel->setStyleSheet("QLabel { color: #55FF55; font-weight: bold; }");
  statusBar()->showMessage(tr("Connected to DWARF II"));
}

void MainWindow::onWebSocketDisconnected() {
  m_connectButton->setEnabled(true);
  m_connectButton->setText(tr("Connect"));
  m_cancelConnectButton->setEnabled(false);
  m_statusLabel->setText(tr("Disconnected"));
  m_statusLabel->setStyleSheet("QLabel { color: #FF5555; font-weight: bold; }");
  statusBar()->showMessage(tr("Disconnected from DWARF II"));
}

void MainWindow::onWebSocketError(const QString &error) {
  QMessageBox::critical(this, tr("Connection Error"), error);
  m_connectButton->setEnabled(true);
  m_connectButton->setText(tr("Connect"));
  m_cancelConnectButton->setEnabled(false);
  m_statusLabel->setText(tr("Error"));
  m_statusLabel->setStyleSheet("QLabel { color: #FF0000; font-weight: bold; }");
  statusBar()->showMessage(tr("Error: %1").arg(error));
}
