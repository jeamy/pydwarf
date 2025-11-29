#include "MainWindow.h"
#include "net/DwarfCameraController.h"
#include "qnamespace.h"
#include <QDebug>
#include <QDockWidget>
#include <QHBoxLayout>
#include <QLabel>
#include <QMessageBox>
#include <QStatusBar>
#include <QStyle>
#include <QTimer>
#include <QVBoxLayout>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), m_wsClient(nullptr), m_dispatcher(nullptr),
      m_scanCancelled(false), m_cameraController(nullptr), m_isRecording(false),
      m_mainVideoWidget(nullptr), m_pipVideoWidget(nullptr),
      m_telePlayer(nullptr), m_widePlayer(nullptr) {
  m_mainStreamView = nullptr;
  m_pipStreamView = nullptr;
  m_teleButton = nullptr;
  m_wideButton = nullptr;
  m_mainStream = CameraStream::Tele;
  m_pipStream = CameraStream::Wide;
  m_cameraController = new DwarfCameraController(this);
  m_telePlayer = new QMediaPlayer(this);
  m_widePlayer = new QMediaPlayer(this);
  m_finder = new DwarfFinder(this);
  connect(m_finder, &DwarfFinder::deviceFound, this,
          &MainWindow::onDeviceFound);
  connect(m_finder, &DwarfFinder::scanFinished, this,
          &MainWindow::onScanFinished);
  connect(m_finder, &DwarfFinder::scanProgress, this,
          &MainWindow::onScanProgress);

  m_dispatcher = new DwarfMessageDispatcher(this);
  connect(m_dispatcher, &DwarfMessageDispatcher::cameraTeleMessage, this,
          &MainWindow::onCameraTeleMessage);
  connect(m_dispatcher, &DwarfMessageDispatcher::cameraWideMessage, this,
          &MainWindow::onCameraWideMessage);

  setupUi();
}

MainWindow::~MainWindow() {
  if (m_wsClient) {
    m_wsClient->disconnect();
    delete m_wsClient;
  }

  stopStreaming();
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
    m_streamNameOverlay->setText(tr("Live Stream (TELE)"));
    // m_pipStreamView->setText(tr("WIDE")); // No text on PiP, video covers it
  } else {
    m_streamNameOverlay->setText(tr("Live Stream (WIDE)"));
    // m_pipStreamView->setText(tr("TELE"));
  }

  if (m_teleButton && m_wideButton) {
    m_teleButton->setChecked(mainIsTele);
    m_wideButton->setChecked(!mainIsTele);
  }

  // Ensure overlays stay on top
  m_streamNameOverlay->raise();
  m_pipStreamView->raise();

  updateStreamRouting();
}

void MainWindow::updateStreamRouting() {
  if (!m_telePlayer || !m_widePlayer || !m_mainVideoWidget || !m_pipVideoWidget)
    return;

  // Disconnect video outputs first to avoid conflicts
  m_telePlayer->setVideoOutput(nullptr);
  m_widePlayer->setVideoOutput(nullptr);

  const bool mainIsTele = (m_mainStream == CameraStream::Tele);
  if (mainIsTele) {
    m_telePlayer->setVideoOutput(m_mainVideoWidget);
    m_widePlayer->setVideoOutput(m_pipVideoWidget);
  } else {
    m_telePlayer->setVideoOutput(m_pipVideoWidget);
    m_widePlayer->setVideoOutput(m_mainVideoWidget);
  }
}

void MainWindow::startStreaming(const QString &ip) {
  if (!m_telePlayer || !m_widePlayer)
    return;

  qWarning() << "[MainWindow] startStreaming called for IP" << ip;

  qDebug() << "Sending OpenCamera commands...";
  // Ensure camera is opened on both Tele and Wide before requesting RTSP
  if (m_cameraController) {
    m_cameraController->openCamera(DwarfCameraController::CameraKind::Tele,
                                   true, 0);
    m_cameraController->openCamera(DwarfCameraController::CameraKind::Wide,
                                   false, 0);
  } else {
    qWarning()
        << "[MainWindow] m_cameraController is null, cannot open cameras";
  }
  // RTSP players will be started in onCameraTeleMessage / onCameraWideMessage
}

void MainWindow::stopStreaming() {
  if (m_telePlayer)
    m_telePlayer->stop();
  if (m_widePlayer)
    m_widePlayer->stop();
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

  m_mainStreamView = new QWidget(centralWidget);
  m_mainStreamView->setObjectName("mainStreamView");
  m_mainStreamView->setMinimumHeight(400);

  // Create Main Video Widget first
  m_mainVideoWidget = new QVideoWidget(m_mainStreamView);
  // m_mainVideoWidget->setStyleSheet("background-color: black; border: none;");
  QVBoxLayout *mainVideoLayout = new QVBoxLayout(m_mainStreamView);
  mainVideoLayout->setContentsMargins(0, 0, 0, 0);
  mainVideoLayout->addWidget(m_mainVideoWidget);
  m_mainVideoWidget->show();

  // Overlay Label for Stream Name - Parented to Video Widget
  m_streamNameOverlay = new QLabel(m_mainVideoWidget);
  m_streamNameOverlay->setObjectName("streamNameOverlay");
  // m_streamNameOverlay->setAttribute(Qt::WA_NativeWindow); // Removed
  m_streamNameOverlay->setStyleSheet(
      "QLabel { color: white; font-size: 16px; font-weight: bold; "
      "background-color: rgba(0, 0, 0, 100); padding: 4px 8px; border-radius: "
      "4px; }");
  m_streamNameOverlay->setAlignment(Qt::AlignCenter);

  // PiP View - Parented to Video Widget
  m_pipStreamView = new ClickableLabel(m_mainVideoWidget);
  m_pipStreamView->setObjectName("pipStreamView");
  // m_pipStreamView->setAttribute(Qt::WA_NativeWindow); // Removed
  m_pipStreamView->setFixedSize(220, 124);

  // Layout for Overlays on top of Main Video
  QGridLayout *overlayLayout = new QGridLayout(m_mainVideoWidget);
  overlayLayout->setContentsMargins(10, 10, 10, 10);
  overlayLayout->addWidget(m_streamNameOverlay, 0, 0,
                           Qt::AlignTop | Qt::AlignHCenter);
  overlayLayout->addWidget(m_pipStreamView, 0, 0, Qt::AlignTop | Qt::AlignLeft);
  // Add a stretch to push everything up
  overlayLayout->setRowStretch(1, 1);

  // PiP Video Widget inside PiP View
  m_pipVideoWidget = new QVideoWidget(m_pipStreamView);
  m_pipVideoWidget->setAttribute(Qt::WA_TransparentForMouseEvents, true);
  // m_pipVideoWidget->setStyleSheet("background-color: black; border: none;");
  QVBoxLayout *pipVideoLayout = new QVBoxLayout(m_pipStreamView);
  pipVideoLayout->setContentsMargins(3, 3, 3, 3);
  pipVideoLayout->addWidget(m_pipVideoWidget);
  m_pipVideoWidget->show();

  viewportLayout->addWidget(m_mainStreamView, 0, 0);
  // Overlays are now inside m_mainStreamView -> m_mainVideoWidget, so we don't
  // add them to viewportLayout

  viewportWidget->setLayout(viewportLayout);
  mainLayout->addWidget(viewportWidget);

  // Ensure overlays are on top (though parenting should handle this)
  m_streamNameOverlay->raise();
  m_pipStreamView->raise();

  m_pipStreamView->setStyleSheet(
      "border: 2px solid white; background-color: black;");

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
  m_ipInput->setText("192.168.8.223");
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
  connect(m_exposureModeCombo,
          QOverload<int>::of(&QComboBox::currentIndexChanged), this,
          &MainWindow::onExposureModeChanged);

  QLabel *shutterLabel = new QLabel(tr("Shutter"), exposureGroup);
  m_shutterSlider = new QSlider(Qt::Horizontal, exposureGroup);
  m_shutterSlider->setRange(1, 100);
  connect(m_shutterSlider, &QSlider::valueChanged, this,
          &MainWindow::onShutterSliderChanged);

  QLabel *gainLabel = new QLabel(tr("Gain"), exposureGroup);
  m_gainSlider = new QSlider(Qt::Horizontal, exposureGroup);
  m_gainSlider->setRange(0, 300);
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

  QLabel *brightnessLabel = new QLabel(tr("Brightness"), imageGroup);
  m_brightnessSlider = new QSlider(Qt::Horizontal, imageGroup);
  m_brightnessSlider->setRange(0, 100);
  connect(m_brightnessSlider, &QSlider::valueChanged, this,
          &MainWindow::onBrightnessSliderChanged);

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
  imageLayout->addWidget(brightnessLabel, 2, 0);
  imageLayout->addWidget(m_brightnessSlider, 2, 1);
  imageLayout->addWidget(contrastLabel, 3, 0);
  imageLayout->addWidget(m_contrastSlider, 3, 1);
  imageLayout->addWidget(saturationLabel, 4, 0);
  imageLayout->addWidget(m_saturationSlider, 4, 1);
  imageLayout->addWidget(sharpnessLabel, 5, 0);
  imageLayout->addWidget(m_sharpnessSlider, 5, 1);
  imageLayout->addWidget(hueLabel, 6, 0);
  imageLayout->addWidget(m_hueSlider, 6, 1);
  imageGroup->setLayout(imageLayout);

  QGroupBox *wbGroup = new QGroupBox(tr("White balance"), cameraTab);
  QGridLayout *wbLayout = new QGridLayout(wbGroup);

  QLabel *wbModeLabel = new QLabel(tr("Mode:"), wbGroup);
  m_wbModeCombo = new QComboBox(wbGroup);
  m_wbModeCombo->addItem(tr("Auto"));
  m_wbModeCombo->addItem(tr("Manual"));
  connect(m_wbModeCombo, QOverload<int>::of(&QComboBox::currentIndexChanged),
          this, &MainWindow::onWbModeChanged);

  QLabel *wbTempLabel = new QLabel(tr("Color temperature"), wbGroup);
  m_wbTemperatureSlider = new QSlider(Qt::Horizontal, wbGroup);
  m_wbTemperatureSlider->setRange(0, 100);
  connect(m_wbTemperatureSlider, &QSlider::valueChanged, this,
          &MainWindow::onWbTemperatureChanged);

  wbLayout->addWidget(wbModeLabel, 0, 0);
  wbLayout->addWidget(m_wbModeCombo, 0, 1);
  wbLayout->addWidget(wbTempLabel, 1, 0);
  wbLayout->addWidget(m_wbTemperatureSlider, 1, 1);
  wbGroup->setLayout(wbLayout);

  cameraLayout->addLayout(sourceLayout);
  cameraLayout->addLayout(captureLayout);
  cameraLayout->addWidget(exposureGroup);
  cameraLayout->addWidget(imageGroup);
  cameraLayout->addWidget(wbGroup);
  cameraLayout->addStretch();
  cameraTab->setLayout(cameraLayout);

  updateCameraStreamViews();

  QWidget *astroTab = new QWidget(this);
  QVBoxLayout *astroLayout = new QVBoxLayout(astroTab);
  QLabel *astroLabel = new QLabel(tr("Astro & Navigation (TODO)"), astroTab);
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
    m_statusLabel->setText(tr("Found %1 devices").arg(m_deviceList->count()));
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
    QMessageBox::warning(this, tr("Error"), tr("Please enter an IP address"));
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
    if (m_cameraController) {
      m_cameraController->setClient(nullptr);
    }
    stopStreaming();
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

    if (m_cameraController) {
      m_cameraController->setClient(m_wsClient);
    }

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
  qWarning() << "[MainWindow] WebSocket connected, starting streaming";
  m_connectButton->setEnabled(true);
  m_connectButton->setText(tr("Disconnect"));
  m_cancelConnectButton->setEnabled(
      false); // Can't cancel if already connected, use Disconnect
  m_statusLabel->setText(tr("Connected"));
  updateStatusStyle("ok");
  statusBar()->showMessage(tr("Connected to DWARF II"));

  // Start streaming now that we are connected
  QString ip = m_ipInput->text().trimmed();
  startStreaming(ip);
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
  if (!m_cameraController)
    return;
  DwarfCameraController::CameraKind kind =
      (m_mainStream == CameraStream::Tele)
          ? DwarfCameraController::CameraKind::Tele
          : DwarfCameraController::CameraKind::Wide;
  m_cameraController->takePhoto(kind);
}

void MainWindow::onCameraRecClicked() {
  if (!m_cameraController)
    return;
  DwarfCameraController::CameraKind kind =
      (m_mainStream == CameraStream::Tele)
          ? DwarfCameraController::CameraKind::Tele
          : DwarfCameraController::CameraKind::Wide;

  if (!m_isRecording) {
    m_cameraController->startRecord(kind);
    m_isRecording = true;
  } else {
    m_cameraController->stopRecord(kind);
    m_isRecording = false;
  }
}

void MainWindow::onExposureModeChanged(int index) {
  if (!m_cameraController)
    return;
  DwarfCameraController::CameraKind kind =
      (m_mainStream == CameraStream::Tele)
          ? DwarfCameraController::CameraKind::Tele
          : DwarfCameraController::CameraKind::Wide;
  m_cameraController->setExposureMode(kind, index);
}

void MainWindow::onShutterSliderChanged(int value) {
  if (!m_cameraController)
    return;
  DwarfCameraController::CameraKind kind =
      (m_mainStream == CameraStream::Tele)
          ? DwarfCameraController::CameraKind::Tele
          : DwarfCameraController::CameraKind::Wide;
  m_cameraController->setExposureIndex(kind, value);
}

void MainWindow::onGainSliderChanged(int value) {
  if (!m_cameraController)
    return;
  DwarfCameraController::CameraKind kind =
      (m_mainStream == CameraStream::Tele)
          ? DwarfCameraController::CameraKind::Tele
          : DwarfCameraController::CameraKind::Wide;
  m_cameraController->setGainIndex(kind, value);
}

void MainWindow::onIrCutToggled(bool checked) {
  if (!m_cameraController)
    return;
  DwarfCameraController::CameraKind kind =
      (m_mainStream == CameraStream::Tele)
          ? DwarfCameraController::CameraKind::Tele
          : DwarfCameraController::CameraKind::Wide;
  m_cameraController->setIrCut(kind, checked ? 1 : 0);
}

void MainWindow::onBinningChanged(int index) {
  Q_UNUSED(index);
  // TODO: Map binning to camera parameters when API details are clarified
}

void MainWindow::onContrastSliderChanged(int value) {
  if (!m_cameraController)
    return;
  DwarfCameraController::CameraKind kind =
      (m_mainStream == CameraStream::Tele)
          ? DwarfCameraController::CameraKind::Tele
          : DwarfCameraController::CameraKind::Wide;
  m_cameraController->setContrast(kind, value);
}

void MainWindow::onSaturationSliderChanged(int value) {
  if (!m_cameraController)
    return;
  DwarfCameraController::CameraKind kind =
      (m_mainStream == CameraStream::Tele)
          ? DwarfCameraController::CameraKind::Tele
          : DwarfCameraController::CameraKind::Wide;
  m_cameraController->setSaturation(kind, value);
}

void MainWindow::onSharpnessSliderChanged(int value) {
  if (!m_cameraController)
    return;
  DwarfCameraController::CameraKind kind =
      (m_mainStream == CameraStream::Tele)
          ? DwarfCameraController::CameraKind::Tele
          : DwarfCameraController::CameraKind::Wide;
  m_cameraController->setSharpness(kind, value);
}

void MainWindow::onHueSliderChanged(int value) {
  if (!m_cameraController)
    return;
  DwarfCameraController::CameraKind kind =
      (m_mainStream == CameraStream::Tele)
          ? DwarfCameraController::CameraKind::Tele
          : DwarfCameraController::CameraKind::Wide;
  m_cameraController->setHue(kind, value);
}

void MainWindow::onBrightnessSliderChanged(int value) {
  if (!m_cameraController)
    return;
  DwarfCameraController::CameraKind kind =
      (m_mainStream == CameraStream::Tele)
          ? DwarfCameraController::CameraKind::Tele
          : DwarfCameraController::CameraKind::Wide;
  m_cameraController->setBrightness(kind, value);
}

void MainWindow::onWbModeChanged(int index) {
  if (!m_cameraController)
    return;
  DwarfCameraController::CameraKind kind =
      (m_mainStream == CameraStream::Tele)
          ? DwarfCameraController::CameraKind::Tele
          : DwarfCameraController::CameraKind::Wide;
  m_cameraController->setWhiteBalanceMode(kind, index);
}

void MainWindow::onWbTemperatureChanged(int value) {
  if (!m_cameraController)
    return;
  DwarfCameraController::CameraKind kind =
      (m_mainStream == CameraStream::Tele)
          ? DwarfCameraController::CameraKind::Tele
          : DwarfCameraController::CameraKind::Wide;
  m_cameraController->setWhiteBalanceByTemperature(kind, value);
}

void MainWindow::onPipStreamClicked() {
  std::swap(m_mainStream, m_pipStream);
  updateCameraStreamViews();
}

void MainWindow::onCameraTeleMessage(uint32_t cmd, const QByteArray &data) {
  qWarning() << "[MainWindow] onCameraTeleMessage cmd" << cmd << "data size"
             << data.size();
  if (cmd == 10000) { // CMD_CAMERA_TELE_OPEN_CAMERA
    dwarf::ComResponse res;
    if (res.ParseFromArray(data.data(), data.size())) {
      if (res.code() == 0 || res.code() == 374) {
        qDebug() << "Tele camera opened (code" << res.code()
                 << "), starting MJPEG stream...";
        QString ip = m_ipInput->text().trimmed();
        // Use MJPEG stream on port 8092 instead of RTSP on 554
        // RTSP port 554 is often closed/refused, while MJPEG works in Python
        // legacy app
        const QUrl teleUrl(QStringLiteral("http://%1:8092/mainstream").arg(ip));
        if (m_telePlayer) {
          m_telePlayer->setSource(teleUrl);
          m_telePlayer->play();
        }
        updateStreamRouting();
        // Ensure overlays stay on top after video starts
        if (m_streamNameOverlay)
          m_streamNameOverlay->raise();
        if (m_pipStreamView)
          m_pipStreamView->raise();
      } else {
        qWarning() << "Failed to open Tele camera, code:" << res.code();
      }
    } else {
      qWarning() << "[MainWindow] Failed to parse Tele ComResponse for cmd"
                 << cmd;
    }
  }
}

void MainWindow::onCameraWideMessage(uint32_t cmd, const QByteArray &data) {
  qWarning() << "[MainWindow] onCameraWideMessage cmd" << cmd << "data size"
             << data.size();
  if (cmd == 12000) { // CMD_CAMERA_WIDE_OPEN_CAMERA
    dwarf::ComResponse res;
    if (res.ParseFromArray(data.data(), data.size())) {
      if (res.code() == 0 || res.code() == 374) {
        qDebug() << "Wide camera opened (code" << res.code()
                 << "), starting MJPEG stream...";
        QString ip = m_ipInput->text().trimmed();
        // Use MJPEG stream on port 8092 instead of RTSP on 554
        const QUrl wideUrl(
            QStringLiteral("http://%1:8092/secondstream").arg(ip));
        if (m_widePlayer) {
          m_widePlayer->setSource(wideUrl);
          m_widePlayer->play();
        }
        updateStreamRouting();
        // Ensure overlays stay on top after video starts
        if (m_streamNameOverlay)
          m_streamNameOverlay->raise();
        if (m_pipStreamView)
          m_pipStreamView->raise();
      } else {
        qWarning() << "Failed to open Wide camera, code:" << res.code();
      }
    } else {
      qWarning() << "[MainWindow] Failed to parse Wide ComResponse for cmd"
                 << cmd;
    }
  }
}
