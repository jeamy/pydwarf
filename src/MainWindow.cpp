#include "MainWindow.h"
#include <QDebug>
#include <QDockWidget>
#include <QHBoxLayout>
#include <QLabel>
#include <QMessageBox>
#include <QStatusBar>
#include <QStyle>
#include <QVBoxLayout>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), m_wsClient(nullptr), m_dispatcher(nullptr),
      m_scanCancelled(false) {
  m_mainStreamView = nullptr;
  m_pipStreamView = nullptr;
  m_teleButton = nullptr;
  m_wideButton = nullptr;
  m_mainStream = CameraStream::Tele;
  m_pipStream = CameraStream::Wide;
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

void MainWindow::updateStatusStyle(const char *statusKey) {
  if (!m_statusLabel)
    return;
  m_statusLabel->setProperty("status", statusKey);
  m_statusLabel->style()->unpolish(m_statusLabel);
  m_statusLabel->style()->polish(m_statusLabel);
  m_statusLabel->update();
}

void MainWindow::updateCameraStreamViews() {
  if (!m_mainStreamView || !m_pipStreamView)
    return;

  const bool mainIsTele = (m_mainStream == CameraStream::Tele);

  if (mainIsTele) {
    m_mainStreamView->setText(tr("Live Stream (TELE)"));
    m_pipStreamView->setText(tr("WIDE"));
  } else {
    m_mainStreamView->setText(tr("Live Stream (WIDE)"));
    m_pipStreamView->setText(tr("TELE"));
  }

  if (m_teleButton && m_wideButton) {
    m_teleButton->setChecked(mainIsTele);
    m_wideButton->setChecked(!mainIsTele);
  }
}

void MainWindow::setupUi() {
  setWindowTitle(tr("DWARF II Controller"));
  resize(1280, 720);

  // Central Widget
  QWidget *centralWidget = new QWidget(this);
  setCentralWidget(centralWidget);

  QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);

  QWidget *viewportWidget = new QWidget(centralWidget);
  QGridLayout *viewportLayout = new QGridLayout(viewportWidget);
  viewportLayout->setContentsMargins(0, 0, 0, 0);

  m_mainStreamView = new QLabel(centralWidget);
  m_mainStreamView->setObjectName("mainStreamView");
  m_mainStreamView->setAlignment(Qt::AlignCenter);
  m_mainStreamView->setMinimumHeight(400);

  m_pipStreamView = new ClickableLabel(centralWidget);
  m_pipStreamView->setObjectName("pipStreamView");
  m_pipStreamView->setFixedSize(220, 124);

  viewportLayout->addWidget(m_mainStreamView, 0, 0);
  viewportLayout->addWidget(m_pipStreamView, 0, 0,
                            Qt::AlignTop | Qt::AlignRight);
  viewportWidget->setLayout(viewportLayout);
  mainLayout->addWidget(viewportWidget);

  connect(m_pipStreamView, &ClickableLabel::clicked, this,
          &MainWindow::onPipStreamClicked);

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
  m_statusLabel->setObjectName("statusLabel");
  m_statusLabel->setAlignment(Qt::AlignCenter);
  updateStatusStyle("disconnected");

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

  QHBoxLayout *sourceLayout = new QHBoxLayout();
  QLabel *sourceLabel = new QLabel(tr("Stream source:"), cameraTab);
  m_teleButton = new QPushButton(tr("TELE"), cameraTab);
  m_wideButton = new QPushButton(tr("WIDE"), cameraTab);
  m_teleButton->setCheckable(true);
  m_wideButton->setCheckable(true);
  m_teleButton->setChecked(true);
  sourceLayout->addWidget(sourceLabel);
  sourceLayout->addWidget(m_teleButton);
  sourceLayout->addWidget(m_wideButton);
  sourceLayout->addStretch();
  connect(m_teleButton, &QPushButton::clicked, this,
          &MainWindow::onCameraSourceTele);
  connect(m_wideButton, &QPushButton::clicked, this,
          &MainWindow::onCameraSourceWide);

  QHBoxLayout *captureLayout = new QHBoxLayout();
  m_photoButton = new QPushButton(tr("PHOTO"), cameraTab);
  m_recButton = new QPushButton(tr("REC"), cameraTab);
  m_photoButton->setMinimumHeight(40);
  m_recButton->setMinimumHeight(40);
  captureLayout->addWidget(m_photoButton);
  captureLayout->addWidget(m_recButton);
  connect(m_photoButton, &QPushButton::clicked, this,
          &MainWindow::onCameraPhotoClicked);
  connect(m_recButton, &QPushButton::clicked, this,
          &MainWindow::onCameraRecClicked);

  QGroupBox *exposureGroup = new QGroupBox(tr("Exposure"), cameraTab);
  QGridLayout *exposureLayout = new QGridLayout(exposureGroup);
  QLabel *modeLabel = new QLabel(tr("Mode:"), exposureGroup);
  m_exposureModeCombo = new QComboBox(exposureGroup);
  m_exposureModeCombo->addItem(tr("Auto"));
  m_exposureModeCombo->addItem(tr("Manual"));
  connect(m_exposureModeCombo, QOverload<int>::of(&QComboBox::currentIndexChanged),
          this, &MainWindow::onExposureModeChanged);

  QLabel *shutterLabel = new QLabel(tr("Shutter"), exposureGroup);
  m_shutterSlider = new QSlider(Qt::Horizontal, exposureGroup);
  m_shutterSlider->setRange(1, 100);
  connect(m_shutterSlider, &QSlider::valueChanged, this,
          &MainWindow::onShutterSliderChanged);

  QLabel *gainLabel = new QLabel(tr("Gain"), exposureGroup);
  m_gainSlider = new QSlider(Qt::Horizontal, exposureGroup);
  m_gainSlider->setRange(0, 100);
  connect(m_gainSlider, &QSlider::valueChanged, this,
          &MainWindow::onGainSliderChanged);

  exposureLayout->addWidget(modeLabel, 0, 0);
  exposureLayout->addWidget(m_exposureModeCombo, 0, 1);
  exposureLayout->addWidget(shutterLabel, 1, 0);
  exposureLayout->addWidget(m_shutterSlider, 1, 1);
  exposureLayout->addWidget(gainLabel, 2, 0);
  exposureLayout->addWidget(m_gainSlider, 2, 1);
  exposureGroup->setLayout(exposureLayout);

  QGroupBox *imageGroup = new QGroupBox(tr("Image parameters"), cameraTab);
  QGridLayout *imageLayout = new QGridLayout(imageGroup);

  m_irCutCheckBox = new QCheckBox(tr("IR-Cut"), imageGroup);
  connect(m_irCutCheckBox, &QCheckBox::toggled, this,
          &MainWindow::onIrCutToggled);

  QLabel *binningLabel = new QLabel(tr("Binning"), imageGroup);
  m_binningCombo = new QComboBox(imageGroup);
  m_binningCombo->addItem(tr("4K"));
  m_binningCombo->addItem(tr("2K"));
  connect(m_binningCombo, QOverload<int>::of(&QComboBox::currentIndexChanged),
          this, &MainWindow::onBinningChanged);

  QLabel *contrastLabel = new QLabel(tr("Contrast"), imageGroup);
  m_contrastSlider = new QSlider(Qt::Horizontal, imageGroup);
  m_contrastSlider->setRange(0, 100);
  connect(m_contrastSlider, &QSlider::valueChanged, this,
          &MainWindow::onContrastSliderChanged);

  QLabel *saturationLabel = new QLabel(tr("Saturation"), imageGroup);
  m_saturationSlider = new QSlider(Qt::Horizontal, imageGroup);
  m_saturationSlider->setRange(0, 100);
  connect(m_saturationSlider, &QSlider::valueChanged, this,
          &MainWindow::onSaturationSliderChanged);

  QLabel *sharpnessLabel = new QLabel(tr("Sharpness"), imageGroup);
  m_sharpnessSlider = new QSlider(Qt::Horizontal, imageGroup);
  m_sharpnessSlider->setRange(0, 100);
  connect(m_sharpnessSlider, &QSlider::valueChanged, this,
          &MainWindow::onSharpnessSliderChanged);

  QLabel *hueLabel = new QLabel(tr("Hue"), imageGroup);
  m_hueSlider = new QSlider(Qt::Horizontal, imageGroup);
  m_hueSlider->setRange(0, 100);
  connect(m_hueSlider, &QSlider::valueChanged, this,
          &MainWindow::onHueSliderChanged);

  imageLayout->addWidget(m_irCutCheckBox, 0, 0, 1, 2);
  imageLayout->addWidget(binningLabel, 1, 0);
  imageLayout->addWidget(m_binningCombo, 1, 1);
  imageLayout->addWidget(contrastLabel, 2, 0);
  imageLayout->addWidget(m_contrastSlider, 2, 1);
  imageLayout->addWidget(saturationLabel, 3, 0);
  imageLayout->addWidget(m_saturationSlider, 3, 1);
  imageLayout->addWidget(sharpnessLabel, 4, 0);
  imageLayout->addWidget(m_sharpnessSlider, 4, 1);
  imageLayout->addWidget(hueLabel, 5, 0);
  imageLayout->addWidget(m_hueSlider, 5, 1);
  imageGroup->setLayout(imageLayout);

  cameraLayout->addLayout(sourceLayout);
  cameraLayout->addLayout(captureLayout);
  cameraLayout->addWidget(exposureGroup);
  cameraLayout->addWidget(imageGroup);
  cameraLayout->addStretch();
  cameraTab->setLayout(cameraLayout);

  updateCameraStreamViews();

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
  updateStatusStyle("scanning");
  m_finder->startScan(subnet);
}

void MainWindow::onCancelScanClicked() {
  m_finder->stopScan();
  m_scanCancelled = true;
  m_statusLabel->setText(tr("Scan Cancelled"));
  updateStatusStyle("cancelled");
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
    updateStatusStyle("noDevices");
    qDebug() << "No devices found";
  } else {
    m_statusLabel->setText(
        tr("Found %1 devices").arg(m_deviceList->count()));
    updateStatusStyle("ok");
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
    updateStatusStyle("disconnected");
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
    updateStatusStyle("connecting");
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
  updateStatusStyle("cancelled");
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
  updateStatusStyle("ok");
  statusBar()->showMessage(tr("Connected to DWARF II"));
}

void MainWindow::onWebSocketDisconnected() {
  m_connectButton->setEnabled(true);
  m_connectButton->setText(tr("Connect"));
  m_cancelConnectButton->setEnabled(false);
  m_statusLabel->setText(tr("Disconnected"));
  updateStatusStyle("disconnected");
  statusBar()->showMessage(tr("Disconnected from DWARF II"));
}

void MainWindow::onWebSocketError(const QString &error) {
  QMessageBox::critical(this, tr("Connection Error"), error);
  m_connectButton->setEnabled(true);
  m_connectButton->setText(tr("Connect"));
  m_cancelConnectButton->setEnabled(false);
  m_statusLabel->setText(tr("Error"));
  updateStatusStyle("error");
  statusBar()->showMessage(tr("Error: %1").arg(error));
}

void MainWindow::onCameraSourceTele() {
  m_mainStream = CameraStream::Tele;
  m_pipStream = CameraStream::Wide;
  updateCameraStreamViews();
}

void MainWindow::onCameraSourceWide() {
  m_mainStream = CameraStream::Wide;
  m_pipStream = CameraStream::Tele;
  updateCameraStreamViews();
}

void MainWindow::onCameraPhotoClicked() {
  qDebug() << "Camera PHOTO triggered";
}

void MainWindow::onCameraRecClicked() {
  qDebug() << "Camera REC triggered";
}

void MainWindow::onExposureModeChanged(int index) {
  qDebug() << "Exposure mode changed to" << index;
}

void MainWindow::onShutterSliderChanged(int value) {
  qDebug() << "Shutter slider changed to" << value;
}

void MainWindow::onGainSliderChanged(int value) {
  qDebug() << "Gain slider changed to" << value;
}

void MainWindow::onIrCutToggled(bool checked) {
  qDebug() << "IR-Cut toggled" << checked;
}

void MainWindow::onBinningChanged(int index) {
  qDebug() << "Binning changed to" << index;
}

void MainWindow::onContrastSliderChanged(int value) {
  qDebug() << "Contrast slider changed to" << value;
}

void MainWindow::onSaturationSliderChanged(int value) {
  qDebug() << "Saturation slider changed to" << value;
}

void MainWindow::onSharpnessSliderChanged(int value) {
  qDebug() << "Sharpness slider changed to" << value;
}

void MainWindow::onHueSliderChanged(int value) {
  qDebug() << "Hue slider changed to" << value;
}

void MainWindow::onPipStreamClicked() {
  std::swap(m_mainStream, m_pipStream);
  updateCameraStreamViews();
}
